from fastapi import APIRouter, Depends, HTTPException
from app.db.database import get_db

# 상태 확인 라우터
router = APIRouter()

@router.get("/health")
async def health():
    """
    서버 상태를 확인하는 엔드포인트
    """
    return {
        "status": "healthy",
        "service": "mcp-server",
        "version": "0.1.0"
    }

@router.get("/db-check")
async def db_check(db = Depends(get_db)):
    """
    데이터베이스 연결을 확인하는 엔드포인트
    """
    try:
        # 간단한 쿼리 실행
        cursor = await db.execute("SELECT 1")
        result = await cursor.fetchone()
        
        if result and result[0] == 1:
            return {"status": "connected", "message": "Database connection successful"}
        else:
            raise HTTPException(status_code=500, detail="Database connection check failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")