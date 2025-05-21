import sqlite3
import aiosqlite
from pathlib import Path

# 데이터베이스 파일 경로
DB_PATH = "mcp.db"

async def get_db():
    """비동기 데이터베이스 연결을 반환하는 함수"""
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()

def init_db():
    """데이터베이스와 필요한 테이블을 초기화하는 함수"""
    # 데이터베이스 파일이 이미 존재하는지 확인
    db_exists = Path(DB_PATH).exists()
    
    # SQLite 데이터베이스 연결
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 테이블 생성
    if not db_exists:
        create_tables(cursor)
    
    conn.commit()
    conn.close()
    
    print(f"데이터베이스 초기화 완료: {DB_PATH}")


def create_tables(cursor):
    """데이터베이스 테이블을 생성하는 함수"""
    
    # api_info 테이블
    cursor.execute('''
    CREATE TABLE api_info (
        api_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        method TEXT NOT NULL,
        endpoint TEXT NOT NULL,
        description TEXT
    )
    ''')
    
    # api_test_case 테이블
    cursor.execute('''
    CREATE TABLE api_test_case (
        test_case_id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY (api_id) REFERENCES api_info(api_id)
    )
    ''')
    
    # api_test_data 테이블
    cursor.execute('''
    CREATE TABLE api_test_data (
        test_data_id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_case_id INTEGER NOT NULL,
        request_data TEXT NOT NULL,
        expected_response TEXT NOT NULL,
        FOREIGN KEY (test_case_id) REFERENCES api_test_case(test_case_id)
    )
    ''')
    
    # user 테이블
    cursor.execute('''
    CREATE TABLE user (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role TEXT
    )
    ''')
    
    # api_test_collection 테이블
    cursor.execute('''
    CREATE TABLE api_test_collection (
        collection_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES user(user_id)
    )
    ''')
    
    # collection_test_case 테이블
    cursor.execute('''
    CREATE TABLE collection_test_case (
        collection_id INTEGER NOT NULL,
        test_case_id INTEGER NOT NULL,
        PRIMARY KEY (collection_id, test_case_id),
        FOREIGN KEY (collection_id) REFERENCES api_test_collection(collection_id),
        FOREIGN KEY (test_case_id) REFERENCES api_test_case(test_case_id)
    )
    ''')
    
    # api_test_run 테이블
    cursor.execute('''
    CREATE TABLE api_test_run (
        test_run_id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_case_id INTEGER NOT NULL,
        executed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT NOT NULL,
        actual_response TEXT,
        user_id INTEGER,
        FOREIGN KEY (test_case_id) REFERENCES api_test_case(test_case_id),
        FOREIGN KEY (user_id) REFERENCES user(user_id)
    )
    ''')
    
    # api_test_result 테이블
    cursor.execute('''
    CREATE TABLE api_test_result (
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_run_id INTEGER NOT NULL,
        assertion TEXT NOT NULL,
        passed BOOLEAN NOT NULL,
        message TEXT,
        FOREIGN KEY (test_run_id) REFERENCES api_test_run(test_run_id)
    )
    ''')