import time
from datetime import datetime, timedelta, timezone

from fastapi.templating import Jinja2Templates

from app.database.models import User
from app.redis.crud.crud import save_user_activity, check_user_activity, save_contest_standings_to_redis
from app.repository.auth.auth import get_previous_user_api_request, get_user_by_id
from app.services.external.sendler import send_request_to_codeforces

templates = Jinja2Templates(directory="app/templates")


async def client_still_alive(user_id: int):
    user: User = await get_user_by_id(user_id)

    user_activity = await check_user_activity(user_id=user.id)

    try:
        user_activity = int(user_activity)
    except:
        user_activity = 0

    if user_activity % 2 == 0:
        res = await collect_standings_from_codeforces_api(
            user_id=user.id,
            key=user.key,
            secret=user.secret,
            contest_id=user.contest_id,
            from_=1,
            count_=50)

    await save_user_activity(user_id=user_id)
    return True


async def collect_standings_from_codeforces_api(
        user_id: int,
        key: str,
        secret: str,
        contest_id: int,
        from_: int,
        count_: int,
):
    """
    """
    participantTypes = 'CONTESTANT'  # так надо

    prev_request_time: Optional[datetime] = await get_previous_user_api_request(user_id=user_id)

    if prev_request_time:
        if prev_request_time.tzinfo is None:
            prev_request_time = prev_request_time.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        if (now - prev_request_time) <= timedelta(seconds=3):
            return {"message": "Too frequent requests"}

    method_name = 'contest.standings'

    current_time = int(time.time())
    params = {
        "contestId": contest_id,
        "apiKey": key,
        "time": current_time,
        "from": from_,
        "count": count_,
        "participantTypes": 'CONTESTANT',
        "asManager": True,
        "showUnofficial": False,
    }
    print(params, '\n' * 10)

    try:
        res = await send_request_to_codeforces(user_id=user_id, secret=secret, method_name=method_name, **params)
        await save_contest_standings_to_redis(contest_id=contest_id, res=res)
    except Exception as e:
        return {"message": f"Error: {str(e)}"}

    return {"message": "ok"}
