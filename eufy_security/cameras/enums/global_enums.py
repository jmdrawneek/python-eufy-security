from enum import Enum


class BaseEnum(Enum):
    NONE = -1


class GlobalSwitch(BaseEnum):
    ON = 1
    OFF = 0


class GlobalFlippedSwitch(BaseEnum):
    ON = 0
    OFF = 1
