#!/bin/bash

# QueryMe 모든 서비스 빌드 스크립트
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

echo -e "${BLUE}🔨 QueryMe 서비스 빌드 시작${NC}"

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

# 빌드 성공/실패 카운터
SUCCESS_COUNT=0
FAILED_SERVICES=()

# 각 서비스 빌드
for service in "${SERVICES[@]}"; do
    echo -e "${YELLOW}🔨 빌드 중: $service${NC}"
    
    SERVICE_DIR="$SERVICES_DIR/$service"
    
    if [ ! -d "$SERVICE_DIR" ]; then
        echo -e "${RED}❌ 서비스 디렉토리를 찾을 수 없습니다: $SERVICE_DIR${NC}"
        FAILED_SERVICES+=("$service")
        continue
    fi
    
    # Dockerfile 존재 확인
    if [ -f "$SERVICE_DIR/Dockerfile" ]; then
        # 개별 Dockerfile이 있는 경우
        docker build \
            --target runtime \
            -f "$SERVICE_DIR/Dockerfile" \
            -t "queryme/$service:$TAG" \
            "$PROJECT_ROOT"
    elif [ -f "$SERVICE_DIR/app/pyproject.toml" ]; then
        # 공통 Dockerfile 사용
        docker build \
            --target runtime \
            -f "$PROJECT_ROOT/scripts/docker/Dockerfile.services" \
            -t "queryme/$service:$TAG" \
            --build-arg SERVICE_PATH="$service" \
            "$PROJECT_ROOT"
    else
        echo -e "${RED}❌ 빌드할 수 없는 서비스: $service (pyproject.toml 없음)${NC}"
        FAILED_SERVICES+=("$service")
        continue
    fi
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $service 빌드 완료${NC}"
        ((SUCCESS_COUNT++))
    else
        echo -e "${RED}❌ $service 빌드 실패${NC}"
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
    done
    exit 1
else
    echo -e "${GREEN}🎉 모든 서비스 빌드 완료!${NC}"
fi
