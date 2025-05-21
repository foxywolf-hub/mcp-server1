from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from pathlib import Path

# 템플릿 디렉토리 설정
templates_path = Path(__file__).resolve().parent.parent.parent / "app" / "templates"
templates = Jinja2Templates(directory=str(templates_path))

# 웹 인터페이스 라우터
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    메인 웹 인터페이스 페이지
    """
    return templates.TemplateResponse("index.html", {"request": request})