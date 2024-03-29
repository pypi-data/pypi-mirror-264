import logging
import sys

loggers = {}
class Logger():
    def __init__(self, name, level):
        """
            Logger class

            Args:
                name (str): Name of the logger
                level (str): Log level
        """
        handler1 = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('WillowDb - %(levelname)s - %(name)-3s: %(message)s')
        handler1.setFormatter(formatter)
        if loggers.get(name):
            self.logger = loggers.get(name)
        else:
            self.logger = logging.getLogger(name)
            self.logger.addHandler(handler1)
            self.logger.propagate = False
            loggers[name] = self.logger

    def info(self, message):
        """
            Log info message

            Args:
                message (str): Message to log
        """
        self.logger.info(message)

    def debug(self, message):
        """
            Log debug message

            Args:
                message (str): Message to log
        """
        self.logger.debug(message)

    def error(self, message):
        """
            Log error message

            Args:
                message (str): Message to log
        """
        self.logger.error(message)

    def warning(self, message):
        """
            Log warning message
            
            Args:
                message (str): Message to log
        """
        self.logger.warning(message)

    def exception(self, message):
        """
            Log exception message

            Args:
                message (str): Message to log
        """
        self.logger.exception(message)