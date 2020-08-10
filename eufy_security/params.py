"""Define parameters that can be sent to the base station."""
import base64
from enum import Enum
import json
import abc

"""Device Types:
30 - Indoor Camera 2k (non-pan-tilt)

This class will represent parameter types for different cameras.

To create a camera with customisable parameters, extend this class and override the values that can be changed
on that device
"""

class CameraParameters():
    def __init__(self):
        self.device_type = None

        self.status_led = None
        self.open_device = None
        self.watermark = None
        self.auto_night_vision = None

        self.motion_detection_switch = None
        self.motion_detection_type = None
        self.motion_detection_sensitivity = None
        self.motion_detection_zone = None

        self.sound_detection_switch = None
        self.sound_detection_type = None
        self.sound_detection_sensitivity = None

        self.recording_quality = None
        self.stream_quality = None

        self.microphone_switch = None
        self.audio_recording = None
        self.speaker_switch = None
        self.speaker_volume = None

        self.continuous_recording_switch = None
        self.continuous_recording_type = None

        self.pet_command = None
        self.pet_command_auto_respond = None

        self.activity_zones = None

        self.person_notification = None
        self.pet_notification = None
        self.other_motion_notification = None
        self.crying_notification = None
        self.all_sound_notification = None
        self.notification_interval = None
        self.notification_content_extension = None

        self.rotate_image_180 = None

        self.time_format = None ##Right now both 24 and 12 return the same value, 0

        self.snoozed_at = None
        self.snooze_mode = None

    def read_value(self, param, value):
        """Read a parameter JSON string."""
        if value:
            if param == self.snooze_mode:
                value = base64.b64decode(value, validate=True).decode()
            return json.loads(value)
        return None

    def write_value(self, param, value):
        """Write a parameter JSON string."""
        value = json.dumps(value)
        if param == self.snooze_mode:
            value = base64.b64encode(value.encode()).decode()
        return value


class ParamType(Enum):
    """Define the types.

    List retrieved from from com.oceanwing.battery.cam.binder.model.CameraParams
    """

    STATUS_LED = 6014

    CHIME_STATE = 2015
    DETECT_EXPOSURE = 2023
    # DETECT_MODE = 2004
    DETECT_MODE = 6045  # PERSON/PET/OTHER. See MotionDetectionMode in detection.py
    DETECT_MOTION_SENSITIVE = 2005
    DETECT_SCENARIO = 2028
    DETECT_SENSITIVITY = 6041  # Sensitivity slider (Lowest-Highest). See MotionDetectionSensitivity in detection.py
    # DETECT_SWITCH = 2027
    DETECT_SWITCH = 6040  # Turn ON/OFF
    DETECT_ZONE = 2006

    SOUND_SWITCH = 6043  # Turn ON/OFF (0 or 1)
    SOUND_SENSITIVITY = 6044  # see SoundDetectionSensitivity in detection.py
    SOUND_TYPE = 6046  # see SoundDetectionMode in detection.py

    DOORBELL_AUDIO_RECODE = 2042
    DOORBELL_BRIGHTNESS = 2032
    DOORBELL_DISTORTION = 2033
    DOORBELL_HDR = 2029
    DOORBELL_IR_MODE = 2030
    DOORBELL_LED_NIGHT_MODE = 2039
    DOORBELL_MOTION_ADVANCE_OPTION = 2041
    DOORBELL_MOTION_NOTIFICATION = 2035
    DOORBELL_NOTIFICATION_JUMP_MODE = 2038
    DOORBELL_NOTIFICATION_OPEN = 2036
    DOORBELL_RECORD_QUALITY = 2034  #
    DOORBELL_RING_RECORD = 2040
    DOORBELL_SNOOZE_START_TIME = 2037
    DOORBELL_VIDEO_QUALITY = 2031
    NIGHT_VISUAL = 2002
    OPEN_DEVICE = 2001
    RINGING_VOLUME = 2022
    SDCARD = 2010
    UN_DETECT_ZONE = 2007
    VOLUME = 2003

    # Inferred from source
    SNOOZE_MODE = 1271  # The value is base64 encoded
    WATERMARK_MODE = 1214  # 1 - hide, 2 - show
    DEVICE_UPGRADE_NOW = 1134
    CAMERA_UPGRADE_NOW = 1133

    # Set only params?
    PUSH_MSG_MODE = 1252  # 0 to ???

    def read_value(self, value):
        """Read a parameter JSON string."""
        if value:
            if self is ParamType.SNOOZE_MODE:
                value = base64.b64decode(value, validate=True).decode()
            return json.loads(value)
        return None

    def write_value(self, value):
        """Write a parameter JSON string."""
        value = json.dumps(value)
        if self is ParamType.SNOOZE_MODE:
            value = base64.b64encode(value.encode()).decode()
        return value
