from flask import Flask, render_template
import os
from dotenv import load_dotenv

# instrument flask with Elastic APM
from elasticapm.contrib.flask import ElasticAPM
import elasticapm
import random
import time
import structlog

import ecs_logging
import logging
import redis

import requests

load_dotenv()

# disable the default flask logger
logger = logging.getLogger('werkzeug')
logger.setLevel(logging.ERROR)
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

# Log to Stream
handler = logging.StreamHandler()
handler.setFormatter(ecs_logging.StdlibFormatter())
logger.addHandler(handler)

from elasticapm.handlers.structlog import structlog_processor
structlog.configure(
    processors=[structlog_processor,ecs_logging.StructlogFormatter()],
    wrapper_class=structlog.BoundLogger,
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory()
)



app = Flask(__name__)

app.config['ELASTIC_APM'] = {
    'SERVER_URL': os.environ["SERVER_URL"],
    'SERVICE_NAME': '08-app-ecs-logging-distributed',
    'SECRET_TOKEN': os.environ["SECRET_TOKEN"],
    'ENVIRONMENT':  'dev'
}
apm = ElasticAPM(app)

apm_client = elasticapm.get_client()

r = redis.Redis(host='redis-svc', port=6379, db=0)
r.ping()

@app.before_request
def do_something_whenever_a_request_comes_in():
    elasticapm.set_user_context(
        username="john", 
        email="someone@example.com", 
        user_id="123-123-123"
    )

# redis, slow and fast requests
@app.route("/endpoint1")
def endpoint1():
    logger.info("Received request", extra={"http.request.method": "get"})

    logger.info('connecting to Redis 20 times')
    for x in range(20):
        r.get('key1')

    # slow down the request 10% of the time
    if random.randint(0,9) < 1:
        with elasticapm.capture_span('this is a slow span'):
            elasticapm.set_custom_context({'slow_request_stats': 1})
            elasticapm.label(label1='slowed down deliberately')
            time.sleep(0.02)
            logger.info('ERR-1000,slow request')
    else:
        with elasticapm.capture_span('this is a fast span'):
            logger.info('INFO-1000,fast request')

    # we'll try to do something here that might fail
    try:
        # we fail for 10% of all requests
        if random.randint(0, 9) < 1:
            time.sleep(0.1)
            raise RuntimeError('CRITICAL-1000,expected error, will be handled')
    except Exception as e:
        logger.error(e)
        apm_client.capture_exception(handled=True)
        elasticapm.set_transaction_outcome(outcome='failure')
        return "CRITICAL-2000,endpoint1, error"

    if random.randint(0, 9) < 1:
        time.sleep(0.1)
        raise RuntimeError('unexpected error')

    response = requests.get(url='http://flask11-svc:5011/endpoint1')

    return render_template('index.html',name=__file__,server=os.environ["SERVER_URL"])

app.run(host='0.0.0.0', port=5008)
