from abc import ABC

from eufy_security.params import CameraParameters


class IndoorCamParameters(CameraParameters):
    def __init__(self):
        super().__init__()

        self.device_type = 30

        self.status_led = 6014
        self.open_device = 2001

        self.motion_detection_switch = 6040
        self.motion_detection_type = 6045
        self.motion_detection_sensitivity = 6041

        self.sound_detection_switch = 6043
        self.sound_detection_sensitivity = 6044
        self.sound_detection_type = 6046

        self.snoozed_at = 2037
        self.snooze_mode = 1271