#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import argparse
import sys
from dataclasses import asdict

from core.models import *
from core.parsers import *


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
                                 help='output directory')

    args = argument_parser.parse_args()

    input_filename = args.input
    output_dir = args.output

    print("DiffSinger project file (.ds) converter")
    print(version)
    print("=" * 16)

    if input_filename is None:
        print("ERROR: Please specify input filename!")
        return 1

    if output_dir is None:
        print("ERROR: Please specify output directory!")
        return 1

    print("Input ds filename: " + input_filename)
    print("Output directory set to " + output_dir)
    print("=" * 16)
    print("Reading ds project file...")

    input_filename_base = os.path.basename(input_filename)

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
    os.makedirs(output_dir, exist_ok=True)
    for i, segment in enumerate(segments):
        out_json = json.dumps(asdict(segment), indent=2)
        with open(os.path.join(output_dir, "{}_{}.json".format(input_filename_base, i)), "w") as f:
            f.write(out_json)

    return 0


if __name__ == '__main__':
    sys.exit(main())
