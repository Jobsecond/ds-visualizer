# -*- coding: utf-8 -*-

__all__ = [
    'f0_to_midi',
    'note_to_midi',
]

import re


import numpy as np


def f0_to_midi(f0_value, a4_midi=69, base_pitch=440.0):
    m = 12 * np.log2(f0_value / base_pitch) + a4_midi
    return m


def note_to_midi(note: str) -> int:
    if not note:
        return -1

    note = note.strip()\
        .replace('\u266d', 'b')\
        .replace('\u266f', '#')\
        .replace('\U0001d12a', '##')\
        .replace('\U0001d12b', 'bb')\
        .lower()
    # \u266d means unicode "flat" symbol
    # \u266f means unicode "sharp" symbol
    # \U0001d12a means unicode "double sharp" symbol
    # \U0001d12b means unicode "double flat" symbol

    if note == 'rest':
        return -1
    matches = re.findall(r'([a-g])(.*?)(-?\d+)', note, re.IGNORECASE)
    if not matches:
        return -1
    note_letter, accidental, octave = matches[0]
    if accidental.lower() not in ['', 'b', '#', 'bb', '##']:
        return -1
    midi_value = (int(octave) + 1) * 12
    midi_value += {'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11}[note_letter.lower()]
    midi_value += {'#': 1, '##': 2, 'b': -1, 'bb': -2}.get(accidental.lower(), 0)
    return midi_value
