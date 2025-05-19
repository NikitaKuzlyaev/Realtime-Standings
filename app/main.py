from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.auto_migrate import auto_migrate
from app.handlers import routers

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

for router in routers:
    app.include_router(router=router)


@app.on_event("startup")
async def startup():
    auto_migrate()
    print('I am alive!')


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})
