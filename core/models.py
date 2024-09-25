# -*- coding: utf-8 -*-

__all__ = [
    'Phoneme',
    'Note', 'Word', 'PitchCurve',
    'Segment', 'Parameter', 'Retake'
]

from dataclasses import dataclass, field
from typing import List, Literal, Optional

import numpy as np


@dataclass
class Phoneme:
    token: str = ''
    language: str = 'zh'
    start: float = 0.0
    #duration: float = 0.0


@dataclass
class Note:
    key: int = -1
    cents: int = 0
    duration: float = 0.0
    glide: str = "none"
    is_rest: bool = False
    #offset: float = 0.0
    #is_slur: bool = False
    #text: str = ''


@dataclass
class Word:
    phones: List[Phoneme] = field(default_factory=lambda: [])
    notes: List[Note] = field(default_factory=lambda: [])


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
class Retake:
    start: int = 0
    end: int = 0


@dataclass
class Parameter:
    tag: str
    dynamic: bool
    interval: float
    values: List[float] = field(default_factory=lambda: [])
    retake: Retake = field(default_factory=lambda: Retake())


@dataclass
class Segment:
    offset: float = 0.0
    words: List[Word] = field(default_factory=lambda: [])
    parameters: List[Parameter] = field(default_factory=lambda: [])
