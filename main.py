import uvicorn
import ssl
import os
from fastapi.responses import RedirectResponse
from app.core.app_factory import create_app
from app.core.config import settings
from app.db.database import init_db

# FastAPI 애플리케이션 생성
app = create_app()

# 루트 경로 라우트 - 웹 인터페이스로 리디렉션
@app.get("/")
async def root():
    return RedirectResponse(url="/api/")

# 서버 시작 전 데이터베이스 초기화
@app.on_event("startup")
async def startup_event():
    # 데이터베이스 초기화
    init_db()
    
    # 업로드 디렉토리 생성
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

if __name__ == "__main__":
    # HTTPS를 사용하는 경우 SSL 컨텍스트 생성
    if settings.USE_HTTPS:
        # 인증서가 없는 경우 자체 서명 인증서 생성
        if not os.path.exists(settings.CERT_FILE) or not os.path.exists(settings.KEY_FILE):
            from app.utils.cert_gen import generate_self_signed_cert
            generate_self_signed_cert()
        
        # SSL 설정
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(settings.CERT_FILE, settings.KEY_FILE)
        
        # HTTPS 서버 실행
        uvicorn.run(
            "main:app", 
            host=settings.HOST, 
            port=settings.PORT,
            ssl_keyfile=settings.KEY_FILE,
            ssl_certfile=settings.CERT_FILE,
            reload=settings.DEBUG
        )
    else:
        # HTTP 서버 실행
        uvicorn.run(
            "main:app", 
            host=settings.HOST, 
            port=settings.PORT,
            reload=settings.DEBUG
        )