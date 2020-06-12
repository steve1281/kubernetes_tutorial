from logging.handlers import RotatingFileHandler
import logging

LOG_FILENAME = 'foo.log'

class Logger():
    def __init__(self, app, logfile=LOG_FILENAME):
        self.app = app
        self.app.logger.addHandler(self.buildHandler(logfile))

    def buildFormatter(self):
        formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
        return formatter

    def buildHandler(self, logfile):
        handler = RotatingFileHandler(logfile, maxBytes=10000000, backupCount=5)
        handler.setFormatter(self.buildFormatter())
        return handler

    def info(self, *message):
        self.app.logger.info(message)

    def warning(self, *message):
        self.app.logger.warn(message)

    def error(self, *message):
        self.app.logger.error(message)

    def critical(self, *message):
        self.app.logger.critical(message)
