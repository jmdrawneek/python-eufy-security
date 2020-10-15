from eufy_security.cameras.enums.global_enums import *


class Switch(GlobalSwitch):
    pass


"""
Both types returning same value, needs investigation
"""


class TimeFormat(BaseEnum):
    TWENTY_FOUR_HOURS = 0
    TWELVE_HOURS = 0


class MotionDetectionMode(BaseEnum):
    PERSON = 1
    PET = 2
    PERSON_AND_PET = 3
    OTHER = 4
    PERSON_AND_OTHER = 5
    PET_AND_OTHER = 6
    PERSON_AND_PET_AND_OTHER = 7


class MotionDetectionSensitivity(BaseEnum):
    LOWEST = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    HIGHEST = 5


class SoundDetectionMode(BaseEnum):
    ALL_SOUND = 2
    CRYING = 1


class SoundDetectionSensitivity(BaseEnum):
    LOWEST = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    HIGHEST = 5


class NotificationExtensions(BaseEnum):
    MOST_EFFICIENT = 1
    FULL_EFFECT = 3
    INCLUDE_THUMBNAIL = 2


class RecordingVideoQuality(BaseEnum):
    TEN_EIGHTY_P = 2,
    TWO_K = 3


class StreamQuality(BaseEnum):
    AUTO = 0
    HIGH = 3
    MEDIUM = 2
    LOW = 1


class ContinuousRecordingType(BaseEnum):
    TWENTY_FOUR_SEVEN = 0
    SCHEDULE = 1


class WaterMark(BaseEnum):
    OFF = 2
    TIMESTAMP = 0
    TIMESTAMP_AND_LOGO = 1
