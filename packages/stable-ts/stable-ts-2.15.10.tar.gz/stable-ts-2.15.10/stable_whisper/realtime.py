import subprocess
import time
from typing import List, Union, Tuple, Optional
from dataclasses import dataclass
from types import MethodType
import re

import numpy as np
import torch
from torch.nn.functional import pad

import whisper
from whisper.audio import (
    SAMPLE_RATE, N_FRAMES, HOP_LENGTH, N_SAMPLES, N_SAMPLES_PER_TOKEN, TOKENS_PER_SECOND, FRAMES_PER_SECOND, N_FFT,
    pad_or_trim, log_mel_spectrogram
)
from whisper.decoding import DecodingOptions

from .audio import AudioLoader
from .utils import isolate_useful_options
from .whisper_compatibility import get_tokenizer
from .decode import decode_stable
from .timing import _split_tokens, add_word_timestamps_stable
from .result import WhisperResult
from .default import get_append_punctuations, get_prepend_punctuations


@dataclass
class TempWord:
    word_dict: dict
    offset: Optional[float] = None

    def __post_init__(self):
        self.match = 0
        self._remove_appends = get_append_punctuations().replace('.', r'\.')
        self._remove_prepends = get_prepend_punctuations().replace('.', r'\.')

    @property
    def start(self) -> float:
        return self.word_dict['start']

    @property
    def end(self) -> float:
        return self.word_dict['end']

    @property
    def word(self) -> str:
        return self.word_dict['word']

    @property
    def probability(self) -> float:
        return self.word_dict['probability']

    @property
    def tokens(self) -> List[int]:
        return self.word_dict['tokens']

    @start.setter
    def start(self, new_start: float):
        self.word_dict['start'] = new_start

    @end.setter
    def end(self, new_end: float):
        self.word_dict['end'] = new_end

    def min_clamp(self, min_offset: float) -> bool:
        if self.start >= min_offset:
            return False
        self.start = min_offset
        if self.end >= min_offset:
            return False
        self.end = min_offset
        return True

    def update_word(self, new_word: "TempWord", update_ts: bool = False):
        if update_ts:
            # self.word_dict = new_word.word_dict
            # return
            if new_word.start < self.end:
                self.start = max(self.start, new_word.start)
            # self.end = min(self.end, new_word.end)
        self.word_dict['word'] = new_word.word
        self.word_dict['probability'] = new_word.probability
        self.word_dict['tokens'] = new_word.tokens

    def is_text_match(self, other_word: Union["TempWord", str]) -> bool:
        text = self.normalize_word()
        other_text = self.normalize_text(other_word) if isinstance(other_word, str) else other_word.normalize_word()
        return text == other_text[:len(text)] or text[-len(other_text):] == other_text

    def normalize_text(self, text: str) -> str:
        text = text.strip()
        text = re.sub(f'^[{self._remove_prepends}]', '', text)
        text = re.sub(f'[{self._remove_appends}]$', '', text)
        return text

    def normalize_word(self) -> str:
        return self.normalize_text(self.word)

    def apply_offset(self, offset: float):
        self.start += offset
        self.end += offset
        self.offset = offset
        return self


def fw_get_prompt(
        self,
        tokenizer,
        previous_tokens: List[int],
        without_timestamps: bool = False,
        prefix: Optional[Union[str, List[int]]] = None,
) -> List[int]:

    prompt = []

    if previous_tokens:
        prompt.append(tokenizer.sot_prev)
        prompt.extend(previous_tokens[-(self.max_length // 2 - 1) :])

    prompt.extend(tokenizer.sot_sequence)

    if without_timestamps:
        prompt.append(tokenizer.no_timestamps)

    if prefix:
        prefix_tokens = tokenizer.encode(" " + prefix.strip()) if isinstance(prefix, str) else prefix
        if len(prefix_tokens) >= self.max_length // 2:
            prefix_tokens = prefix_tokens[: self.max_length // 2 - 1]
        if not without_timestamps:
            prompt.append(tokenizer.timestamp_begin)
        prompt.extend(prefix_tokens)

    return prompt


class LiveWhisper:

    def __init__(self, model: whisper.Whisper, language: Optional[str] = None):
        if not isinstance(model, whisper.Whisper):
            raise NotImplementedError(f'Live transcription has not been implemented for {type(model)}.')
            # model.get_prompt = MethodType(fw_get_prompt, model)
        self._model = model
        self.dtype = torch.float16
        self._task = 'transcribe'
        self._language = language
        self._tokenizer = None
        self._prob_threshold = self._audio_feature = self._audio_chunk = self._chunk_mel = None
        self.unfinalized_words: List[TempWord] = []
        self.finalized_words: List[TempWord] = []
        self._min_prefix_index = 0
        self._seek = 0
        self._offset = 0.0

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, new_model):
        if new_model is not self._model:
            self._model = new_model

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, language: str):
        if self._language != language:
            self._language = language
            self._set_tokenizer()

    @property
    def prob_threshold(self):
        return self._prob_threshold

    @prob_threshold.setter
    def prob_threshold(self, threshold: float):
        self._prob_threshold = threshold

    @property
    def tokenizer(self):
        return self._tokenizer

    def _set_tokenizer(self):
        if self._tokenizer is None or self._tokenizer.language != self._language:
            self._tokenizer = get_tokenizer(self.model, task=self._task, language=self._language)

    def reset_states(self):
        self._prob_threshold = self._audio_feature = self._audio_chunk = self._chunk_mel = None
        self.unfinalized_words: List[TempWord] = []
        self.finalized_words: List[TempWord] = []
        self._min_prefix_index = 0
        self._seek = 0
        self._offset = 0.0

    def transcribe(
            self,
            audio,
            chunk_length: Union[int, str] = '0.25s',
            language: str = 'en',
            no_speech_threshold: float = 0.6,
            k=2,
            inference_chunk_size=5,
            prob_threshold: Optional[float] = 0.1,
            playback: bool = False,
            **kwargs
    ):
        if isinstance(chunk_length, str):
            assert chunk_length.endswith('s')
            chunk_length = round(float(chunk_length[:-1]) * SAMPLE_RATE)
        if not isinstance(audio, AudioLoader):
            audio = AudioLoader(audio, chunk_length, sr=SAMPLE_RATE, playback=playback)
        assert not isinstance(kwargs.get('temperature'), (list, tuple)), 'temperature can only be a single value'
        self.reset_states()
        self.language = language
        self.prob_threshold = prob_threshold

        next_seek = 0

        max_inference_samples = round(SAMPLE_RATE * inference_chunk_size)
        max_prefix_samples = max_inference_samples - chunk_length

        while True:

            prefix_tokens, prefix_words_count = self._get_prefix(next_seek, max_prefix_samples=max_prefix_samples)

            target_chunk_length = next_seek - self._seek + chunk_length
            next_seek = self._seek + target_chunk_length
            self._audio_chunk = audio.next_chunk(self._seek, target_chunk_length)
            if self._audio_chunk is None:
                break

            temp_words = self._transcribe_chunk(
                no_speech_threshold,
                prefix_tokens=prefix_tokens,
                prefix_words_count=prefix_words_count
            )
            if not temp_words:
                if prefix_tokens:
                    self._update_seek(next_seek)
                self._mark_nonspeech()
                continue

            last_i = self._update_unfinalized_words(temp_words, k)
            self.remove_unconfident_words(self.unfinalized_words)

            if target_chunk_length != self._audio_chunk.size(-1):
                last_i = len(self.unfinalized_words)

            self._update_finalized_words(last_i)

        audio.terminate()
        result = WhisperResult([[w.word_dict for w in self.finalized_words]])
        return result

    def _transcribe_chunk(
            self,
            no_speech_threshold: float,
            prefix_tokens: Optional[List[int]] = None,
            prefix_words_count: Optional[int] = None,
            **kwargs
    ) -> List[TempWord]:
        result = self._decode(prefix=prefix_tokens, **kwargs)
        if (not prefix_tokens and result.no_speech_prob > no_speech_threshold) or not result.tokens:
            return []

        return self._add_timestamp_words(
            tokens=result.tokens,
            prefix_tokens=prefix_tokens,
            prefix_words_count=prefix_words_count
        )

    def _update_unfinalized_words(self, temp_words: List[TempWord], k) -> int:
        last_i = None
        self.unfinalized_words = self.unfinalized_words[:len(temp_words)]
        min_offset = None
        for i, temp_word in enumerate(temp_words):
            if i < len(self.unfinalized_words):
                unfinalize_word = self.unfinalized_words[i]
                is_match = unfinalize_word.is_text_match(temp_word)
                if is_match:
                    unfinalize_word.update_word(temp_word, True)
                    unfinalize_word.match += 1
                    if unfinalize_word.match > k:
                        last_i = i + 1
                    continue
                else:
                    self.unfinalized_words = self.unfinalized_words[:i]
                    if self.unfinalized_words:
                        min_offset = self.unfinalized_words[-1].end

            if min_offset is not None and not temp_word.min_clamp(min_offset):
                min_offset = None

            self.unfinalized_words.append(temp_word)

        return last_i

    def _get_prefix(
            self, next_seek: int, max_prefix_samples: int
    ):
        prefix_count = None
        prefix_words = self.finalized_words[self._min_prefix_index:]
        if prefix_words:
            seek_time = round(max(next_seek - max_prefix_samples, self._seek) / SAMPLE_RATE, 3)
            for i, word in enumerate(reversed(prefix_words), 1):
                if word.start < seek_time:
                    break
                prefix_count = i

        if prefix_count is None:
            prefix_tokens = prefix_words_count = None
            self._update_seek(next_seek - max_prefix_samples)

            if self.unfinalized_words:
                for i, word in enumerate(reversed(self.unfinalized_words), 1):
                    if word.start < self._offset:
                        break
                    prefix_count = i
                finalize_count = (len(self.unfinalized_words) - prefix_count) if prefix_count else None
                self._update_finalized_words(finalize_count, update_seek=True)

        else:
            prefix = prefix_words[-prefix_count:]
            prefix_words_count = len(prefix)
            self._update_seek(round(prefix[0].start * SAMPLE_RATE), offset=prefix[0].start)
            prefix_tokens = [t for w in prefix for t in w.tokens]

        return prefix_tokens, prefix_words_count

    def _update_seek(self, seek: int, offset: Optional[float] = None, ignore_invalid: bool = True):
        if seek == self._seek or (seek < self._seek and ignore_invalid):
            return
        self._seek = seek
        if offset is None:
            offset = round(self._seek / SAMPLE_RATE, 3)
        self._offset = offset

    def on_words_callback(self, new_words: List[TempWord]):
        print(''.join(w.word for w in new_words))

    def _mark_nonspeech(self):
        self.unfinalized_words = []
        self._min_prefix_index = len(self.finalized_words)

    def _update_finalized_words(self, count: Optional[int], update_seek: bool = False):
        if not count or not self.unfinalized_words:
            return

        if self.finalized_words and self.unfinalized_words[0].is_text_match(self.finalized_words[-1]):
            self.finalized_words[-1].update_word(self.unfinalized_words[0], True)
            del self.unfinalized_words[0]
            if not self.unfinalized_words:
                return
            count -= 1

        new_words, self.unfinalized_words = self.unfinalized_words[:count], self.unfinalized_words[count:]
        if not new_words:
            return
        self.on_words_callback(new_words)
        self.finalized_words.extend(new_words)
        if update_seek:
            new_offset = self.finalized_words[-1].end
            self._update_seek(round(new_offset * SAMPLE_RATE), new_offset)

    def _decode(self, **kwargs):
        left_pad = N_SAMPLES - self._audio_chunk.size(-1)
        assert left_pad >= 0
        mel_chunk = log_mel_spectrogram(
            pad(self._audio_chunk, (0, left_pad)),
            self.model.dims.n_mels
        ).to(device=self.model.device, dtype=self.dtype)
        decoding_options = DecodingOptions(**kwargs, without_timestamps=True, language=self._language)
        result, self._audio_feature = decode_stable(self.model, mel_chunk, decoding_options, max_new_tokens=5)
        return result

    def _add_timestamp_words(
            self,
            tokens: List[int],
            prefix_tokens: Optional[List[int]],
            prefix_words_count: Optional[int],
    ) -> List[TempWord]:
        if prefix_tokens:
            tokens = prefix_tokens + tokens
        words, tokens = _split_tokens(tokens, self._tokenizer)

        segment = dict(
            seek=self._offset,
            tokens=(words, tokens)
        )

        add_word_timestamps_stable(
            segments=[segment],
            model=self._model,
            tokenizer=self._tokenizer,
            mel=self._chunk_mel,
            audio_features=self._audio_feature,
            num_samples=self._audio_chunk.size(-1),
            split_callback=(lambda x, _: x),
            gap_padding=None
        )

        words = segment['words'][prefix_words_count:] if prefix_words_count else segment['words']

        temp_words = [TempWord(word, offset=self._offset) for word in words]
        if prefix_tokens:
            self.min_clamp(temp_words)
        return temp_words

    def remove_unconfident_words(self, words: List[TempWord]):
        for i in reversed(range(len(words))):
            nonzero_duration = words[i].end - words[i].start != 0
            meet_prob_threshold = words[i].probability >= self._prob_threshold
            if nonzero_duration and meet_prob_threshold:
                break
            del words[i]

    def min_clamp(self, words: List[TempWord], min_offset: Optional[float] = None):
        if not words:
            return
        if min_offset is None and self.finalized_words:
            min_offset = self.finalized_words[-1].end
        if min_offset is None or words[0].start >= min_offset:
            return
        for w in words:
            if not w.min_clamp(min_offset):
                break
        self.remove_unconfident_words(words)
