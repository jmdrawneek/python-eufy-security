from enum import Enum


class DetectionMode(Enum):
    PERSON = 1
    PET = 2
    PERSON_AND_PET = 3
    OTHER = 4
    PERSON_AND_OTHER = 5
    PET_AND_OTHER = 6
    PERSON_AND_PET_AND_OTHER = 7


class DetectionSensitivity(Enum):
    LOWEST = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    HIGHEST = 5