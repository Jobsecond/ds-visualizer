# -*- coding: utf-8 -*-
__all__ = [
    'visualize_track'
]

from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from matplotlib.patches import Rectangle
from matplotlib import font_manager

from core.models import *
from utils import *
from core.parsers import *


def visualize_track(track: Track, output: str,
                    display_f0: bool = True,
                    color_head: str = '#8c2128',
                    color_body: str = '#d34343',
                    color_f0: str = '#e0e0e0',
                    color_text: str = '#000000',
                    figsize=(1280, 15),
                    dpi=50,
                    aspect=0.125,
                    font_name='fonts/NotoSansCJKsc-Medium.otf',
                    font_size=12,
                    font_style='normal'):
    fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)

    if display_f0:
        for segment in track.segments:
            f0_midi = segment.pitch_curve.get_midi_pitch()
            timestep = segment.pitch_curve.timestep
            f0_t = np.full_like(f0_midi, timestep)
            f0_t = float_sum([f0_t.cumsum(), segment.offset])
            ax.plot(f0_t, f0_midi, color=color_f0)

    visualize_units_track = get_visualize_units_track(track)
    patches = []
    colors = []
    ph_labels = []
    lyrics_labels = []
    for vu in visualize_units_track:
        if vu.category in [PhonemeCategory.SP, PhonemeCategory.AP]:
            continue
        patch = Rectangle(
            xy=(vu.offset, vu.midi_pitch - 0.5),
            width=vu.duration,
            height=1.0
        )
        patches.append(patch)
        colors.append(color_body if vu.category == PhonemeCategory.BODY else color_head)
        ph_labels.append(Label(text=vu.text_phoneme, x=float_sum([vu.offset * 2, vu.duration]) / 2, y=vu.midi_pitch - 1))
        lyrics_labels.append(Label(text=vu.text_lyric, x=float_sum([vu.offset, 0.01]), y=vu.midi_pitch + 0.75))

    #print(ph_labels)
    pc = mc.PatchCollection(patches, facecolors=colors, edgecolors='#400d51', linewidths=0.5)
    ax.add_collection(pc)
    #print('\n'.join(str(_) for _ in patches))

    font = font_manager.FontProperties(
        fname=font_name,
        size=font_size,
        style=font_style)
    for ph_label in ph_labels:
        ax.text(x=ph_label.x, y=ph_label.y, s=ph_label.text, horizontalalignment='center', color=color_text, fontproperties=font)
    for lyric_label in lyrics_labels:
        ax.text(x=lyric_label.x, y=lyric_label.y, s=lyric_label.text, horizontalalignment='left', color=color_text, fontproperties=font)

    ymax = max(visualize_units_track, key=lambda x: x.midi_pitch).midi_pitch + 1
    ymin = min(visualize_units_track, key=lambda x: x.midi_pitch if x.midi_pitch != -1 else ymax).midi_pitch - 1
    xmin = 0
    xmax = max([float_sum([x.duration, x.offset]) for x in visualize_units_track]) + 1
    ax.axis('off')
    ax.set_aspect(aspect=aspect)
    plt.xlim((xmin, xmax))
    plt.ylim((ymin, ymax))
    plt.savefig(output, transparent=True, bbox_inches='tight', pad_inches=0)
