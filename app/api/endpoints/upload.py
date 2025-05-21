from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
import json
import os
from typing import List
from uuid import uuid4
from datetime import datetime
from app.core.config import settings
from app.db.database import get_db

# 파일 업로드 라우터
router = APIRouter()

@router.post("/collection")
async def upload_postman_collection(
    file: UploadFile = File(...),
    db = Depends(get_db)
):
    """
    Postman Collection 파일 업로드 및 처리 엔드포인트
    """
    if not file.filename.endswith(('.json')):
        raise HTTPException(status_code=400, detail="JSON 파일만 업로드 가능합니다")
    
    # 파일 저장 경로 생성
    collection_dir = os.path.join(settings.UPLOAD_DIR, "collections")
    os.makedirs(collection_dir, exist_ok=True)
    
    # 고유한 파일명 생성
    file_id = str(uuid4())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{timestamp}_{file_id}_{file.filename}"
    file_path = os.path.join(collection_dir, file_name)
    
    # 파일 저장
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # 파일 파싱
        try:
            collection_data = json.loads(contents.decode())
            
            # 여기서 나중에 데이터베이스에 저장하는 로직을 구현할 예정
            
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Postman Collection 업로드 성공",
                    "file_name": file_name,
                    "collection_name": collection_data.get("info", {}).get("name", "Unknown"),
                }
            )
            
        except json.JSONDecodeError:
            # 유효하지 않은 JSON 파일인 경우 삭제
            os.remove(file_path)
            raise HTTPException(status_code=400, detail="유효하지 않은 JSON 형식입니다")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 업로드 중 오류 발생: {str(e)}")

@router.post("/environment")
async def upload_postman_environment(
    file: UploadFile = File(...),
    db = Depends(get_db)
):
    """
    Postman Environment 파일 업로드 및 처리 엔드포인트
    """
    if not file.filename.endswith(('.json')):
        raise HTTPException(status_code=400, detail="JSON 파일만 업로드 가능합니다")
    
    # 파일 저장 경로 생성
    env_dir = os.path.join(settings.UPLOAD_DIR, "environments")
    os.makedirs(env_dir, exist_ok=True)
    
    # 고유한 파일명 생성
    file_id = str(uuid4())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{timestamp}_{file_id}_{file.filename}"
    file_path = os.path.join(env_dir, file_name)
    
    # 파일 저장
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # 파일 파싱
        try:
            env_data = json.loads(contents.decode())
            
            # 여기서 나중에 데이터베이스에 저장하는 로직을 구현할 예정
            
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Postman Environment 업로드 성공",
                    "file_name": file_name,
                    "environment_name": env_data.get("name", "Unknown"),
                }
            )
            
        except json.JSONDecodeError:
            # 유효하지 않은 JSON 파일인 경우 삭제
            os.remove(file_path)
            raise HTTPException(status_code=400, detail="유효하지 않은 JSON 형식입니다")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 업로드 중 오류 발생: {str(e)}")