import time

import pyrealsense2 as rs
from utils import find_cameras


def record(output_path1, output_path2, record_time):
    context = rs.context()
    camera_serial_nums = find_cameras(context)

    #ctx = rs.context()
    dev1 = context.devices[0]
    sensor = dev1.first_depth_sensor()
    sensor.set_option(rs.option.inter_cam_sync_mode, 1.0)
    print(f"{dev1.get_info(rs.camera_info.serial_number)} is master")
    dev2 = context.devices[1]
    sensor = dev2.first_depth_sensor()
    sensor.set_option(rs.option.inter_cam_sync_mode, 2.0)
    print(f"{dev2.get_info(rs.camera_info.serial_number)} is slave")

    # base_path = '/'.join(output_path.split("/")[:-1])
    # file_name = output_path.split("/")[-1]

    # Configure depth and color streams...
    # ...from Camera 1
    pipeline_1 = rs.pipeline()
    config_1 = rs.config()
    config_1.enable_device(camera_serial_nums[0])
    config_1.enable_record_to_file(output_path1)
    config_1.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    config_1.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
    # ...from Camera 2
    pipeline_2 = rs.pipeline()
    config_2 = rs.config()
    config_2.enable_device(camera_serial_nums[1])
    config_2.enable_record_to_file(output_path2)
    config_2.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    config_2.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

    # Start streaming from both cameras
    camera_1_profile = pipeline_1.start(config_1)
    camera_2_profile = pipeline_2.start(config_2)

    # camera_1_sensor = camera_1_profile.get_device().first_depth_sensor()
    # camera_1_sensor.set_option(rs.option.inter_cam_sync_mode, 1)
    #
    # camera_2_sensor = camera_2_profile.get_device().first_depth_sensor()
    # camera_2_sensor.set_option(rs.option.inter_cam_sync_mode, 2)

    time.sleep(record_time)

    pipeline_1.stop()
    pipeline_2.stop()

    del pipeline_1
    del pipeline_2

    del config_1
    del config_2


if __name__ == "__main__":
    record("C:\\Users\\trien\\Desktop\\bags\\dynamic_box_camera_1_hw_sync_master.bag",
           "C:\\Users\\trien\\Desktop\\bags\\dynamic_box_camera_2_hw_sync_slave.bag", 7)
