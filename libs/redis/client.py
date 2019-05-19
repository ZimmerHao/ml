from __future__ import absolute_import

import redis
from django.conf import settings


class RedisClient(object):

    DEFAULT_DB = 0

    def __init__(self, host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=DEFAULT_DB, decode_responses=False):
        self.host = host
        self.port = port
        self.db = db
        self.decode_responses = decode_responses

    def connection(self):
        r = redis.StrictRedis(
            host=self.host, port=self.port, db=self.db, decode_responses=self.decode_responses)
        return r

    def pool(self):
        pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db)
        r = redis.Redis(connection_pool=pool)
        return r