import logging
import feature_detection as fd
from threading import Thread
from typing import Callable, Any
from entity import Stream
from service import StreamSupplier
import numpy as np
import cv2


def display_in_one_window(color_image, depth_colormap):
    depth_colormap_dim = depth_colormap.shape
    color_colormap_dim = color_image.shape

    # If depth and color resolutions are different, resize color image to match depth image for display
    if depth_colormap_dim != color_colormap_dim:
        resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]),
                                         interpolation=cv2.INTER_AREA)
        images = np.hstack((resized_color_image, depth_colormap))
    else:
        images = np.hstack((color_image, depth_colormap))

    cv2.namedWindow('RealSense_color', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('RealSense', images)


def get_color_images(streams: [Stream]):
    color_images = []

    for s in streams:
        # Wait for a coherent pair of frames: depth and color
        frames = s.get_pipeline().wait_for_frames()
        color_frame = frames.get_color_frame()

        # if not color_frame1 or not color_frame2:
        #    continue

        color_image = np.asanyarray(color_frame.get_data())
        color_image = cv2.resize(color_image, (640, 480))
        color_images.append(color_image)

    return color_images


def start_pipelines(streams: [Stream]):
    for s in streams:
        s.get_pipeline().start(s.get_config())


# что должен делать:
# читать pipeline
# стримить поток
# стримить несколько потоков
# принимать matcher и стримить сматченное изображение

class Streamer:

    def __init__(self, supplier: StreamSupplier, algorithm: Callable[[Any], None], window_size, record: bool, path):
        self.logger = logging.getLogger(__name__)
        self.__supplier = supplier
        self.__algorithm = algorithm
        self.__window_size = window_size
        self.__record = record
        self.__path = path

    def start_streaming(self, in_one_window=False, feature_detection=True):
        streams = self.__get_streams()
        for s in streams:
            Thread(target=self.__stream, args=(s, in_one_window, feature_detection)).start()

    def match_two_streams(self):
        streams = self.__get_streams()

        if len(streams) != 2:
            self.logger.error("There should be two streams for matching")
            return

        start_pipelines(streams)
        for s in streams:
            try:
                while True:
                    matched_img = fd.match_features(*get_color_images(streams))

                    # Show images
                    cv2.namedWindow('RealSense_color', cv2.WINDOW_AUTOSIZE)
                    cv2.imshow('RealSense_color', matched_img)
                    cv2.waitKey(0)
            finally:
                # Stop streaming
                s.get_pipeline().stop()

    def __stream(self, stream: Stream, in_one_window, feature_detection):
        stream.get_pipeline().start(stream.get_config())

        try:
            while True:
                # Wait for a coherent pair of frames: depth and color
                frames = stream.get_pipeline().wait_for_frames()
                depth_frame = frames.get_depth_frame()
                color_frame = frames.get_color_frame()
                if not depth_frame or not color_frame:
                    continue

                # Convert images to numpy arrays
                depth_image = np.asanyarray(depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())

                # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.1), cv2.COLORMAP_JET)

                color_image = cv2.resize(color_image, self.__window_size)
                depth_colormap = cv2.resize(depth_colormap, self.__window_size)

                if feature_detection:
                    color_image = self.__algorithm(color_image)

                if in_one_window:
                    display_in_one_window(color_image, depth_colormap)
                else:
                    # Show images
                    cv2.namedWindow(f'RealSense_color {stream}', cv2.WINDOW_AUTOSIZE)
                    cv2.imshow(f'RealSense_color {stream}', depth_colormap)
                    cv2.namedWindow(f'RealSense_depth {stream}', cv2.WINDOW_AUTOSIZE)
                    cv2.imshow(f'RealSense_depth {stream}', color_image)
                    cv2.waitKey(1)

        finally:
            # Stop streaming
            stream.get_pipeline().stop()

    def __get_streams(self) -> [Stream]:
        return self.__supplier.get_streams(self.__record, self.__path)


class StreamBuilder:

    def __init__(self):
        self.__supplier = None
        self.__algorithm = None
        self.__window_size = (1280, 720)
        self.__record = False
        self.__path = None

    def set_stream_supplier(self, supplier: StreamSupplier):
        self.__supplier = supplier
        return self

    def set_algorithm(self, algorithm: Callable[[], None]):
        self.__algorithm = algorithm
        return self

    def set_window_size(self, size: ()):
        self.__window_size = size
        return self

    def record(self, path=None):
        self.__path = path
        return self

    def build(self) -> Streamer:
        return Streamer(self.__supplier, self.__algorithm, self.__window_size, self.__record, self.__path)
