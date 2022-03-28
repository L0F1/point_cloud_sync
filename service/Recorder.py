import pyrealsense2 as rs
from pathlib import Path


class Recorder:
    default_path = Path(__file__).parent.parent.__str__()



    def find_cameras(self, ctx):
        devices = ctx.devices

        data = {}

        for dev in devices:
            name = dev.get_info(rs.camera_info.name)
            serial_number = dev.get_info(rs.camera_info.serial_number)

            data[name] = serial_number
            print(f"found camera with name: {name} and serial number: {serial_number}")

        return data

