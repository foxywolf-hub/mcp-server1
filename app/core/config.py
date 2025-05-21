import secrets
from pydantic import BaseModel, Field
from typing import Optional


class Settings(BaseModel):
    """서버 및 애플리케이션 설정"""
    
    # 애플리케이션 정보
    APP_NAME: str = "MCP Server"
    API_PREFIX: str = "/api"
    DEBUG: bool = True
    
    # 서버 설정
    HOST: str = "localhost"
    PORT: int = 8610
    USE_HTTPS: bool = True
    CERT_FILE: str = "./certs/server.crt"
    KEY_FILE: str = "./certs/server.key"
    
    # 보안 설정
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7일
    
    # 데이터베이스 설정
    DB_URL: str = "sqlite:///./mcp.db"
    
    # 파일 업로드 설정
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB


settings = Settings()