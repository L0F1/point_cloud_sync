import pyrealsense2 as rs
import numpy as np
import cv2


def find_cameras(ctx):
    devices = ctx.devices

    data = {}

    for dev in devices:
        name = dev.get_info(rs.camera_info.name)
        serial_number = dev.get_info(rs.camera_info.serial_number)

        data[name] = serial_number
        print(f"found camera with name: {name} and serial number: {serial_number}")

    return data


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


def start_streaming(pipeline, config, detection_alg, in_one_window=False, feature_detection=True):
    pipeline.start(config)
    first_frame = True

    try:
        while True:
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
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
        pipeline.stop()