# -*- coding: utf-8 -*-
import collections
from itertools import chain, islice


def take(n, iterable):
    """Return first n items of the iterable as a list"""
    return list(islice(iterable, n))


def prepend(value, iterator):
    """Prepend a single value in front of an iterator"""
    # prepend(1, [2, 3, 4]) -> 1 2 3 4
    return chain([value], iterator)


def tail(n, iterable):
    """"Return an iterator over the last n items"""
    # tail(3, 'ABCDEFG') --> E F G
    return iter(collections.deque(iterable, maxlen=n))
