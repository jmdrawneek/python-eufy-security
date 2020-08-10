from enum import Enum


class RecordingVideoQuality(Enum):
    TEN_EIGHTY_P = 2,
    TWO_K = 3

class StreamQuality(Enum):
    AUTO = 0
    HIGH = 3
    MEDIUM = 2
    LOW = 1