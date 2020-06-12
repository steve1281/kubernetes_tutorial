from flask import Flask
from logger import Logger

app = Flask(__name__)
logger = Logger(app, "log.log")

@app.route('/')
def foo():
    logger.warning('A warning occurred (%d apples)' % 42)
    logger.error('An error occurred')
    logger.info('Info')
    return "foo"

if __name__ == '__main__':
    logger.info("starting flask...")
    app.run()
