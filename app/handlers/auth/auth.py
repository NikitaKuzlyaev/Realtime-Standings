from fastapi import APIRouter, HTTPException
from fastapi import Request, Form, Response
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.schema.auth_schema import UserSession
from app.services.auth.auth import login_user

router = APIRouter(prefix="/auth", tags=["auth"])

templates = Jinja2Templates(directory="app/templates")


@router.get('/ping')
async def ping():
    return {"message": "ok. it works"}


@router.get("/")
async def home(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("main.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login_submit(
        request: Request,
        key: str = Form(...),
        secret: str = Form(...),
        contest_id: int = Form(...),
):
    user_data = UserSession(key=key, secret=secret, contest_id=contest_id)

    try:
        tokens = await login_user(user_data)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie("access_token", tokens.access_token, httponly=True, secure=True)
    response.set_cookie("refresh_token", tokens.refresh_token, httponly=True)
    return response


@router.post("/logout")
async def logout(request: Request, response: Response):
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response
