from enum import Enum


class RecordingVideoQuality(Enum):
    TEN_EIGHTY_P = 2,
    TWO_K = 3


class StreamQuality(Enum):
    AUTO = 0
    HIGH = 3
    MEDIUM = 2
    LOW = 1


class ContinuousRecordingType(Enum):
    TWENTY_FOUR_SEVEN = 0
    SCHEDULE = 1


class WaterMark(Enum):
    OFF = 2
    TIMESTAMP = 0
    TIMESTAMP_AND_LOGO = 1
