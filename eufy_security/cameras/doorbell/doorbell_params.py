from eufy_security.params import CameraParameters


class DoorbellParameters(CameraParameters):
    def __init__(self):
        super().__init__()

        self.device_type = 7

        self.battery_level = 1101

        self.open_device = 99904
        self.status_led = 1716
        self.auto_night_vision = 1013
        self.watermark = 1214 ##TODO: This takes different values than the indoor cam Q_Q   1 == Off, 2 == On

        self.motion_detection_switch = 1011
        self.activity_zones = 1204
        self.motion_detection_type = 1252 ##2 = all motion, 0 == humans only
        self.motion_detection_sensitivity = 1276

        self.power_manager_mode = 1246 ##3 = Optimal battery life, 1 = optimal surveillance, 2 = customize recording

        self.custom_recording_clip_length = 1249
        self.custom_recording_retrigger_interval = 1250
        self.custom_recording_end_clip_early = 1251 ## 0 == yes, 1 == no

        self.wdr_enabled = 1704
        self.stream_quality = 1705 ##with high encoding -> 5 = auto, 6 = low, 7 = medium, 8 = high
                                   ##with low encoding -> 0 = auto, 1 = low, 2 = medium, 3 = high
                                   ##changing encoding quality also changes the "smart displays" option

        self.audio_recording = 1288 ##1 == off, 0 == on
        self.doorbell_audio_volume = 1230
        self.doorbell_ringtone_volume = 1708

        self.notification_settings = 1710
        self.notification_doorbell_ring = None ##This is in a json object in the above param
        self.notification_motion_detect = None ##This is in a json object in the above param
        self.notification_content_extension = None ##This is in a json object in the above param 1 = most efficient, 2 = include thumbnail, 3 = full effect

        self.opening_notif_jump_to = 2038 ##2 = live view, 1 = related history event

        ##Tones don't change in the API

        self.homebase_alert = 1702
        self.homebase_ringtone_volume = 1717 ##max appears to be 26
        self.homebase_tone = 1718