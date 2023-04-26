# -*- coding: utf-8 -*-
__all__ = [
    'parse_segment',
    'get_visualize_units_track'
]

from typing import List, Mapping, Optional

import numpy as np

from .models import *
from utils import *


def parse_segment(segment: Mapping) -> Optional[Segment]:
    offset = segment.get('offset', 0.0)
    f0_seq = np.array([float(x) for x in segment['f0_seq'].split()])
    f0_timestep = float(segment['f0_timestep'])
    text = np.array(segment['text'].split())
    ph_seq = np.array(segment['ph_seq'].split())
    ph_dur = np.array([float(x) for x in segment['ph_dur'].split()])
    ph_num = np.array([int(x) for x in segment['ph_num'].split()])
    note_seq = np.array(segment['note_seq'].split())
    note_dur = np.array([float(x) for x in segment['note_dur'].split()])
    note_slur = np.array([bool(int(x)) for x in segment['note_slur'].split()])

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
    notes = []
    i = 0
    j = 0
    k = 0
    note_offset_cumsum = 0.0
    epsilon = 10000  # Deal with float precision. Avoid something like 0.1 + 0.2 -> 0.30000000000000004
    while i < len(note_seq) and j < len(text) and k < len(ph_seq):
        ph_count = ph_num[j]
        phoneme_list = []
        midi_pitch = note_to_midi(note_seq[i])
        if not note_slur[i]:
            for m in range(1, 1 + ph_count):
                if ph_seq[k] == 'AP':
                    category = PhonemeCategory.AP
                elif ph_seq[k] == 'SP':
                    category = PhonemeCategory.SP
                elif ph_count > 1 and m == ph_count:
                    category = PhonemeCategory.HEAD
                else:
                    category = PhonemeCategory.BODY
                phoneme_list.append(Phoneme(name=ph_seq[k], duration=ph_dur[k], category=category))
                k += 1
        note_cv = Note(text=text[j] if not note_slur[i] else '-',
                       phonemes=phoneme_list,
                       duration=note_dur[i],
                       offset=note_offset_cumsum / epsilon,
                       midi_pitch=midi_pitch,
                       is_slur=note_slur[i])
        notes.append(note_cv)

        note_offset_cumsum = (note_offset_cumsum + note_dur[i] * epsilon)
        i += 1
        if ((i < len(note_slur)) and (not note_slur[i])) \
                or (i >= len(note_slur)):
            # if current note is not the last note, and the following note is not slur;
            # or current note is already the last note
            j += 1

    pitch_curve = PitchCurve(f0=f0_seq, timestep=f0_timestep)
    output_segment = Segment(offset=offset, notes=notes, pitch_curve=pitch_curve)
    return output_segment


def get_visualize_units_track(track: Track) -> List[VisualizeUnit]:
    visualize_units_track = []
    for segment in track.segments:
        visualize_units_segment = []
        slur_stack = []
        for i in range(len(segment.notes)):
            note = segment.notes[i]
            next_note = segment.notes[i + 1] if i + 1 < len(segment.notes) else None
            slur_stack.append(note)
            if not ((next_note is None) or ((next_note is not None) and (not next_note.is_slur))):
                continue
            current_phonemes = slur_stack[0].phonemes
            dur_all_notes_in_slur_stack = float_sum(x.duration for x in slur_stack)
            dur_all_heads_in_slur_stack = float_sum(x.duration for x in current_phonemes
                                                    if x.category == PhonemeCategory.HEAD)
            dur_all_bodies_in_slur_stack_ds = float_sum(x.duration for x in current_phonemes
                                                        if x.category != PhonemeCategory.HEAD)
            dur_all_bodies_in_slur_stack = float_sum([dur_all_notes_in_slur_stack,
                                                      -dur_all_heads_in_slur_stack])
            dur_all_bodies_in_slur_stack_delta = float_sum([dur_all_bodies_in_slur_stack, -dur_all_bodies_in_slur_stack_ds])
            #bodies_count_in_slur_stack = len([x for x in current_phonemes if x.category != PhonemeCategory.HEAD])
            #dur_bodies_balance_in_slur_stack = dur_all_bodies_in_slur_stack
            offset_cumsum = float_sum([segment.offset, slur_stack[0].offset])
            idx_note = 0
            idx_ph = 0
            #current_ph_duration_balance = 0

            # find the split point (in which note) of body and head notes.
            body_head_split_index = 0
            tmp = dur_all_bodies_in_slur_stack
            for curr_note in slur_stack:
                tmp = float_sum([tmp, -curr_note.duration])
                if tmp < 0:
                    break
                body_head_split_index += 1
            curr_ph_dur_remaining = 0
            curr_note_dur_remaining = 0
            while idx_note < len(slur_stack) and idx_ph < len(current_phonemes):
                # if slur_stack[idx_note].duration <= current_phonemes[idx_ph].duration:
                #     current_ph_duration_balance = current_phonemes[idx_ph].duration
                #     current_duration = current_phonemes[idx_ph].duration
                #     idx_ph += 1
                # else:
                #     current_duration = slur_stack[idx_note].duration
                if curr_ph_dur_remaining == 0:
                    curr_ph_dur_remaining = current_phonemes[idx_ph].duration
                current_text_lyric = '' if current_phonemes[idx_ph].category != PhonemeCategory.BODY \
                    else slur_stack[idx_note].text
                if current_phonemes[idx_ph].category != PhonemeCategory.HEAD:
                    if idx_note < body_head_split_index:
                        visualize_unit = VisualizeUnit(text_lyric=current_text_lyric,# if not slur_stack[idx_note].is_slur else '-',
                                                       text_phoneme=current_phonemes[idx_ph].name,# if not slur_stack[idx_note].is_slur else '-',
                                                       offset=offset_cumsum,
                                                       midi_pitch=slur_stack[idx_note].midi_pitch,
                                                       duration=slur_stack[idx_note].duration,
                                                       category=current_phonemes[idx_ph].category)
                        offset_cumsum = float_sum([offset_cumsum, visualize_unit.duration])
                        visualize_units_segment.append(visualize_unit)
                        curr_ph_dur_remaining = float_sum([curr_ph_dur_remaining, -slur_stack[idx_note].duration])
                        idx_note += 1
                        continue
                    else:
                        curr_ph_dur_remaining = float_sum([curr_ph_dur_remaining, dur_all_bodies_in_slur_stack_delta])
                        visualize_unit = VisualizeUnit(text_lyric=current_text_lyric,# if not slur_stack[idx_note].is_slur else '-',
                                                       text_phoneme=current_phonemes[idx_ph].name,# if not slur_stack[idx_note].is_slur else '-',
                                                       offset=offset_cumsum,
                                                       midi_pitch=slur_stack[idx_note].midi_pitch,
                                                       duration=curr_ph_dur_remaining,
                                                       category=current_phonemes[idx_ph].category)
                        offset_cumsum = float_sum([offset_cumsum, visualize_unit.duration])
                        visualize_units_segment.append(visualize_unit)
                        curr_note_dur_remaining = max(0.0, float_sum([slur_stack[idx_note].duration, -curr_ph_dur_remaining]))
                        if curr_note_dur_remaining == 0:
                            idx_note += 1
                        curr_ph_dur_remaining = 0
                        idx_ph += 1
                        continue
                else:  # "head" notes
                    if idx_note == body_head_split_index:
                        use_dur = curr_note_dur_remaining
                    else:
                        use_dur = curr_ph_dur_remaining
                    visualize_unit = VisualizeUnit(text_lyric=current_text_lyric,# if not slur_stack[idx_note].is_slur else '-',
                                                   text_phoneme=current_phonemes[idx_ph].name,# if not slur_stack[idx_note].is_slur else '-',
                                                   offset=offset_cumsum,
                                                   midi_pitch=slur_stack[idx_note].midi_pitch,
                                                   duration=use_dur,
                                                   category=current_phonemes[idx_ph].category)
                    offset_cumsum = float_sum([offset_cumsum, visualize_unit.duration])
                    visualize_units_segment.append(visualize_unit)
                    curr_ph_dur_remaining = float_sum([curr_ph_dur_remaining, -use_dur])
                    idx_note += 1
                    continue
            slur_stack.clear()

        last_pitch = None
        for vu in reversed(visualize_units_segment):
            if vu.category in [PhonemeCategory.SP, PhonemeCategory.AP]:
                continue
            if last_pitch is not None and vu.midi_pitch == -1:
                vu.midi_pitch = last_pitch
            last_pitch = vu.midi_pitch

        visualize_units_track.extend(visualize_units_segment)

    return visualize_units_track
