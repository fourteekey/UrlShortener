from django.conf import settings
import redis


class Redis:
    def __init__(self, url=settings.REDIS_URL, db=0):
        self.redis_instance = redis.from_url(url=f'{url}/{db}')

    def get(self, key):
        return self.redis_instance.get(key)

    def set(self, key, value):
        return self.redis_instance.set(key, value)

    def delete_key(self, key):
        return self.redis_instance.delete(key)

    def getset(self, name, value):
        """Update value and return new key"""
        return self.redis_instance.getset(name, value)

    def keys(self, pattern='*'):
        return self.redis_instance.keys(pattern)

    def clean_db(self):
        self.redis_instance.flushdb()

    def clean_redis(self):
        self.redis_instance.flushall()
