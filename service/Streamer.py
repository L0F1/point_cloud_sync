import pyrealsense2 as rs
import numpy as np
import cv2

from service import BagReader


class Streamer:

    def __init__(self, reader: BagReader):
        self.reader = reader

    def start_streaming(self, config, detection_alg, in_one_window=False, feature_detection=True):
        self.start(config)
        first_frame = True

        try:
            while True:
                # Wait for a coherent pair of frames: depth and color
                frames = self.wait_for_frames()
                depth_frame = frames.get_depth_frame()
                color_frame = frames.get_color_frame()
                if not depth_frame or not color_frame:
                    continue

                # Convert images to numpy arrays
                depth_image = np.asanyarray(depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())

                # if first_frame:
                #     with open("depth_image.txt", "w") as f:
                #         # for row in depth_image:
                #         np.savetxt(f, depth_image)
                #     first_frame = False

                # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.1), cv2.COLORMAP_JET)
                if feature_detection:
                    color_image = detection_alg(color_image)

                if in_one_window:
                    display_in_one_window(color_image, depth_colormap)
                else:
                    # Show images
                    cv2.namedWindow('RealSense_color', cv2.WINDOW_AUTOSIZE)
                    cv2.imshow('RealSense_color', depth_colormap)
                    cv2.namedWindow('RealSense_depth', cv2.WINDOW_AUTOSIZE)
                    cv2.imshow('RealSense_depth', color_image)
                    cv2.waitKey(1)

        finally:
            # Stop streaming
            self.stop()