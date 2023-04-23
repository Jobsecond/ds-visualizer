# -*- coding: utf-8 -*-
import re


def convert_color_str(s):
    s1 = s.strip().lower()
    if re.match(r'^[0-9a-zA-Z]{6}$', s1, re.IGNORECASE):
        new_s = '#{}'.format(s1)
        return new_s
    return s
