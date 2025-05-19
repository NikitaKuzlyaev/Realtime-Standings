from fastapi import HTTPException, Request, Depends
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.database.models import User
from app.repository.auth.auth import get_user, create_user
from app.repository.auth.auth import get_user_by_id
from app.schema.auth_schema import UserSession, TokenResponse
from app.services.auth.jwt import create_access_token, create_refresh_token, decode_access_token


async def login_user(data: UserSession) -> TokenResponse:
    user = await get_user(data)
    if not user:
        user = await create_user(data)

    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)
    return TokenResponse(access_token=access, refresh_token=refresh)


async def get_user_session(
        request: Request,
        session: AsyncSession = Depends(get_session)
) -> UserSession:
    """
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = decode_access_token(token)
        user_id = int(payload.get('sub'))
        user: User = await get_user_by_id(user_id=user_id)

        return UserSession(key=user.key, secret=user.secret, contest_id=user.contest_id)

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
