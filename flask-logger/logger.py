from logging.handlers import RotatingFileHandler
import logging

LOG_FILENAME = 'foo.log'

class Logger:

    class __Logger:
        def __init__(self, app, logfile):
            self.app =  app
            self.app.logger.addHandler(self.buildHandler(logfile))

        def __str__(self):
            return repr(self) + self.val

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

        def debug(self, *message):
            self.app.logger.debug(message)

        def critical(self, *message):
            self.app.logger.critical(message)

    instance = None
    def __init__(self, app=None, logfile=LOG_FILENAME):
        if not Logger.instance:
            print("New Logger generated")
            Logger.instance = Logger.__Logger(app, logfile)

    def __getattr__(self, name):
        return getattr(self.instance, name)
