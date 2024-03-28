from looqbox_commons.src.main.logger.logger_interface import LoggerInterface
from looqbox_commons.src.main.logger.logger import RootLogger

class PythonPackageLogger(LoggerInterface):
    logger = RootLogger().get_new_logger("python_package")

    def get_logger(self):
        return self.logger

class ResponseLogger(LoggerInterface):
    logger = RootLogger().get_new_logger("response")
    def _get_logger(self):
        return self.logger

    @property
    def __call__(self):
        return self._get_logger()