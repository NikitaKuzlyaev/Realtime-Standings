import os

import redis.asyncio as redis
from dotenv import load_dotenv

load_dotenv()

# REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
# REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
# REDIS_DB = int(os.getenv("REDIS_DB", 1))

#REDIS_HOST = "redis"
REDIS_HOST = "redis2"
REDIS_PORT = 6379
REDIS_DB = 1

redis_app = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)
