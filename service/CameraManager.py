import logging
import pyrealsense2 as rs
from entity import Stream
from service import StreamSupplier


class CameraManager(StreamSupplier):

    def __init__(self, resolution=None, fps=30):
        super(CameraManager, self).__init__(resolution, fps)
        self.logger = logging.getLogger(__name__)

    def get_streams(self):
        streams = []
        context = rs.context()
        camera_serial_nums = self.__find_cameras(context)

        for serial_num in camera_serial_nums:
            pipeline = rs.pipeline()
            config = rs.config()
            config.enable_device(serial_num)
            config.enable_stream(rs.stream.depth, *self._resolution, rs.format.z16, self._fps)
            config.enable_stream(rs.stream.color, *self._resolution, rs.format.bgr8, self._fps)
            streams.append(Stream(pipeline, config))

        return streams

    def __find_cameras(self, ctx) -> {}:
        devices = ctx.devices

        data = {}

        for dev in devices:
            name = dev.get_info(rs.camera_info.name)
            serial_number = dev.get_info(rs.camera_info.serial_number)

            data[name] = serial_number
            self.logger.info(f"found camera with name: {name} and serial number: {serial_number}")

        return data
