import pyrealsense2 as rs
import numpy as np
import cv2
import time

#
# NOTE: it appears that imu, rgb and depth cannot all be running simultaneously.
#       Any two of those 3 are fine, but not all three: causes timeout on wait_for_frames()
#
file_path = "C:\\Users\\trien\\Desktop\\bags\\dynamic_box_camera_1.bag"
enable_imu = False
enable_rgb = True
enable_depth = True
# TODO: enable_pose
# TODO: enable_ir_stereo


if __name__ == "__main__":
    # Configure streams
    if enable_imu:
        imu_pipeline = rs.pipeline()
        imu_config = rs.config()
        if None != file_path:
            rs.config.enable_device_from_file(imu_config, file_path)

        #imu_config.enable_stream(rs.stream.accel, rs.format.motion_xyz32f, 63)  # acceleration
        #imu_config.enable_stream(rs.stream.gyro, rs.format.motion_xyz32f, 200)  # gyroscope
        imu_profile = imu_pipeline.start(imu_config)

    if enable_depth or enable_rgb:
        pipeline = rs.pipeline()
        config = rs.config()

        # if we are provided with a specific device, then enable it
        if None != file_path:
            rs.config.enable_device_from_file(config, file_path)

        #if enable_depth:
            #config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 60)  # depth

        #if enable_rgb:
            #config.enable_stream(rs.stream.color, 424, 240, rs.format.bgr8, 60)  # rgb

        # Start streaming
        profile = pipeline.start(config)

        # Getting the depth sensor's depth scale (see rs-align example for explanation)
        if enable_depth:
            depth_sensor = profile.get_device().first_depth_sensor()
            depth_scale = depth_sensor.get_depth_scale()
            print("Depth Scale is: ", depth_scale)
            if enable_depth:
                # Create an align object
                # rs.align allows us to perform alignment of depth frames to others frames
                # The "align_to" is the stream type to which we plan to align depth frames.
                align_to = rs.stream.color
                align = rs.align(align_to)

    try:
        frame_count = 0
        start_time = time.time()
        frame_time = start_time
        while True:
            last_time = frame_time
            frame_time = time.time() - start_time
            frame_count += 1

            #
            # get the frames
            #
            if enable_rgb or enable_depth:
                frames = pipeline.wait_for_frames(
                    200 if (frame_count > 1) else 10000)  # wait 10 seconds for first frame

            if enable_imu:
                imu_frames = imu_pipeline.wait_for_frames(200 if (frame_count > 1) else 10000)

            if enable_rgb or enable_depth:
                # Align the depth frame to color frame
                aligned_frames = align.process(frames) if enable_depth and enable_rgb else None
                depth_frame = aligned_frames.get_depth_frame() if aligned_frames is not None else frames.get_depth_frame()
                color_frame = aligned_frames.get_color_frame() if aligned_frames is not None else frames.get_color_frame()

                # Convert images to numpy arrays
                depth_image = np.asanyarray(depth_frame.get_data()) if enable_depth else None
                color_image = np.asanyarray(color_frame.get_data()) if enable_rgb else None

                # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03),
                                                   cv2.COLORMAP_JET) if enable_depth else None

                # Stack both images horizontally
                images = None
                if enable_rgb:
                    images = np.hstack((color_image, depth_colormap)) if enable_depth else color_image
                elif enable_depth:
                    images = depth_colormap

                # Show images
                cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
                if images is not None:
                    cv2.imshow('RealSense', images)

            if enable_imu:
                accel_frame = imu_frames.first_or_default(rs.stream.accel, rs.format.motion_xyz32f)
                gyro_frame = imu_frames.first_or_default(rs.stream.gyro, rs.format.motion_xyz32f)
                print("imu frame {} in {} seconds: \n\taccel = {}, \n\tgyro = {}".format(str(frame_count),
                                                                                         str(frame_time - last_time),
                                                                                         str(accel_frame.as_motion_frame().get_motion_data()),
                                                                                         str(gyro_frame.as_motion_frame().get_motion_data())))

            # Press esc or 'q' to close the image window
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q') or key == 27:
                cv2.destroyAllWindows()
                break

    finally:
        # Stop streaming
        pipeline.stop()
