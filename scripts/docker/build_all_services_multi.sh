#!/bin/bash

# QueryMe 모든 서비스 빌드 스크립트 (병렬 처리)
set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 프로젝트 루트 디렉토리
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
echo "PROJECT_ROOT: $PROJECT_ROOT"
SERVICES_DIR="$PROJECT_ROOT/services"
echo "SERVICES_DIR: $SERVICES_DIR"

echo -e "${BLUE}🔨 QueryMe 서비스 빌드 시작 (병렬 처리)${NC}"

# 서비스 목록
SERVICES=(
    "auth_service"
    "connection_service" 
    "ddl_session_service"
    "history_service"
    "nl2sql_service"
    "gateway"
)

# Docker 이미지 태그 (기본값: latest)
TAG=${1:-latest}

# 동시 실행 수 제한 (CPU 코어 수에 따라 조정)
MAX_JOBS=${2:-4}

# 빌드 성공/실패 카운터
SUCCESS_COUNT=0
FAILED_SERVICES=()
CURRENT_JOBS=0
PIDS=()

# 빌드 함수
build_service() {
    local service=$1
    local tag=$2
    
    echo -e "${YELLOW}🔨 빌드 시작: $service${NC}"
    
    SERVICE_DIR="$SERVICES_DIR/$service"
    
    if [ ! -d "$SERVICE_DIR" ]; then
        echo -e "${RED}❌ 서비스 디렉토리를 찾을 수 없습니다: $SERVICE_DIR${NC}"
        return 1
    fi
    
    # Dockerfile 존재 확인
    if [ -f "$SERVICE_DIR/Dockerfile" ]; then
        # 개별 Dockerfile이 있는 경우
        docker build \
            --target runtime \
            -f "$SERVICE_DIR/Dockerfile" \
            -t "queryme/$service:$tag" \
            "$PROJECT_ROOT" > "/tmp/build_${service}.log" 2>&1
    elif [ -f "$SERVICE_DIR/app/pyproject.toml" ]; then
        # 공통 Dockerfile 사용
        docker build \
            --target runtime \
            -f "$PROJECT_ROOT/scripts/docker/Dockerfile.services" \
            -t "queryme/$service:$tag" \
            --build-arg SERVICE_PATH="$service" \
            "$PROJECT_ROOT" > "/tmp/build_${service}.log" 2>&1
    else
        echo -e "${RED}❌ 빌드할 수 없는 서비스: $service (pyproject.toml 없음)${NC}"
        return 1
    fi
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $service 빌드 완료${NC}"
        return 0
    else
        echo -e "${RED}❌ $service 빌드 실패${NC}"
        echo -e "${RED}로그: /tmp/build_${service}.log${NC}"
        return 1
    fi
}

# 각 서비스 병렬 빌드
for service in "${SERVICES[@]}"; do
    # 동시 실행 수 제한 확인 (macOS 호환)
    while [ $CURRENT_JOBS -ge $MAX_JOBS ]; do
        # 완료된 프로세스 확인
        for i in "${!PIDS[@]}"; do
            if ! kill -0 "${PIDS[$i]}" 2>/dev/null; then
                unset PIDS[$i]
                CURRENT_JOBS=$((CURRENT_JOBS - 1))
            fi
        done
        sleep 1
    done
    
    # 백그라운드에서 빌드 실행
    build_service "$service" "$TAG" &
    PIDS+=($!)
    CURRENT_JOBS=$((CURRENT_JOBS + 1))
done

# 모든 백그라운드 작업 완료 대기
wait

# 결과 수집
for service in "${SERVICES[@]}"; do
    if [ -f "/tmp/build_${service}.log" ]; then
        # 로그 파일에서 성공/실패 확인
        if grep -q "Successfully built" "/tmp/build_${service}.log" 2>/dev/null; then
            ((SUCCESS_COUNT++))
        else
            FAILED_SERVICES+=("$service")
        fi
    else
        FAILED_SERVICES+=("$service")
    fi
done

# 빌드 결과 요약
echo -e "\n${BLUE}📊 빌드 결과 요약${NC}"
echo -e "${GREEN}✅ 성공: $SUCCESS_COUNT/${#SERVICES[@]}${NC}"

if [ ${#FAILED_SERVICES[@]} -gt 0 ]; then
    echo -e "${RED}❌ 실패한 서비스:${NC}"
    for service in "${FAILED_SERVICES[@]}"; do
        echo -e "${RED}  - $service${NC}"
        if [ -f "/tmp/build_${service}.log" ]; then
            echo -e "${RED}    로그: /tmp/build_${service}.log${NC}"
        fi
    done
    exit 1
else
    echo -e "${GREEN}🎉 모든 서비스 빌드 완료!${NC}"
fi

# 임시 로그 파일 정리
for service in "${SERVICES[@]}"; do
    rm -f "/tmp/build_${service}.log"
done
