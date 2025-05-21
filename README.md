# MCP Server (Model Context Protocol)

AI Host(Claude, OpenAI, 사용자 개발)에서 범용적으로 사용 가능한 Model Context Protocol(MCP) 서버입니다.

## 프로젝트 개요

이 프로젝트는 다양한 AI 호스트 환경에서 사용할 수 있는, Postman Collection 기반의 API 테스트 자동화 서버를 제공합니다. 사용자가 Postman Collection, Environment, Data json 파일을 업로드하면 SQLite DB에 저장하고 테스트를 실행할 수 있습니다.

## 주요 기능

- Postman Collection, Environment, Data json 파일 업로드 및 관리
- API 테스트 케이스 실행 및 결과 추적
- 테스트 컬렉션 관리
- 다양한 AI 모델 지원 (Claude, OpenAI, 사용자 개발 모델)

## 기술 스택

- **백엔드**: Python, FastAPI
- **데이터베이스**: SQLite
- **패키지 관리**: uv
- **서버 환경**: 로컬 HTTPS 서버 (포트 8610)

## 설치 및 실행 방법

### 필요 조건

- Python 3.10 이상
- uv 패키지 관리자

### 설치

```bash
# 저장소 클론
git clone https://github.com/foxywolf-hub/mcp-server1.git
cd mcp-server1

# 의존성 설치
uv pip install -r requirements.txt
```

### 실행

```bash
# 서버 실행
python main.py
```

서버는 https://localhost:8610 에서 실행됩니다.

## 프로젝트 구조

```
mcp-server1/
├── app/                    # 애플리케이션 코드
│   ├── api/                # API 라우트
│   ├── core/               # 코어 설정
│   ├── db/                 # 데이터베이스 관련
│   ├── models/             # 데이터 모델
│   ├── schemas/            # Pydantic 스키마
│   ├── services/           # 비즈니스 로직
│   └── utils/              # 유틸리티 함수
├── certs/                  # HTTPS 인증서
├── tests/                  # 테스트 코드
├── main.py                 # 애플리케이션 진입점
├── requirements.txt        # 의존성 목록
└── README.md               # 프로젝트 설명
```

## 데이터베이스 구조

### 주요 테이블

- `api_info`: API 기본 정보
- `api_test_case`: API 테스트 케이스
- `api_test_data`: 테스트 데이터
- `api_test_collection`: 테스트 컬렉션
- `collection_test_case`: 컬렉션과 테스트 케이스 연결
- `api_test_run`: 테스트 실행 기록
- `api_test_result`: 테스트 결과
- `user`: 사용자 정보