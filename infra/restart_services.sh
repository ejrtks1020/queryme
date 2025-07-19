#!/bin/bash

# QueryMe 서비스 재시작 스크립트
# 
# 사용법:
#   ./restart_services.sh                    # 전체 서비스 재시작
#   ./restart_services.sh auth_service       # 특정 서비스만 재시작
#   ./restart_services.sh auth_service gateway connection_service  # 여러 서비스 재시작
#
# 지원 서비스:
#   - auth_service
#   - connection_service
#   - ddl_session_service
#   - history_service
#   - nl2sql_service
#   - gateway

# 전체 서비스 목록
ALL_SERVICES=(
    "auth_service"
    "connection_service"
    "ddl_session_service"
    "history_service"
    "nl2sql_service"
    "gateway"
)

# 서비스 목록 결정
if [ $# -eq 0 ]; then
    # 인자가 없으면 전체 서비스 재시작
    SERVICES=("${ALL_SERVICES[@]}")
    echo "🔄 전체 서비스 재시작: ${SERVICES[*]}"
else
    # 인자가 있으면 지정된 서비스만 재시작
    SERVICES=("$@")
    echo "🔄 지정된 서비스 재시작: ${SERVICES[*]}"
fi

# 서비스 중지
echo "⏹️  서비스 중지 중..."
docker compose down "${SERVICES[@]}"

# 서비스 시작
echo "▶️  서비스 시작 중..."
docker compose up -d "${SERVICES[@]}"

echo "✅ 서비스 재시작 완료!"