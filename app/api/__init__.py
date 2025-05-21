from fastapi import APIRouter
from app.api.endpoints import health, upload, web

# API 라우터
api_router = APIRouter()

# 엔드포인트 라우터 등록
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(upload.router, prefix="/upload", tags=["Upload"])
api_router.include_router(web.router, tags=["Web Interface"])