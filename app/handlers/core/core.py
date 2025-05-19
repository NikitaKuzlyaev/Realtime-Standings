from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.database.database import get_session
from app.redis.crud.crud import get_contest_standings_from_redis
from app.repository.auth.auth import get_user
from app.schema.auth_schema import UserSession
from app.services.auth.auth import get_user_session
from app.services.external.external import client_still_alive as external_client_still_alive

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/core", tags=["core"])


@router.get('/ping')
async def ping():
    return 200, {'message': 'ok. it works'}


@router.get('/table', response_class=HTMLResponse)
async def online_table(
        request: Request,
        session=Depends(get_session),
):
    user_session: UserSession = await get_user_session(request=request, session=session)

    return templates.TemplateResponse("online_table.html", {"request": request})


@router.get("/client_still_alive")
async def client_still_alive(
        request: Request,
        session=Depends(get_session),
):
    user_session: UserSession = await get_user_session(request=request, session=session)
    user = await get_user(data=user_session)

    response = await external_client_still_alive(user_id=user.id)
    now = datetime.now(timezone.utc)

    return JSONResponse(content={
        "time": now.isoformat(),
    })


@router.get("/get_contest_standings")
async def get_contest_standings(
        request: Request,
        session=Depends(get_session),
):
    user_session: UserSession = await get_user_session(request=request, session=session)
    user = await get_user(data=user_session)

    response = await get_contest_standings_from_redis(contest_id=user.contest_id)
    now = datetime.now(timezone.utc)

    return JSONResponse(content=response)
