# 🧠 QueryMe (NL2SQL Platform)

## 📌 프로젝트 개요

QueryMe는 사용자가 다양한 데이터베이스를 연결하고, 자연어로 데이터를 질의하면
DB 스키마를 기반으로 SQL을 자동 생성·실행하여 결과를 반환하는 웹 기반 AI SQL 서비스입니다.

> 🎯 주요 특징
- 사용자별 다중 DB 커넥션 지원 (DBeaver 스타일)
- 자연어 → SQL 변환 (LLM 기반)
- 질의 히스토리 관리
- 완전한 마이크로서비스 아키텍처
- 이벤트 기반 내부 통신 (RabbitMQ)
- React 프론트엔드 + FastAPI 백엔드

---

## 🛠️ 기술 스택

### 📦 Frontend
- React + TypeScript (Vite)
- TailwindCSS + shadcn/ui
- Zustand (상태관리)
- Axios (API 통신)

### 🧩 Backend
- FastAPI (각 마이크로서비스)
- Pydantic V2, SQLAlchemy
- RabbitMQ (이벤트 기반 통신)
- Redis (스키마 캐시)
- MariaDB / MongoDB (메타, 이력 저장)
- LangChain + OpenAI/LLaMA (NL → SQL 변환)

### ☁️ DevOps & Infra
- Docker, Docker Compose
- Kubernetes, Helm/Kustomize
- GitHub Actions, ArgoCD
- Prometheus + Grafana
- JWT 기반 인증

---

## 🧱 디렉토리 구조

```
frontend/                         # React 앱
  └── src/
      ├── features/               # query-workspace, connection-panel 등
      ├── components/
      ├── hooks/, stores/
      └── App.tsx

services/                         # 모든 FastAPI 마이크로서비스
  ├── auth_service/               # 로그인, 회원가입, JWT 발급
  ├── gateway/                    # API Gateway
  ├── connection_service/         # DB 커넥션 관리
  ├── schema_parser_service/      # DB 스키마 수집
  ├── nl2sql_service/             # 자연어 → SQL 변환
  ├── query_executor_service/     # SQL 실행
  └── history_service/            # 쿼리 기록 관리

common/                           # 공통 모듈 (모델, 유틸, MQ)
  ├── schemas/                    # Pydantic 모델 공유
  ├── messaging/                  # RabbitMQ 유틸
  ├── db/, logger/, utils/

infra/                            # 배포 및 운영 환경
  ├── docker-compose.yml
  ├── k8s/                        # Kubernetes YAML or Helm
  └── ci-cd/                      # GitHub Actions, ArgoCD

docs/
  └── architecture.md

README.md
```

---

## 🔁 마이크로서비스 통신 흐름

- 모든 서비스 간 통신은 RabbitMQ 기반 이벤트(pub/sub) 구조
- gateway에서 JWT 인증 후 각 서비스로 라우팅
- 사용자별 DB 커넥션, 스키마 파싱, NL→SQL 변환, 쿼리 실행, 히스토리 저장까지 완전 분리

---

## 🔐 인증 구조

- 로그인 방식: 이메일 + 비밀번호 (bcrypt 해싱)
- 인증 방식: JWT (gateway에서 검증)
- 토큰 전달: Authorization: Bearer <token>
- 유저 식별: 모든 서비스에서 user_id 기반 처리

---

## 🛠️ 개발 및 실행 방법

1. 프론트엔드
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
2. 각 백엔드 서비스
   ```bash
   cd services/<service_name>
   uv venv
   uv pip install -r requirements.txt  # 또는 pyproject.toml 기반 설치
   uv pip install -e .
   uv run main.py
   ```
3. 전체 통합 개발 환경
   ```bash
   docker-compose up --build
   ```

---

## 🎯 주요 기능
- 사용자별 DB 커넥션 등록/조회
- 연결된 DB의 테이블/스키마 자동 수집 및 캐시
- 자연어로 질문하면 SQL 자동 생성
- 생성된 SQL을 실제 DB에서 실행
- 쿼리 히스토리 좌측 패널에 저장 및 재조회
- 모든 마이크로서비스는 이벤트 기반 비동기 통신

---

## ✅ 향후 확장 계획
- 쿼리 오류 → GPT 기반 디버깅 피드백
- 커넥션 권한 설정 (사용자 그룹)
- 대시보드 기반 시각화 (Chart.js or Superset)
- Whisper 기반 음성 질의
- 플러그인형 데이터 커넥터 (Google Sheets 등)