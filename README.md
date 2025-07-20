# QueryMe - AI 기반 자연어 SQL 생성 플랫폼

## 📌 프로젝트 개요

QueryMe는 자연어를 SQL 쿼리로 변환하는 AI 기반 데이터베이스 관리 웹 애플리케이션입니다.
사용자가 데이터베이스에 연결하거나 DDL 스키마를 정의하여 자연어로 질문하면, Google Gemini AI가 적절한 SQL 쿼리를 생성합니다.

> 🎯 주요 특징
- 실제 데이터베이스 연결 지원 (MySQL, PostgreSQL 등)
- DDL 스키마 기반 가상 쿼리 환경
- Google Gemini API를 통한 자연어 → SQL 변환
- 실시간 스트리밍 응답
- 쿼리 히스토리 관리
- 마이크로서비스 아키텍처

---

## 🛠️ 기술 스택

### 📦 Frontend
- **React 19.1.0** + **TypeScript**
- **Vite 6.3.5** (빌드 도구)
- **Ant Design 5.26.1** (UI 컴포넌트)
- **Redux 5.0.1** (상태 관리)
- **Axios 1.10.0** (API 통신)
- **TailwindCSS 3.4.17** (스타일링)

### 🧩 Backend
- **FastAPI 0.115+** (각 마이크로서비스)
- **Python 3.12.5**
- **SQLAlchemy 2.0+** (ORM)
- **MariaDB 11** (데이터베이스)
- **Google Gemini 2.5 Flash** (AI 모델)
- **Uvicorn + Gunicorn** (웹 서버)

### ☁️ DevOps & Infra
- **Docker + Docker Compose**
- **Alembic** (DB 마이그레이션)
- **UV** (Python 패키지 관리)

---

## 🧱 시스템 아키텍처

```
frontend/                    # React + TypeScript 웹 애플리케이션
└── src/
    ├── api/                # API 클라이언트
    ├── components/         # UI 컴포넌트
    ├── views/             # 페이지 컴포넌트
    └── store/             # Redux 상태 관리

services/                   # FastAPI 마이크로서비스
├── gateway/               # API Gateway (Port: 8080)
├── auth_service/          # 인증 서비스 (Port: 8081)
├── connection_service/    # DB 연결 관리 (Port: 8082)
├── nl2sql_service/        # NL2SQL 변환 (Port: 8083)
├── ddl_session_service/   # DDL 세션 관리 (Port: 8084)
└── history_service/       # 쿼리 히스토리 (Port: 8085)

infra/
└── docker-compose.yaml    # 컨테이너 오케스트레이션
```

---

## 🔄 서비스 간 통신

- **API Gateway**: 모든 클라이언트 요청의 진입점
- **HTTP API**: 서비스 간 REST API 통신
- **세션 기반 인증**: 쿠키를 통한 사용자 인증
- **실시간 스트리밍**: Server-Sent Events로 AI 응답 전달

---

## 🔐 인증 시스템

- **로그인**: 이메일 + 비밀번호 (BCrypt 해싱)
- **인증 방식**: 세션 기반 (쿠키 저장)
- **세션 관리**: UUID 기반 세션 ID, 1시간 만료
- **접근 제어**: 사용자별 데이터 격리

---

## 🚀 실행 방법

### 1. 전체 서비스 실행 (Docker Compose)
```bash
cd infra
make start  # 또는 docker-compose up
```

### 2. 개발 환경 실행
```bash
# 프론트엔드
cd frontend
npm install
npm run dev

# 백엔드 서비스들 (멀티프로세스)
cd services
python run_all_services.py
```

### 3. 개별 서비스 실행
```bash
cd services/<service_name>/app
uv run main.py
```

---

## 🎯 주요 기능

### 1. 데이터베이스 연결 모드
- MySQL, PostgreSQL 등 실제 DB 연결
- 자동 스키마 분석 및 메타데이터 추출
- 실시간 쿼리 실행

### 2. DDL 스키마 모드
- 사용자 정의 DDL 스키마 입력
- 가상 환경에서 SQL 쿼리 테스트
- 세션별 히스토리 관리

### 3. AI 기반 NL2SQL
- Google Gemini 2.5 Flash 모델 사용
- 실시간 스트리밍 응답
- 컨텍스트 인식 프롬프트 생성

### 4. 히스토리 관리
- 모든 쿼리 실행 이력 저장
- 성공/실패 상태, 실행 시간 추적
- 사용자별 세션별 분류

---

## 📊 서비스 포트

| 서비스 | 포트 | 설명 |
|--------|------|------|
| Frontend | 3000 | React 웹 애플리케이션 |
| Gateway | 8080 | API Gateway |
| Auth Service | 8081 | 사용자 인증 |
| Connection Service | 8082 | DB 연결 관리 |
| NL2SQL Service | 8083 | AI 쿼리 변환 |
| DDL Session Service | 8084 | DDL 세션 관리 |
| History Service | 8085 | 쿼리 히스토리 |
| MariaDB | 3306 | 데이터베이스 |

---

## ✅ 구현 완료 기능

- ✅ 사용자 회원가입/로그인
- ✅ 데이터베이스 연결 관리
- ✅ DDL 스키마 기반 쿼리
- ✅ 자연어 → SQL 변환
- ✅ 실시간 스트리밍 응답
- ✅ 쿼리 히스토리 관리
- ✅ 세션 기반 인증
- ✅ 마이크로서비스 아키텍처
- ✅ Docker 컨테이너화

---

## 🛠️ 개발 환경 설정

1. **환경 변수 설정**
   ```bash
   # Google Gemini API 키 필요
   GOOGLE_GEMINI_API_KEY=your_api_key
   ```

2. **데이터베이스 초기화**
   ```bash
   # 각 서비스에서 자동 마이그레이션 실행
   alembic upgrade head
   ```

3. **서비스 헬스체크**
   ```bash
   curl http://localhost:8080/healthcheck
   ```