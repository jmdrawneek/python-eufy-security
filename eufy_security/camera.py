"""Define a Eufy camera object."""
import logging
from typing import TYPE_CHECKING
import datetime

from .cameras.indoor_cam import IndoorCamParameters
from .params import ParamType, CameraParameters

if TYPE_CHECKING:
    from .api import API  # pylint: disable=cyclic-import

_LOGGER: logging.Logger = logging.getLogger(__name__)


def get_camera_params_from_device_type(device_type):
    if device_type == 30:
        return IndoorCamParameters()

    return CameraParameters()


class Camera:
    """Define the camera object."""

    def __init__(self, api: "API", camera_info: dict) -> None:
        """Initialize."""
        self._api = api
        self.camera_info: dict = camera_info
        self.camera_parameters = get_camera_params_from_device_type(camera_info['device_type'])

    @property
    def hardware_version(self) -> str:
        """Return the camera's hardware version."""
        return self.camera_info["main_hw_version"]

    @property
    def last_camera_image_url(self) -> str:
        """Return the URL to the latest camera thumbnail."""
        return self.camera_info["cover_path"]

    @property
    def mac(self) -> str:
        """Return the camera MAC address."""
        return self.camera_info["wifi_mac"]

    @property
    def model(self) -> str:
        """Return the camera's model."""
        return self.camera_info["device_model"]

    @property
    def name(self) -> str:
        """Return the camera name."""
        return self.camera_info["device_name"]

    @property
    def device_type(self) -> int:
        """Return the camera's device type"""
        return self.camera_info["device_type"]

    @property
    def params(self) -> dict:
        """Return camera parameters."""
        params = {}
        for param in self.camera_info["params"]:
            param_type = param["param_type"]
            value = param["param_value"]

            try:
                for param_name in self.camera_parameters.__dict__.keys():
                    param_value = self.camera_parameters.__dict__.get(param_name)

                    if param_value == param_type:
                        param_type = param_name
                        value = self.camera_parameters.read_value(param_value, value)
            except ValueError as e:
                _LOGGER.debug('Unable to process parameter "%s", value "%s"', param_type, value)

            params[param_type] = value
        return params

    @property
    def serial(self) -> str:
        """Return the camera serial number."""
        return self.camera_info["device_sn"]

    @property
    def software_version(self) -> str:
        """Return the camera's software version."""
        return self.camera_info["main_sw_version"]

    @property
    def station_serial(self) -> str:
        """Return the camera's station serial number."""
        return self.camera_info["station_sn"]

    async def async_set_params(self, params: dict) -> None:
        """Set camera parameters."""
        serialized_params = []
        for param_type, value in params.items():
            value = self.camera_parameters.write_value(param_type, value)
            serialized_params.append({"param_type": param_type, "param_value": value})
        await self._api.request(
            "post",
            "app/upload_devs_params",
            json={
                "device_sn": self.serial,
                "station_sn": self.station_serial,
                "params": serialized_params,
            },
        )
        await self.async_update()

    async def async_status_led_on(self):
        """Turn Status LED ON"""
        await self.async_set_params({self.camera_parameters.status_led: 1})

    async def async_status_led_off(self):
        """Turn Status LED OFF"""
        await self.async_set_params({self.camera_parameters.status_led: 0})

    async def async_turn_camera_off(self):
        """Turn Camera OFF"""
        await self.async_set_params({self.camera_parameters.open_device: False})

    async def async_turn_camera_on(self):
        """Turn Camera ON"""
        await self.async_set_params({self.camera_parameters.open_device: True})

    async def async_start_motion_detection(self):
        """Turn camera's motion detection ON."""
        await self.async_set_params({self.camera_parameters.motion_detection_switch: 1})

    async def async_stop_motion_detection(self):
        """Turn camera's motion detection OFF."""
        await self.async_set_params({self.camera_parameters.motion_detection_switch: 0})

    async def async_set_motion_detection_mode(self, mode):
        """Set motion detection mode. use detection.MotionDetectionMode"""
        await self.async_set_params({self.camera_parameters.motion_detection_type: mode.value})

    async def async_set_motion_detection_sensitivity(self, sensitivity):
        """Set motion detection sensitivity. use detection.MotionDetectionSensitivity"""
        await self.async_set_params({self.camera_parameters.motion_detection_sensitivity: sensitivity.value})

    async def async_start_sound_detection(self):
        """Turn camera's sound detection ON"""
        await self.async_set_params({self.camera_parameters.sound_detection_switch: 1})

    async def async_stop_sound_detection(self):
        """Turn camera's sound detection OFF"""
        await self.async_set_params({self.camera_parameters.sound_detection_switch: 0})

    async def async_set_sound_detection_mode(self, mode):
        """Set sound detection mode. use detection.SoundDetectionMode"""
        await self.async_set_params({self.camera_parameters.sound_detection_type: mode.value})

    async def async_set_sound_detection_sensitivity(self, sensitivity):
        """Set sound detection sensitivity. use detection.SoundDetectionSensitivity"""
        await self.async_set_params({self.camera_parameters.sound_detection_sensitivity: sensitivity.value})

    async def async_set_snooze_off(self):
        """Turn notification snooze OFF"""
        await self.async_set_params({self.camera_parameters.snooze_mode: None})

    async def async_set_snooze_for(self, seconds_to_snooze):
        """Turn snooze on for x seconds"""
        await self.async_set_params({self.camera_parameters.snoozed_at: int(datetime.datetime.now().timestamp())})
        await self.async_set_params({self.camera_parameters.snooze_mode: {"account_id": self._api.user_id, "snooze_time": seconds_to_snooze}})

    async def async_set_recording_video_quality(self, recording_video_quality):
        """Set recording video quality"""
        await self.async_set_params({self.camera_parameters.recording_quality: recording_video_quality.value})

    async def async_set_streaming_video_quality(self, streaming_video_quality):
        """Set streaming quality"""
        await self.async_set_params({self.camera_parameters.stream_quality: streaming_video_quality.value})

    async def async_turn_microphone_on(self):
        """Turn the device microphone ON"""
        await self.async_set_params({self.camera_parameters.microphone_switch: 1})

    async def async_turn_microphone_off(self):
        """Turn the device microphone OFF"""
        await self.async_set_params({self.camera_parameters.microphone_switch: 0})

    async def async_turn_audio_recording_on(self):
        """Turn the device audio recording ON"""
        await self.async_set_params({self.camera_parameters.audio_recording: 1})

    async def async_turn_audio_recording_off(self):
        """Turn the device audio recording OFF"""
        await self.async_set_params({self.camera_parameters.audio_recording: 0})

    async def async_turn_speaker_on(self):
        """Turn the device speaker ON"""
        await self.async_set_params({self.camera_parameters.speaker_switch: 1})

    async def async_turn_speaker_off(self):
        """Turn the device speaker OFF"""
        await self.async_set_params({self.camera_parameters.speaker_switch: 0})

    async def async_set_speaker_volume(self, volume):
        """Set the volume of the device speaker"""
        await self.async_set_params({self.camera_parameters.speaker_volume: volume})

    async def async_set_continuous_recording_on(self):
        """Turn continuous recording ON"""
        await self.async_set_params({self.camera_parameters.continuous_recording_switch: 1})

    async def async_set_continuous_recording_off(self):
        """Turn continuous recording OFF"""
        await self.async_set_params({self.camera_parameters.continuous_recording_switch: 0})

    async def async_set_continuous_recording_type(self, recording_type):
        """Set the type of continuous recording"""
        await self.async_set_params({self.camera_parameters.continuous_recording_type: recording_type.value})

    async def async_set_pet_command_on(self):
        """Turn the Pet Command feature ON"""
        await self.async_set_params({self.camera_parameters.pet_command: 1})

    async def async_set_pet_command_off(self):
        """Turn the Pet Command feature OFF"""
        await self.async_set_params({self.camera_parameters.pet_command: 0})

    async def async_set_pet_command_auto_respond(self, value):
        """Set the Pet Command auto respond, not sure yet how to GET the values that you set in the EufySecurity app"""
        await self.async_set_params({self.camera_parameters.pet_command_auto_respond: value})

    async def async_remove_all_activity_zones(self):
        """Remove all activity zones from camera"""
        await self.async_set_params({self.camera_parameters.activity_zones: {"polygens":[], "zonecount": 0}})

    async def async_set_activity_zones(self, activity_zones):
        """Set the activity zones to that sent in the parameter
        Not much we can do for user input so that should be handled by the program using this API.
        sample data json:
        {"polygens":[
            {"isDetectZone":true,
            "isEditable":false,
            "isSaved":true,
            "points":[
                {"x":293,"y":110},{"x":419,"y":110},{"x":482,"y":218},{"x":419,"y":326},{"x":293,"y":326},{"x":230,"y":218}
            ]}
        ]
        ,"zonecount":1}

        on my indoor cam 2k, oneplus 6t, the zones coords went y:0-432, x:0-768, we need to check if they're universal
        """
        await self.async_set_params({self.camera_parameters.activity_zones: activity_zones})

    async def async_set_watermark(self, watermark):
        """Set the watermark type"""
        await self.async_set_params({self.camera_parameters.watermark: watermark.value})

    async def async_set_person_notification_switch(self, state):
        """Set the person notification to ON/OFF"""
        await self.async_set_params({self.camera_parameters.person_notification: state.value})

    async def async_set_pet_notification_switch(self, state):
        """Set the pet notification to ON/OFF"""
        await self.async_set_params({self.camera_parameters.pet_notification: state.value})

    async def async_set_other_motion_notification_switch(self, state):
        """Set the other motion notification to ON/OFF"""
        await self.async_set_params({self.camera_parameters.other_motion_notification: state.value})

    async def async_set_crying_notification_switch(self, state):
        """Set the crying notification to ON/OFF"""
        await self.async_set_params({self.camera_parameters.crying_notification: state.value})

    async def async_set_other_sound_notification_switch(self, state):
        """Set the all sound notification to ON/OFF"""
        await self.async_set_params({self.camera_parameters.all_sound_notification: state.value})

    async def async_set_notification_interval(self, seconds):
        """Set the notification interval
        The EufySecurity app shows the minimum section that was reached. e.g if you set 1m30s (90s) it will select the 1 minute option.
        Anything greater than 5m shows as 5m, anything less than 1m shows as 0 in app.
        """
        await self.async_set_params({self.camera_parameters.notification_interval: seconds})

    async def async_set_notification_extension(self, type):
        """Set the type of notification extensions to use"""
        await self.async_set_params({self.camera_parameters.notification_content_extension: type.value})

    async def async_set_rotate_image_180(self, state):
        """Set whether to rotate the image 180 or not"""
        await self.async_set_params({self.camera_parameters.rotate_image_180: state.value})

    async def async_set_auto_night_vision_switch(self, state):
        """Turn auto night vision ON/OFF"""
        await self.async_set_params({self.camera_parameters.auto_night_vision: state.value})

    async def async_start_stream(self) -> str:
        """Start the camera stream and return the RTSP URL."""
        start_resp = await self._api.request(
            "post",
            "web/equipment/start_stream",
            json={
                "device_sn": self.serial,
                "station_sn": self.station_serial,
                "proto": 2,
            },
        )

        return start_resp["data"]["url"]

    async def async_stop_stream(self) -> None:
        """Stop the camera stream."""
        await self._api.request(
            "post",
            "web/equipment/stop_stream",
            json={
                "device_sn": self.serial,
                "station_sn": self.station_serial,
                "proto": 2,
            },
        )

    async def async_update(self) -> None:
        """Get the latest values for the camera's properties."""
        await self._api.async_update_device_info()
