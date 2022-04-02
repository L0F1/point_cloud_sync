import pyrealsense2 as rs
from entity import Stream
from service.StreamSupplier import StreamSupplier


class BagReader(StreamSupplier):

    def __init__(self, paths: [str]):
        self.__paths = paths

    def get_streams(self, record=None, path=None):
        streams = []

        for p in self.__paths:
            pipeline = rs.pipeline()
            config = rs.config()
            rs.config.enable_device_from_file(config, p)
            streams.append(Stream(pipeline, config))

        return streams
