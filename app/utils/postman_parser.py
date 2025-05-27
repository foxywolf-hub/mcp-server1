import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert

from app.db.models import ApiInfo, ApiTestCase, ApiTestData

async def parse_collection(collection_data, db: AsyncSession):
    """
    Postman Collection 파일을 파싱하여 DB에 저장
    """
    collection_name = collection_data.get("info", {}).get("name", "Unnamed Collection")
    api_count = 0
    test_case_count = 0
    
    # 컬렉션의 아이템 처리
    items = collection_data.get("item", [])
    for item in items:
        if "request" in item:
            # 단일 API 항목인 경우
            await process_api_item(item, db)
            api_count += 1
            test_case_count += 1
        elif "item" in item:
            # 폴더인 경우
            folder_name = item.get("name", "Unnamed Folder")
            for sub_item in item.get("item", []):
                if "request" in sub_item:
                    await process_api_item(sub_item, db, folder=folder_name)
                    api_count += 1
                    test_case_count += 1
    
    await db.commit()
    
    return {
        "name": collection_name,
        "api_count": api_count,
        "test_case_count": test_case_count
    }

async def process_api_item(item, db: AsyncSession, folder=None):
    """
    Postman Collection의 개별 API 항목을 처리
    """
    name = item.get("name", "Unnamed API")
    request = item.get("request", {})
    
    # API 정보 추출
    method = request.get("method", "GET")
    url = request.get("url", {})
    
    if isinstance(url, str):
        endpoint = url
    else:
        # URL 객체인 경우
        raw = url.get("raw", "")
        endpoint = raw
    
    description = request.get("description", "")
    
    # API 정보 저장
    api_info_stmt = insert(ApiInfo).values(
        name=name,
        method=method,
        endpoint=endpoint,
        description=description
    )
    result = await db.execute(api_info_stmt)
    api_id = result.inserted_primary_key[0]
    
    # 테스트 케이스 생성
    test_case_stmt = insert(ApiTestCase).values(
        api_id=api_id,
        title=f"Test {name}",
        description=f"Auto-generated test case for {name}"
    )
    test_case_result = await db.execute(test_case_stmt)
    test_case_id = test_case_result.inserted_primary_key[0]
    
    # 요청 데이터 추출
    request_data = {}
    expected_response = {"status_code": 200}
    
    if "body" in request and request["body"]:
        if "raw" in request["body"] and request["body"]["raw"]:
            try:
                request_data["body"] = json.loads(request["body"]["raw"])
            except:
                request_data["body"] = request["body"]["raw"]
    
    if "header" in request and request["header"]:
        request_data["headers"] = {h["key"]: h["value"] for h in request["header"] if "key" in h and "value" in h}
    
    if "auth" in request and request["auth"]:
        request_data["auth"] = request["auth"]
    
    # 테스트 데이터 저장
    test_data_stmt = insert(ApiTestData).values(
        test_case_id=test_case_id,
        request_data=json.dumps(request_data),
        expected_response=json.dumps(expected_response)
    )
    await db.execute(test_data_stmt)

async def parse_environment(environment_data, db: AsyncSession):
    """
    Postman Environment 파일을 파싱하여 처리
    환경 변수를 저장하거나 다른 작업을 수행
    """
    env_name = environment_data.get("name", "Unnamed Environment")
    variables = environment_data.get("values", [])
    
    # 환경 변수 처리 로직
    # 이 부분은 프로젝트 요구사항에 따라 다르게 구현될 수 있음
    
    return {
        "name": env_name,
        "variable_count": len(variables)
    }