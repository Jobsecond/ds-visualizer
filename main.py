#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import argparse
import sys
import re

from core.models import *
from core.parsers import *
from visualizer.visualizers import *
from utils.misc import convert_color_str


def main():
    version = ""
    try:
        with open(os.path.join(os.path.dirname(__file__), "VERSION"), "r", encoding="utf-8") as version_f:
            version = "version {}".format(version_f.read())
    except IOError:
        pass
    except NameError:
        pass

    try:
        script_dir = os.path.realpath(os.path.dirname(__file__))
    except NameError:
        script_dir = os.path.realpath(os.getcwd())

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('-i', '--input',
                                 type=str,
                                 help='input .ds project file')
    argument_parser.add_argument('-o', '--output',
                                 type=str,
                                 required=False,
                                 help='output file (.svg format recommended)')
    argument_parser.add_argument('--color-head',
                                 type=str,
                                 default='8c2128',
                                 help='color of "head" notes (e.g. consonants)')
    argument_parser.add_argument('--color-body',
                                 type=str,
                                 default='d34343',
                                 help='color of "body" notes (e.g. vowels)')
    argument_parser.add_argument('--color-f0',
                                 type=str,
                                 default='cc88cc',
                                 help='color of pitch curve')
    argument_parser.add_argument('--color-text',
                                 type=str,
                                 default='000000',
                                 help='color of text (lyrics and phonemes)')
    argument_parser.add_argument('--width',
                                 type=int,
                                 default=1280,
                                 help='width of figure')
    argument_parser.add_argument('--height',
                                 type=int,
                                 default=15,
                                 help='width of figure')
    argument_parser.add_argument('--dpi',
                                 type=int,
                                 default=50,
                                 help='dots per inch (DPI) of figure')
    argument_parser.add_argument('--aspect',
                                 type=float,
                                 default=0.125,
                                 help='aspect ratio of figure')
    argument_parser.add_argument('--font-name',
                                 type=str,
                                 required=False,
                                 help='filename of font')
    argument_parser.add_argument('--font-size',
                                 type=float,
                                 default=12.0,
                                 help='font size')
    argument_parser.add_argument('--font-style',
                                 type=str,
                                 default='normal',
                                 help='font style (normal, bold, italic, etc.)')
    argument_parser.add_argument('--no-f0',
                                 action='store_true',
                                 required=False,
                                 default=False,
                                 help='do not plot pitch curve')

    args = argument_parser.parse_args()

    input_filename = args.input
    output_filename = args.output
    color_head = convert_color_str(args.color_head)
    color_body = convert_color_str(args.color_body)
    color_f0 = convert_color_str(args.color_f0)
    color_text = convert_color_str(args.color_text)

    figsize = (int(args.width), int(args.height))
    dpi = int(args.dpi)
    aspect = float(args.aspect)

    font_name = args.font_name
    font_size = float(args.font_size)
    font_style = args.font_style

    if font_name is None:
        font_name = os.path.join(script_dir, 'fonts', 'NotoSansCJKsc-Medium.otf')

    display_f0 = not args.no_f0

    print(args, display_f0)

    print("DiffSinger project file (.ds) visualizer")
    print(version)
    print("=" * 16)

    if input_filename is None:
        print("ERROR: Please specify input filename!")
        return 1

    if output_filename is None:
        output_filename_tmp = os.path.basename(input_filename)
        basename, ext = os.path.splitext(output_filename_tmp)
        if ext.lower() == '.ds':
            output_filename = basename + '.svg'
        else:
            output_filename = output_filename_tmp + '.svg'
        # current_wdir = os.path.realpath(os.getcwd())
        #
        # if script_dir == current_wdir:
        #     output_dir = os.path.join(script_dir, 'output')
        #     if not os.path.exists(output_dir):
        #         os.makedirs(output_dir)
        #     output_filename = os.path.join(output_dir, output_filename)

    print("Input ds filename: " + input_filename)
    print("Output file set to " + output_filename)
    print("=" * 16)
    print("Reading ds project file...")

    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            ds = json.load(f)
        if not isinstance(ds, list):
            ds = [ds]
    except FileNotFoundError:
        print("ERROR: Input file not found: " + input_filename)
        return 2

    print("Parsing notes and phonemes...")
    segments = [parse_segment(s) for s in ds]
    track = Track(segments=segments)

    print("Visualizing ds project...")
    visualize_track(track, output_filename,
                    color_f0=color_f0,
                    color_body=color_body,
                    color_head=color_head,
                    color_text=color_text,
                    figsize=figsize,
                    dpi=dpi,
                    aspect=aspect,
                    font_name=font_name,
                    font_size=font_size,
                    font_style=font_style,
                    display_f0=display_f0)
    print("Saved visualization to " + output_filename)
    return 0


if __name__ == '__main__':
    sys.exit(main())
