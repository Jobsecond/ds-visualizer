# -*- coding: utf-8 -*-

__all__ = [
    'float_sum'
]

from typing import Iterable


def float_sum(nums: Iterable[float], /, epsilon: int = 10000) -> float:
    s = 0
    for num in nums:
        s += num * epsilon
    return s / epsilon
