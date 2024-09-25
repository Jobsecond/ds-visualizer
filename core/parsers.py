# -*- coding: utf-8 -*-
__all__ = [
    'parse_segment'
]

from typing import List, Mapping, Optional
from decimal import Decimal

import numpy as np

from .models import *
from utils import *


def parse_segment(segment: Mapping) -> Optional[Segment]:
    offset = segment.get('offset', 0.0)
    f0_seq = np.array([float(x) for x in segment['f0_seq'].split()])
    f0_timestep = float(segment['f0_timestep'])
    text = np.array(segment['text'].split())
    ph_seq = np.array(segment['ph_seq'].split())
    ph_dur = np.array([Decimal(x) for x in segment['ph_dur'].split()])
    ph_num = np.array([int(x) for x in segment['ph_num'].split()])
    note_seq = np.array(segment['note_seq'].split())
    note_dur = np.array([Decimal(x) for x in segment['note_dur'].split()])
    note_slur = np.array([bool(int(x)) for x in segment['note_slur'].split()])
    if 'gender' in segment and segment['gender'] is not None \
            and 'gender_timestep' in segment and segment['gender_timestep'] is not None:
        gender_seq = np.array([float(x) for x in segment['gender'].split()])
        gender_timestep = float(segment['gender_timestep'])
    else:
        gender_seq = None
        gender_timestep = None
    if 'velocity' in segment and segment['velocity'] is not None \
            and 'velocity_timestep' in segment and segment['velocity_timestep'] is not None:
        velocity_seq = np.array([float(x) for x in segment['velocity'].split()])
        velocity_timestep = float(segment['velocity_timestep'])
    else:
        velocity_seq = None
        velocity_timestep = None


    # sanity check
    assert_conditions = [
        len(note_slur) == len(note_dur),
        len(note_slur) == len(note_seq),
        len(text) == len(ph_num),
        sum(ph_num) == len(ph_seq),
        len(ph_seq) == len(ph_dur),
        len(note_slur[~note_slur]) == len(ph_num),  # num of non-slur notes == num of ph_num items
    ]
    if not all(assert_conditions):
        return None

    # index_notes_nonslur = np.nonzero(~note_slur)[0]  # `nonzero` returns a tuple
    # for index, item in enumerate(index_notes_nonslur):
    #    # TODO
    #    note = Note(text=text[index], duration=note_)
    words = []
    current_word = None
    flag_slur = False
    notes = []
    i = 0
    j = 0
    k = 0
    ph_offset_cumsum = Decimal("0.0")
    note_offset_cumsum = Decimal("0.0")
    epsilon = 10000  # Deal with float precision. Avoid something like 0.1 + 0.2 -> 0.30000000000000004
    while i < len(note_seq) and j < len(text) and k < len(ph_seq):
        ph_count = ph_num[j]
        phoneme_list = []
        midi_pitch = note_to_midi(note_seq[i])
        flag_slur = note_slur[i]
        if not flag_slur:
            if current_word is not None:
                words.append(current_word)
            current_word = Word()
            ph_offset_cumsum *= 0

            for m in range(1, 1 + ph_count):
                #current_phoneme = Phoneme(token=ph_seq[k], duration=float(ph_dur[k]), start=float(ph_offset_cumsum))
                current_token_raw = ph_seq[k]
                if "/" in current_token_raw:
                    current_lang, current_token = current_token_raw.split('/', 1)
                    current_phoneme = Phoneme(token=current_token, language=current_lang, start=float(ph_offset_cumsum))
                else:
                    current_phoneme = Phoneme(token=current_token_raw, start=float(ph_offset_cumsum))
                phoneme_list.append(current_phoneme)
                current_word.phones.append(current_phoneme)
                ph_offset_cumsum += ph_dur[k]
                k += 1
        #note_cv = Note(text=text[j] if not note_slur[i] else '-',
        #               duration=note_dur[i],
        #               offset=note_offset_cumsum / epsilon,
        #               key=midi_pitch,
        #               is_slur=note_slur[i])
        note_cv = Note(key=(0 if midi_pitch == -1 else midi_pitch),
                       duration=float(note_dur[i]),
                       is_rest=(midi_pitch == -1))
        notes.append(note_cv)
        current_word.notes.append(note_cv)

        note_offset_cumsum = (note_offset_cumsum + note_dur[i] * epsilon)
        i += 1
        if ((i < len(note_slur)) and (not note_slur[i])) \
                or (i >= len(note_slur)):
            # if current note is not the last note, and the following note is not slur;
            # or current note is already the last note
            j += 1

    #
    words.append(current_word)
    current_word = None

    pitch_curve = PitchCurve(f0=f0_seq, timestep=f0_timestep)
    pitch_param = Parameter(tag="pitch", dynamic=True, interval=pitch_curve.timestep,
                            values=pitch_curve.get_midi_pitch().tolist(),
                            retake=Retake(0, len(pitch_curve.f0)))
    parameters = [pitch_param]
    if gender_seq is not None:
        gender_param = Parameter(tag="gender", dynamic=True, interval=gender_timestep,
                                 values=gender_seq.tolist(),
                                 retake=Retake(0, len(gender_seq)))
        parameters.append(gender_param)
    if velocity_seq is not None:
        velocity_param = Parameter(tag="velocity", dynamic=True, interval=velocity_timestep,
                                   values=velocity_seq.tolist(),
                                   retake=Retake(0, len(velocity_seq)))
        parameters.append(velocity_param)
    output_segment = Segment(offset=offset, parameters=parameters, words=words)
    return output_segment
