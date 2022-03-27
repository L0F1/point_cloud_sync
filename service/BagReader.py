import pyrealsense2 as rs
from entity import Stream


class BagReader:
    __resolution = [1280, 720]
    __fps = 30

    def __init__(self, file: str):
        self.__file = file

    def read_bag_file(self) -> Stream:
        pipeline = rs.pipeline()
        config = rs.config()

        rs.config.enable_device_from_file(config, self.__file)

        config.enable_stream(rs.stream.depth, *BagReader.__resolution, rs.format.z16, BagReader.__fps)
        config.enable_stream(rs.stream.color, *BagReader.__resolution, rs.format.bgr8, BagReader.__fps)

        return Stream(pipeline, config)

    def set_resolution(self, resolution: []):
        self.__resolution = resolution

    def set_fps(self, fps: int):
        self.__fps: fps
