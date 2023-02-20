from flask import Flask
import os
from dotenv import load_dotenv

import random
import time

import logging
import redis

load_dotenv()

# disable the default flask logger
logger = logging.getLogger('werkzeug')
logger.setLevel(logging.ERROR)
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

# Log to Stream
handler = logging.StreamHandler()
logger.addHandler(handler)
app = Flask(__name__)

r = redis.Redis(host='redis-svc', port=6379, db=0)
r.ping()

# redis, slow and fast requests
@app.route("/endpoint1")
def endpoint1():
    logger.info("Received request")

    logger.info('connecting to Redis 20 times')
    for x in range(20):
        r.get('key1')

    # slow down the request 10% of the time
    if random.randint(0,9) < 1:
        time.sleep(0.02)
        logger.info('slow request')
    else:
        logger.info('fast request')

    # we'll try to do something here that might fail
    try:
        # we fail for 10% of all requests
        if random.randint(0, 9) < 1:
            time.sleep(0.1)
            raise RuntimeError('expected error, will be handled')
    except Exception as e:
        logger.error(e)
        return "endpoint1, error"

    if random.randint(0, 9) < 1:
        time.sleep(0.1)
        raise RuntimeError('unexpected error')
    return __file__

app.run(host='0.0.0.0', port=5001)
