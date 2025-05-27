from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse

from app.api import health, upload
from app.db.database import create_tables

app = FastAPI(title="MCP Server", description="Model Context Protocol Server for API Testing")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기본 라우터 설정
app.include_router(health.router, prefix="/api")
app.include_router(upload.router, prefix="/api")

# 정적 파일 마운트 (웹 인터페이스 서빙)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.on_event("startup")
async def startup_event():
    """
    서버 시작 시 데이터베이스 테이블 생성 등 초기화 작업 수행
    """
    await create_tables()

@app.get("/", include_in_schema=False)
async def root():
    """
    루트 경로에서 웹 인터페이스로 리디렉션
    """
    return RedirectResponse(url="/api/")

@app.get("/api/", include_in_schema=False)
async def web_interface():
    """
    웹 인터페이스 HTML 반환
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MCP Server - API Testing Platform</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { 
                font-family: Arial, sans-serif;
                padding-top: 50px;
            }
            .container {
                max-width: 800px;
            }
            .header {
                text-align: center;
                margin-bottom: 40px;
            }
            .upload-section {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 30px;
            }
            .footer {
                text-align: center;
                margin-top: 50px;
                color: #6c757d;
                font-size: 0.9rem;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>MCP Server</h1>
                <p class="lead">API Testing Platform</p>
            </div>
            
            <div class="upload-section">
                <h3>Upload Postman Collection</h3>
                <p>Upload your Postman Collection (.json) to create API tests:</p>
                <form action="/api/upload/collection" method="post" enctype="multipart/form-data" class="mb-4">
                    <div class="mb-3">
                        <input type="file" class="form-control" name="file" accept=".json,.postman_collection.json" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Upload Collection</button>
                </form>
            </div>
            
            <div class="upload-section">
                <h3>Upload Postman Environment</h3>
                <p>Upload your Postman Environment (.json) for test variables:</p>
                <form action="/api/upload/environment" method="post" enctype="multipart/form-data">
                    <div class="mb-3">
                        <input type="file" class="form-control" name="file" accept=".json,.postman_environment.json" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Upload Environment</button>
                </form>
            </div>
            
            <div class="mt-5">
                <h3>API Documentation</h3>
                <p>Access interactive API documentation to explore available endpoints:</p>
                <a href="/docs" class="btn btn-info" target="_blank">API Docs (Swagger UI)</a>
                <a href="/redoc" class="btn btn-secondary ms-2" target="_blank">ReDoc</a>
            </div>
            
            <div class="footer">
                <p>MCP Server - Model Context Protocol for API Testing</p>
                <p>&copy; 2025 All Rights Reserved</p>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)