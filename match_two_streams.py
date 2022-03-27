import numpy as np
import feature_detection as fd
from read_bag_stream import read_bag_file
import cv2


def match_streams(pipeline1, config1, pipeline2, config2):
    pipeline1.start(config1)
    pipeline2.start(config2)

    try:
        while True:
            # Wait for a coherent pair of frames: depth and color
            frames1 = pipeline1.wait_for_frames()
            frames2 = pipeline2.wait_for_frames()
            color_frame1 = frames1.get_color_frame()
            color_frame2 = frames2.get_color_frame()
            #if not color_frame1 or not color_frame2:
            #    continue

            color_image1 = np.asanyarray(color_frame1.get_data())
            color_image2 = np.asanyarray(color_frame2.get_data())
            color_image1 = cv2.resize(color_image1, (640, 480))
            color_image2 = cv2.resize(color_image2, (640, 480))
            matched_img = fd.match_features(color_image1, color_image2)

            # Show images
            cv2.namedWindow('RealSense_color', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense_color', matched_img)
            cv2.waitKey(0)
    finally:
        # Stop streaming
        pipeline1.stop()
        pipeline2.stop()


if __name__ == "__main__":
    pipeline1, config1 = read_bag_file("C:\\Users\\trien\\Desktop\\bags\\dynamic_box_camera_1.bag")
    pipeline2, config2 = read_bag_file("C:\\Users\\trien\\Desktop\\bags\\dynamic_box_camera_2.bag")

    match_streams(pipeline1, config1, pipeline2, config2)