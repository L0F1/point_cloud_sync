from service import BagReader
from utils import start_streaming
import feature_detection as fd


if __name__ == "__main__":
    reader = BagReader("C:\\Users\\trien\\Desktop\\bags\\dynamic_box_camera_1_hw_sync_master.bag")
    pipeline, config = reader.read_bag_file()
    start_streaming(pipeline, config, fd.orb_detection_show)
