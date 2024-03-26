"""Redis Wrapper"""
from builtins import object
import redis
import os
import logging
import traceback
from redis.retry import Retry
from redis.backoff import NoBackoff
from redis import ConnectionError


class RedisWrapper(object):
    def __init__(self):
        self.redis_client = redis.Redis(host=os.environ.get('REDISHOST', 'localhost'),
                                        port=int(os.environ.get('REDISPORT', 6379)), db=0,
                                        retry=Retry(NoBackoff(), 1), retry_on_error=[ConnectionError])

    def get(self, key):
        try:
            return self.redis_client.get(key)
        except Exception as e:
            logging.error("command: GET, key:{}, error: {}".format(key, e))

        return None

    def set(self, key, data, expiry=None, nx=False, px=None):
        try:
            return self.redis_client.set(key, data, expiry, nx=nx, px=px)
        except Exception as e:
            logging.error("command: SET, key:{}, error: {}".format(key, e))

        return 0

    def delete(self, key):
        try:
            return self.redis_client.delete(key)
        except Exception as e:
            logging.error("command: DELETE, key:{}, error: {}".format(key, e))

        return 0

    def ttl(self, key):
        try:
            return self.redis_client.ttl(key)
        except Exception as e:
            logging.error("command: TTL, key:{}, error: {}".format(key, e))

        return 0

    def hmset(self, key, data):
        try:
            self.redis_client.hmset(key, data)
        except Exception as e:
            logging.error("command: HMSET, key:{}, error: {}".format(key, e))

    def hgetall(self, key):
        try:
            return self.redis_client.hgetall(key)
        except Exception as e:
            logging.error("command: HGETALL, key:{}, error: {}".format(key, e))

        return {}

    def sadd(self, name, *values):
        try:
            return self.redis_client.sadd(name, *values)
        except Exception as e:
            logging.error("command: SADD, key:{}, error: {}".format(name, e))

        return 0

    def sismember(self, name, value):
        try:
            return self.redis_client.sismember(name, value)
        except Exception as e:
            logging.error("command: SISMEMBER, key:{}, error: {}".format(name, e))

        return 0

    def smembers(self, name):
        try:
            return self.redis_client.smembers(name)
        except Exception as e:
            logging.error("command: SMEMBERS, key:{}, error: {}".format(name, e))

        return None

    def srem(self, name, values):
        try:
            return self.redis_client.srem(name, values)
        except Exception as e:
            logging.error("command: SREM, key:{}, error: {}".format(name, e))

        return 0

    def scan(self, match_pattern, cursor=0, count=None):
        all_keys = []
        try:
            if cursor == 0:
                count = self.redis_client.dbsize()
            next_index = -1

            while next_index != 0:
                next_index, keys = self.redis_client.scan(
                    cursor, match_pattern, count)
                all_keys = all_keys + keys
        except Exception as e:
            logging.error("command: SCAN, match_pattern:{}, error: {}".format(match_pattern, e))

        return all_keys

    def get_keys_by_pattern(self, match_pattern):
        batch_size = 1000
        keys = []
        try:
            logging.debug("Keys scan started for pattern: %s" % match_pattern)
            for k in self.redis_client.scan_iter(match_pattern, count=batch_size):
                keys.append(k)

        except:
            logging.error(traceback.format_exc())

        return keys

    def delete_keys_by_pattern(self, match_pattern):
        deleted_keys_count = 0
        batch_size = 1000

        try:
            keys = []
            logging.debug("Keys scan started for pattern: %s" % match_pattern)
            for k in self.redis_client.scan_iter(match_pattern, count=batch_size):
                keys.append(k)
                if len(keys) >= batch_size:
                    deleted_keys_count += len(keys)
                    self.redis_client.delete(*keys)
                    logging.debug(
                        "Deleted keys: %s".format(deleted_keys_count))
                    keys = []

            # If batch of keys < 1000
            if len(keys) > 0:
                deleted_keys_count += len(keys)
                self.redis_client.delete(*keys)
                logging.debug("Deleted keys: %s".format(deleted_keys_count))
        except:
            logging.error(traceback.format_exc())
            return False

        return True
