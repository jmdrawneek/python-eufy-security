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
