import json
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.utils.postman_parser import parse_collection, parse_environment

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/collection")
async def upload_collection(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Postman Collection 파일 업로드 및 처리
    """
    if not file.filename.endswith(('.json', '.postman_collection.json')):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file format. Only JSON files with .json or .postman_collection.json extension are allowed."
        )
    
    try:
        content = await file.read()
        collection_data = json.loads(content.decode())
        
        # 파싱 및 DB 저장
        result = await parse_collection(collection_data, db)
        
        return {
            "status": "success",
            "message": "Collection uploaded and processed successfully",
            "details": {
                "name": result.get("name"),
                "api_count": result.get("api_count"),
                "test_case_count": result.get("test_case_count")
            }
        }
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing collection: {str(e)}")
    finally:
        await file.close()

@router.post("/environment")
async def upload_environment(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Postman Environment 파일 업로드 및 처리
    """
    if not file.filename.endswith(('.json', '.postman_environment.json')):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file format. Only JSON files with .json or .postman_environment.json extension are allowed."
        )
    
    try:
        content = await file.read()
        environment_data = json.loads(content.decode())
        
        # 파싱 및 DB 저장
        result = await parse_environment(environment_data, db)
        
        return {
            "status": "success",
            "message": "Environment uploaded and processed successfully",
            "details": {
                "name": result.get("name"),
                "variable_count": result.get("variable_count")
            }
        }
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing environment: {str(e)}")
    finally:
        await file.close()