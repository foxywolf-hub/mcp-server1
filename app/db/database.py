import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 데이터베이스 경로 설정 (환경 변수 또는 기본값 사용)
DB_PATH = os.environ.get("DB_PATH", "sqlite+aiosqlite:///./mcp_server.db")

# SQLAlchemy 엔진 생성
engine = create_async_engine(DB_PATH, echo=True)

# 세션 팩토리 생성
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 모델 기본 클래스
Base = declarative_base()

async def get_db():
    """
    비동기 데이터베이스 세션을 제공하는 의존성 함수
    """
    db = async_session()
    try:
        yield db
    finally:
        await db.close()

async def create_tables():
    """
    데이터베이스 테이블 생성
    """
    from app.db.models import ApiInfo, ApiTestCase, ApiTestData, ApiTestCollection, CollectionTestCase, ApiTestRun, ApiTestResult, User
    
    async with engine.begin() as conn:
        # 모든 테이블 생성 (존재하지 않는 경우)
        await conn.run_sync(Base.metadata.create_all)