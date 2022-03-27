import numpy as np
import feature_detection as fd
from entity import Stream
from service import BagReader
import cv2


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


def match_streams(streams: [Stream]):
    for s in streams:
        s.get_pipeline().start(s.get_config())

    try:
        while True:
            matched_img = fd.match_features(*get_color_images(streams))

            # Show images
            cv2.namedWindow('RealSense_color', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense_color', matched_img)
            cv2.waitKey(0)
    finally:
        # Stop streaming
        for s in streams:
            s.get_pipeline().stop()


if __name__ == "__main__":
    stream_1 = BagReader("C:\\Users\\trien\\Desktop\\bags\\dynamic_box_camera_1.bag").read_bag_file()
    stream_2 = BagReader("C:\\Users\\trien\\Desktop\\bags\\dynamic_box_camera_2.bag").read_bag_file()

    match_streams([stream_1, stream_2])
