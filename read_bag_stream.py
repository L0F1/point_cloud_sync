from service import BagReader, StreamBuilder
import feature_detection as fd


if __name__ == "__main__":
    reader = BagReader(["C:\\Users\\trien\\Desktop\\bags\\dynamic_box_camera_1.bag",
                        "C:\\Users\\trien\\Desktop\\bags\\dynamic_box_camera_2.bag"])
    StreamBuilder()\
        .set_stream_supplier(reader)\
        .set_algorithm(fd.surf_detection)\
        .build()\
        .start_streaming()
