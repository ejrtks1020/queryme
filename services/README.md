# QueryMe Services

이 디렉토리는 QueryMe 애플리케이션의 마이크로서비스들을 포함하는 워크스페이스입니다.

## 워크스페이스 구조

```
services/
├── pyproject.toml          # 워크스페이스 루트 설정
├── common/                 # 공통 유틸리티 패키지 (라이브러리)
├── auth_service/           # 인증 서비스
├── connection_service/     # 데이터베이스 연결 관리 서비스
├── ddl_session_service/    # DDL 세션 관리 서비스
├── gateway/                # API 게이트웨이
├── history_service/        # 쿼리 히스토리 서비스
└── nl2sql_service/         # 자연어-SQL 변환 서비스
```

## 의존성 관리

### 공통 의존성
모든 서비스에서 공통으로 사용하는 패키지들:
- fastapi, uvicorn, gunicorn (웹 프레임워크)
- pydantic, pydantic-settings (데이터 검증)
- greenlet, icecream (유틸리티)

### Optional Dependencies
특정 기능이 필요한 서비스만 사용하는 패키지들:

- **database**: 데이터베이스 관련 (alembic, sqlalchemy, asyncmy, pymysql)
- **auth**: 인증 관련 (bcrypt, passlib, pyjwt, python-multipart)
- **http**: HTTP 클라이언트 (httpx, aiohttp)
- **ai**: AI/LLM 관련 (google-genai)
- **dev**: 개발 도구 (pytest, black, isort, mypy)

## 설치 및 실행

### 프로젝트 설치
```bash
cd services
uv sync
```

### 서비스 실행
```bash
# 인증 서비스
uv run python auth_service/app/main.py

# 게이트웨이
uv run python gateway/app/main.py

# 연결 서비스
uv run python connection_service/app/main.py

# DDL 세션 서비스
uv run python ddl_session_service/app/main.py

# 히스토리 서비스
uv run python history_service/app/main.py

# NL2SQL 서비스
uv run python nl2sql_service/app/main.py
```

### 개발 도구 사용
```bash
# 코드 포맷팅
uv run black .
uv run isort .

# 타입 체크
uv run mypy .

# 테스트 실행
uv run pytest
```

## 공통 패키지 (queryme-common)

각 서비스에서 공통으로 사용하는 유틸리티들을 제공하는 라이브러리 패키지입니다:

- **core**: 설정, 로거 등 핵심 기능
- **db**: 데이터베이스 연결 유틸리티
- **schemas**: 공통 스키마 정의
- **util**: 유틸리티 함수들

**참고**: common 패키지는 독립적인 라이브러리로, 서버가 실행되지 않고 다른 서비스들에서 import하여 사용합니다.

사용 예시:
```python
from common.core import db_config, setup_logger
from common.db import MariaDBConnection
``` 