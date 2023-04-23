# -*- coding: utf-8 -*-

__all__ = [
    'PhonemeCategory', 'Phoneme',
    'Note', 'PitchCurve',
    'Segment', 'Track',
    'VisualizeUnit', 'Label'
]

import enum
from dataclasses import dataclass, field
from typing import List, Mapping, Optional

import numpy as np


class PhonemeCategory(enum.Enum):
    BODY = enum.auto()  # usually vowel
    HEAD = enum.auto()  # usually consonant
    SP = enum.auto()  # silence
    AP = enum.auto()  # aspiration


@dataclass
class Phoneme:
    name: str = ''
    duration: float = 0.0
    category: PhonemeCategory = PhonemeCategory.SP


@dataclass
class Note:
    text: str = ''
    phonemes: List[Phoneme] = field(default_factory=lambda: [])
    duration: float = 0.0
    offset: float = 0.0
    midi_pitch: int = -1
    is_slur: bool = False


@dataclass
class PitchCurve:
    f0: "np.array" = field(default_factory=lambda: np.array([]))
    timestep: float = 0.05

    def __post_init__(self):
        self.f0 = np.asarray(self.f0)
        self.timestep = float(self.timestep)

    def get_midi_pitch(self, a4_midi=69, base_pitch=440.0):
        m = 12 * np.log2(self.f0 / base_pitch) + a4_midi
        return m


@dataclass
class Segment:
    offset: float = 0.0
    notes: List[Note] = field(default_factory=lambda: [])
    pitch_curve: PitchCurve = None


@dataclass
class Track:
    segments: List[Segment] = field(default_factory=lambda: [])
    attributes: str = ""


@dataclass
class VisualizeUnit:
    text_lyric: str = ''
    text_phoneme: str = ''
    offset: float = 0.0
    duration: float = 0.0
    midi_pitch: int = -1
    category: PhonemeCategory = PhonemeCategory.SP


@dataclass
class Label:
    text: str
    x: float
    y: float
