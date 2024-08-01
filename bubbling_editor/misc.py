from collections import namedtuple
from enum import Enum


class Kind(int, Enum):
    REGULAR = 1
    COUNTER = 2


AddBubblePayload = namedtuple('AddBubblePayload',
                              ['pos', 'radius', 'kind'],
                              defaults=[Kind.REGULAR])
