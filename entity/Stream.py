class Stream:

    def __init__(self, pipeline, config):
        self.__pipeline = pipeline
        self.__config = config

    def get_pipeline(self):
        return self.__pipeline

    def get_config(self):
        return self.__config
