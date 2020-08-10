from enum import Enum

class Switch(Enum):
    ON = 1
    OFF = 0

"""
Both types returning same value, needs investigation
"""
class TimeFormat(Enum):
    TWENTY_FOUR_HOURS = 0
    TWELVE_HOURS = 0