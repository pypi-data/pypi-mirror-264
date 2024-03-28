
"""redis cache and local instance cache"""
import os
from json import JSONEncoder

from .redisWrapper import RedisWrapper

REDIS_WRAPPER = None

if os.environ.get('REDISHOST', None):
    REDIS_WRAPPER = RedisWrapper()

def wrapped_default(self, obj):
    """fix json dumps issue for local cache"""
    return getattr(obj.__class__, "__json__", wrapped_default.default)(obj)


wrapped_default.default = JSONEncoder().default

# apply the patch
JSONEncoder.original_default = JSONEncoder.default
JSONEncoder.default = wrapped_default
