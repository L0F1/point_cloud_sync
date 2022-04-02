from entity import Stream


class StreamSupplier:
    default_resolution = [1280, 720]

    def __init__(self, resolution=None, fps=30):
        if resolution is None:
            resolution = StreamSupplier.default_resolution
        self._resolution = resolution
        self._fps = fps

    def get_streams(self, record, path) -> [Stream]:
        pass

    def set_resolution(self, resolution: []):
        self._resolution = resolution

    def set_fps(self, fps: int):
        self._fps: fps
