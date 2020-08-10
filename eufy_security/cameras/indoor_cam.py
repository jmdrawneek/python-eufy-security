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

        self.recording_quality = 2034
        self.stream_quality = 2031

        self.microphone_switch = 1240
        self.audio_recording = 6012
        self.speaker_switch = 1241
        self.speaker_volume = 1230

        self.continuous_recording_switch = 6010
        self.continuous_recording_type = 6011

        self.snoozed_at = 2037
        self.snooze_mode = 1271
