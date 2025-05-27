from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/health")
async def health_check():
    """
    서버 상태 확인을 위한 엔드포인트
    """
    return {"status": "ok", "message": "MCP Server is running"}

@router.get("/db-check")
async def db_health_check(db: AsyncSession = Depends(get_db)):
    """
    데이터베이스 연결 상태 확인을 위한 엔드포인트
    """
    try:
        # 간단한 쿼리 실행
        result = await db.execute("SELECT 1")
        return {"status": "ok", "message": "Database connection is healthy"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection error: {str(e)}")