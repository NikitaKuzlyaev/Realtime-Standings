import base64
import io

import matplotlib.pyplot as plt
from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.schema.auth_schema import UserSession

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/analytics", tags=["analytics"])


def generate_pie(value1: float, value2: float) -> str:
    labels = ["Value 1", "Value 2"]
    values = [value1, value2]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return f"data:image/png;base64,{image_base64}"


@router.get('/ping')
async def ping():
    return 200, {'message': 'ok. it works'}


@router.get("/pie", response_class=HTMLResponse)
async def pie_chart(request: Request, value1: float = 50, value2: float = 50):
    img_data = generate_pie(value1, value2)
    return templates.TemplateResponse("pie.html", {"request": request, "img_data": img_data})


@router.get("/statistic/all_submissions", response_class=JSONResponse)
async def get_all_submissions(
        key: str,
        secret: str,
        contest_id: int
):
    user_session = UserSession(key=key, secret=secret, contest_id=contest_id)

    data = get_statistic_by_all_submissions(user_session=user_session)

    return data
