import redis
import os
from RedisServer import RedisServer

# Redis connection details
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
redis_password = os.getenv('REDIS_PASSWORD') or ''

redisServer = RedisServer(redis_host, redis_port, redis_password)

