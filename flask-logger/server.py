from flask import Flask
from logger import Logger

app = Flask(__name__)

@app.route('/')
def foo():
    logger = Logger()
    print(logger)
    logger.warning('A warning occurred (%d apples)' % 42)
    logger.error('An error occurred')
    logger.info('Info')
    return "foo"

if __name__ == '__main__':
    logger = Logger(app, "log.log")
    logger.warning("starting flask...")
    app.run()
