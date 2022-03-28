import pyrealsense2 as rs
from entity import Stream
from service.StreamSupplier import StreamSupplier


class BagReader(StreamSupplier):

    def __init__(self, paths: [str], resolution=None, fps=30):
        super(BagReader, self).__init__(resolution, fps)
        self.__paths = paths

    def get_streams(self):
        streams = []

        for path in self.__paths:
            pipeline = rs.pipeline()
            config = rs.config()

            rs.config.enable_device_from_file(config, path)

            config.enable_stream(rs.stream.depth, *self._resolution, rs.format.z16, self._fps)
            config.enable_stream(rs.stream.color, *self._resolution, rs.format.bgr8, self._fps)

            streams.append(Stream(pipeline, config))

        return streams
