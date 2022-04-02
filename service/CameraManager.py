import logging
from pathlib import Path
import pyrealsense2 as rs
from entity import Stream
from service import StreamSupplier


class CameraManager(StreamSupplier):
    default_path = Path(__file__).parent.parent.__str__()
    default_resolution = (1280, 720)

    def __init__(self, resolution=None, fps=30):
        self.logger = logging.getLogger(__name__)
        if resolution is None:
            resolution = CameraManager.default_resolution
        self.__resolution = resolution
        self.__fps = fps

    def get_streams(self, record=False, path=default_path):
        streams = []
        context = rs.context()
        camera_serial_nums = self.__find_cameras(context)

        for i, serial_num in enumerate(camera_serial_nums):
            pipeline = rs.pipeline()
            config = rs.config()
            config.enable_device(serial_num)
            config.enable_stream(rs.stream.depth, *self.__resolution, rs.format.z16, self.__fps)
            config.enable_stream(rs.stream.color, *self.__resolution, rs.format.bgr8, self.__fps)
            if record:
                config.enable_record_to_file(path + f"/camera_{i}")
            streams.append(Stream(pipeline, config))

        return streams

    def set_resolution(self, resolution: []):
        self.__resolution = resolution

    def set_fps(self, fps: int):
        self.__fps = fps

    def __find_cameras(self, ctx) -> {}:
        devices = ctx.devices

        data = {}

        for dev in devices:
            name = dev.get_info(rs.camera_info.name)
            serial_number = dev.get_info(rs.camera_info.serial_number)

            data[name] = serial_number
            self.logger.info(f"found camera with name: {name} and serial number: {serial_number}")

        return data
