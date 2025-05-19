import json
from typing import Union

from app.redis import redis_app


async def save_contest_log_to_redis(contest_id: Union[int, str], res: str, ttl: int = 36000):
    key = f"contest_id:{contest_id}:last_res"
    await redis_app.set(key, res, ex=ttl)


async def save_contest_standings_to_redis(contest_id: Union[int, str], res: str, ttl: int = 36000):
    key = f"contest_id:{contest_id}:last_contest_standings"
    await redis_app.set(key, res, ex=ttl)


async def get_contest_standings_from_redis(contest_id: Union[int, str]):
    key = f"contest_id:{contest_id}:last_contest_standings"
    res = await redis_app.get(key)
    if res:
        return json.loads(res)
    else:
        return {"status": "ERROR", "message": "No data in Redis"}


async def save_user_activity(user_id: Union[int, str], ttl: int = 60):
    key = f"user_id:{user_id}:user_activity"

    value = await check_user_activity(user_id=user_id) + 1

    await redis_app.set(key, value, ex=ttl)


async def check_user_activity(user_id: Union[int, str]) -> int:
    key = f"user_id:{user_id}:user_activity"
    last_activity = await redis_app.get(key)
    try:
        last_activity = int(last_activity)
    except:
        last_activity = 0

    return last_activity
