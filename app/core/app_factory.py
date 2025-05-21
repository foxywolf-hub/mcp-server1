from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api import api_router
from app.core.config import settings
from pathlib import Path

def create_app() -> FastAPI:
    """
    FastAPI 애플리케이션 인스턴스를 생성하고 설정합니다.
    """
    app = FastAPI(
        title="MCP Server",
        description="Model Context Protocol Server for API Testing",
        version="0.1.0",
    )

    # CORS 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 개발 환경에서는 모든 출처 허용
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # API 라우터 등록
    app.include_router(api_router, prefix=settings.API_PREFIX)
    
    # 정적 파일 제공
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # 업로드 디렉토리 마운트
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

    return app