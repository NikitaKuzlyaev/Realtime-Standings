import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import LastRequestByContestAndMethod


async def get_previous_api_request_by_contest_and_method(contest_id: int, method: str, session: AsyncSession):
    query = select(LastRequestByContestAndMethod).filter_by(contest_id=contest_id, method=method)
    result = await session.execute(query)
    previous_request = result.scalar_one_or_none()
    return previous_request


async def set_previous_api_request_by_contest_and_method(contest_id: int, method: str, session: AsyncSession):
    previous_request = await get_previous_api_request_by_contest_and_method(contest_id, method, session)

    if previous_request:
        previous_request.last_request = datetime.utcnow()
    else:
        previous_request = LastRequestByContestAndMethod(
            contest_id=contest_id,
            method=method,
            last_request=datetime.utcnow()
        )
        session.add(previous_request)

    await session.commit()
