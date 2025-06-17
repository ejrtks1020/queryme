# QueryMe Gateway Service

API Gateway 서비스로, 다양한 마이크로서비스들에 대한 라우팅과 프록시 기능을 제공합니다.

## 주요 기능

### 🔐 Auth Service 라우팅
- `/auth/*` 경로로 오는 모든 요청을 Auth Service로 프록시
- 환경 변수 `PROFILE`에 따른 동적 라우팅:
  - `PROFILE=local`: `localhost:8080`으로 라우팅
  - `PROFILE=prod`: `auth_service:8080`으로 라우팅

### 🛡️ 요청 프록시 기능
- HTTP 메서드 지원: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
- 헤더 전달 및 필터링
- 스트리밍 응답 지원
- 에러 처리 및 로깅

## 환경 설정

### 환경 변수

| 변수명 | 기본값 | 설명 |
|--------|--------|------|
| `PROFILE` | `local` | 실행 환경 (local/prod) |
| `AUTH_SERVICE_HOST` | - | Auth 서비스 호스트 (직접 지정 시) |
| `AUTH_SERVICE_PORT` | - | Auth 서비스 포트 (직접 지정 시) |

### 프로필별 기본 설정

#### Local 환경
```
PROFILE=local
Auth Service: localhost:8080
Gateway Port: 8081
```

#### Production 환경
```
PROFILE=prod
Auth Service: auth_service:8080
Gateway Port: 8081
```

## 실행 방법

### 로컬 개발
```bash
cd services/gateway/app
PROFILE=local python main.py
```

### Docker 실행
```bash
# 프로덕션 환경
docker build -t gateway .
docker run -p 8081:8081 -e PROFILE=prod gateway

# 로컬 환경
docker run -p 8081:8081 -e PROFILE=local gateway
```

## API 엔드포인트

### 상태 확인
- **GET** `/` - Gateway 상태 및 설정 정보
- **GET** `/health` - 헬스 체크

### Auth 프록시
- **ALL** `/auth/*` - Auth Service로 프록시

## 예시 사용법

### 로그인 요청
```bash
# Gateway를 통한 로그인 (localhost:8081 -> auth_service:8080)
curl -X POST http://localhost:8081/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'
```

### 상태 확인
```bash
# Gateway 상태 확인
curl http://localhost:8081/

# 응답 예시
{
  "service": "QueryMe Gateway",
  "status": "healthy",
  "profile": "local",
  "gateway": {
    "host": "0.0.0.0",
    "port": 8081
  },
  "auth_service": {
    "url": "http://localhost:8080"
  }
}
```

## 아키텍처

```
Client Request
     ↓
Gateway (8081)
     ↓
Auth Service (8080)
```

### 요청 흐름
1. 클라이언트가 `/auth/*` 경로로 요청
2. Gateway가 요청을 받아 환경에 따른 Auth Service URL 결정
3. 요청을 Auth Service로 프록시
4. Auth Service 응답을 클라이언트에게 전달

## 로깅

Gateway는 다음과 같은 로그를 제공합니다:
- 시작/종료 시 환경 정보
- 프록시 요청 정보
- 에러 발생 시 상세 정보

## 확장성

새로운 서비스 라우팅을 추가하려면:
1. `core/config.py`에 서비스 설정 추가
2. `routers/` 폴더에 새 라우터 생성
3. `main.py`에 라우터 등록

이 설계는 clean code 원칙과 마이크로서비스 아키텍처를 따라 확장 가능하고 유지보수하기 쉽게 구성되었습니다.
