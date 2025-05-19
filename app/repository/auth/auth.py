import datetime

from sqlalchemy import select

from app.database.database import async_session
from app.database.models import User
from app.database.models import UserRequest
from app.schema.auth_schema import UserSession


async def get_user(data: UserSession) -> User:
    async with async_session() as session:
        query = select(User).where(
            User.key == data.key,
            User.secret == data.secret,
            User.contest_id == data.contest_id
        )
        result = await session.execute(query)
    return result.scalars().first()


async def get_user_by_id(user_id: int) -> User:
    async with async_session() as session:
        query = select(User).where(
            User.id == user_id
        )
        result = await session.execute(query)
    return result.scalars().first()


async def create_user(data: UserSession):
    async with async_session() as session:
        user = User(
            key=data.key,
            secret=data.secret,
            contest_id=data.contest_id
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user


async def get_previous_user_api_request(user_id: int):
    async with async_session() as session:
        stmt = select(UserRequest).where(UserRequest.user_id == user_id)
        result = await session.execute(stmt)
        user_request = result.scalar_one_or_none()

    if user_request:
        return user_request.last_request
    return None


async def set_previous_user_api_request(user_id: int):
    async with async_session() as session:
        now = datetime.datetime.utcnow()

        stmt = select(UserRequest).where(UserRequest.user_id == user_id)
        result = await session.execute(stmt)
        user_request = result.scalar_one_or_none()

        if user_request:
            user_request.last_request = now
        else:
            user_request = UserRequest(user_id=user_id, last_request=now)
            session.add(user_request)

        await session.commit()
