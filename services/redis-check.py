import redis
r = redis.Redis(host='redis-svc', port=6379, db=0)
r.ping()