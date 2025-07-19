# QueryMe 서비스 관리 Makefile
#
# 사용법:
#   make help                    # 도움말 보기
#   make start                   # 전체 서비스 시작
#   make stop                    # 전체 서비스 중지
#   make restart                 # 전체 서비스 재시작
#   make start SERVICE=auth      # 특정 서비스 시작
#   make stop SERVICE=auth       # 특정 서비스 중지
#   make restart SERVICE=auth    # 특정 서비스 재시작
#   make start SERVICES="auth gateway"  # 여러 서비스 시작
#   make restart SERVICES="auth connection nl2sql"  # 여러 서비스 재시작
#   make logs SERVICE=auth       # 특정 서비스 로그 보기
#   make status                  # 서비스 상태 확인
#   make clean                   # 모든 컨테이너와 볼륨 정리
#
# 지원 서비스:
#   - auth (auth_service)
#   - connection (connection_service)
#   - ddl (ddl_session_service)
#   - history (history_service)
#   - nl2sql (nl2sql_service)
#   - gateway
#   - frontend
#   - mariadb

# 전체 서비스 목록
SERVICES := auth_service connection_service ddl_session_service history_service nl2sql_service gateway frontend mariadb

# 서비스별 단축명 매핑
AUTH := auth_service
CONNECTION := connection_service
DDL := ddl_session_service
HISTORY := history_service
NL2SQL := nl2sql_service
GATEWAY := gateway
FRONTEND := frontend
MARIADB := mariadb

# 기본값
SERVICE ?= all
ACTION ?= start

# 색상 정의
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
BLUE := \033[0;34m
NC := \033[0m # No Color

.PHONY: help start stop restart logs status clean

# 도움말
help:
	@echo "$(BLUE)QueryMe 서비스 관리 Makefile$(NC)"
	@echo ""
	@echo "$(YELLOW)사용법:$(NC)"
	@echo "  make start [SERVICE=service_name]                    # 단일 서비스 시작"
	@echo "  make start [SERVICES=\"service1 service2\"]          # 여러 서비스 시작"
	@echo "  make stop [SERVICE=service_name]                     # 단일 서비스 중지"
	@echo "  make stop [SERVICES=\"service1 service2\"]           # 여러 서비스 중지"
	@echo "  make restart [SERVICE=service_name]                  # 단일 서비스 재시작"
	@echo "  make restart [SERVICES=\"service1 service2\"]        # 여러 서비스 재시작"
	@echo "  make logs [SERVICE=service_name]                     # 서비스 로그 보기"
	@echo "  make status                                          # 서비스 상태 확인"
	@echo "  make clean                                           # 모든 컨테이너와 볼륨 정리"
	@echo ""
	@echo "$(YELLOW)지원 서비스:$(NC)"
	@echo "  - auth (auth_service)"
	@echo "  - connection (connection_service)"
	@echo "  - ddl (ddl_session_service)"
	@echo "  - history (history_service)"
	@echo "  - nl2sql (nl2sql_service)"
	@echo "  - gateway"
	@echo "  - frontend"
	@echo "  - mariadb"
	@echo "  - all (전체 서비스)"
	@echo ""
	@echo "$(YELLOW)예시:$(NC)"
	@echo "  make start                                           # 전체 서비스 시작"
	@echo "  make start SERVICE=auth                              # auth_service만 시작"
	@echo "  make start SERVICES=\"auth gateway\"                 # auth와 gateway 시작"
	@echo "  make restart SERVICES=\"auth connection nl2sql\"     # 3개 서비스 재시작"
	@echo "  make logs SERVICE=nl2sql                              # nl2sql_service 로그 보기"
	@echo "  make backend                                         # 백엔드 서비스들만 시작"
	@echo "  make stop-backend                                    # 백엔드 서비스들만 중지"
	@echo "  make restart-api                                     # API 서비스들만 재시작"
	@echo "  make auth                                            # auth_service만 시작"
	@echo "  make stop-auth                                       # auth_service만 중지"

# 서비스 시작
start:
	@if [ "$(SERVICE)" != "all" ] && [ -n "$(SERVICE)" ]; then \
		echo "$(GREEN)🚀 $(SERVICE) 서비스 시작 중...$(NC)"; \
		docker compose up -d $(SERVICE); \
	else \
		echo "$(GREEN)🚀 전체 서비스 시작 중...$(NC)"; \
		docker compose up -d; \
	fi
	@echo "$(GREEN)✅ 서비스 시작 완료!$(NC)"

# 서비스 중지
stop:
	@if [ "$(SERVICE)" != "all" ] && [ -n "$(SERVICE)" ]; then \
		echo "$(YELLOW)⏹️  $(SERVICE) 서비스 중지 중...$(NC)"; \
		docker compose down $(SERVICE); \
	else \
		echo "$(YELLOW)⏹️  전체 서비스 중지 중...$(NC)"; \
		docker compose down; \
	fi
	@echo "$(YELLOW)✅ 서비스 중지 완료!$(NC)"

# 서비스 재시작
restart:
	@if [ "$(SERVICE)" != "all" ] && [ -n "$(SERVICE)" ]; then \
		echo "$(BLUE)🔄 $(SERVICE) 서비스 재시작 중...$(NC)"; \
		docker compose down $(SERVICE); \
		docker compose up -d $(SERVICE); \
	else \
		echo "$(BLUE)🔄 전체 서비스 재시작 중...$(NC)"; \
		docker compose down; \
		docker compose up -d; \
	fi
	@echo "$(BLUE)✅ 서비스 재시작 완료!$(NC)"

# 서비스 로그 보기
logs:
	@if [ "$(SERVICE)" = "all" ]; then \
		echo "$(GREEN)📋 전체 서비스 로그 보기$(NC)"; \
		docker compose logs -f; \
	else \
		echo "$(GREEN)📋 $(SERVICE) 서비스 로그 보기$(NC)"; \
		docker compose logs -f $(SERVICE); \
	fi

# 서비스 상태 확인
status:
	@echo "$(BLUE)🔍 서비스 상태 확인$(NC)"
	@docker compose ps

# 모든 컨테이너와 볼륨 정리
clean:
	@echo "$(RED)🧹 모든 컨테이너와 볼륨 정리 중...$(NC)"
	@docker compose down -v
	@docker system prune -f
	@echo "$(RED)✅ 정리 완료!$(NC)"

# 미리 정의된 서비스 그룹들 - 시작
backend:
	@echo "$(GREEN)🚀 백엔드 서비스들 시작 중...$(NC)"
	@docker compose up -d auth_service connection_service ddl_session_service history_service nl2sql_service
	@echo "$(GREEN)✅ 백엔드 서비스 시작 완료!$(NC)"

api:
	@echo "$(GREEN)🚀 API 서비스들 시작 중...$(NC)"
	@docker compose up -d auth_service connection_service ddl_session_service history_service nl2sql_service gateway
	@echo "$(GREEN)✅ API 서비스 시작 완료!$(NC)"

core:
	@echo "$(GREEN)🚀 핵심 서비스들 시작 중...$(NC)"
	@docker compose up -d auth_service connection_service gateway
	@echo "$(GREEN)✅ 핵심 서비스 시작 완료!$(NC)"

data:
	@echo "$(GREEN)🚀 데이터베이스 서비스 시작 중...$(NC)"
	@docker compose up -d mariadb
	@echo "$(GREEN)✅ 데이터베이스 서비스 시작 완료!$(NC)"

# 미리 정의된 서비스 그룹들 - 중지
stop-backend:
	@echo "$(YELLOW)⏹️  백엔드 서비스들 중지 중...$(NC)"
	@docker compose down auth_service connection_service ddl_session_service history_service nl2sql_service
	@echo "$(YELLOW)✅ 백엔드 서비스 중지 완료!$(NC)"

stop-api:
	@echo "$(YELLOW)⏹️  API 서비스들 중지 중...$(NC)"
	@docker compose down auth_service connection_service ddl_session_service history_service nl2sql_service gateway
	@echo "$(YELLOW)✅ API 서비스 중지 완료!$(NC)"

stop-core:
	@echo "$(YELLOW)⏹️  핵심 서비스들 중지 중...$(NC)"
	@docker compose down auth_service connection_service gateway
	@echo "$(YELLOW)✅ 핵심 서비스 중지 완료!$(NC)"

stop-data:
	@echo "$(YELLOW)⏹️  데이터베이스 서비스 중지 중...$(NC)"
	@docker compose down mariadb
	@echo "$(YELLOW)✅ 데이터베이스 서비스 중지 완료!$(NC)"

# 미리 정의된 서비스 그룹들 - 재시작
restart-backend:
	@echo "$(BLUE)🔄 백엔드 서비스들 재시작 중...$(NC)"
	@docker compose down auth_service connection_service ddl_session_service history_service nl2sql_service
	@docker compose up -d auth_service connection_service ddl_session_service history_service nl2sql_service
	@echo "$(BLUE)✅ 백엔드 서비스 재시작 완료!$(NC)"

restart-api:
	@echo "$(BLUE)🔄 API 서비스들 재시작 중...$(NC)"
	@docker compose down auth_service connection_service ddl_session_service history_service nl2sql_service gateway
	@docker compose up -d auth_service connection_service ddl_session_service history_service nl2sql_service gateway
	@echo "$(BLUE)✅ API 서비스 재시작 완료!$(NC)"

restart-core:
	@echo "$(BLUE)🔄 핵심 서비스들 재시작 중...$(NC)"
	@docker compose down auth_service connection_service gateway
	@docker compose up -d auth_service connection_service gateway
	@echo "$(BLUE)✅ 핵심 서비스 재시작 완료!$(NC)"

restart-data:
	@echo "$(BLUE)🔄 데이터베이스 서비스 재시작 중...$(NC)"
	@docker compose down mariadb
	@docker compose up -d mariadb
	@echo "$(BLUE)✅ 데이터베이스 서비스 재시작 완료!$(NC)"

# 개별 서비스별 타겟 - 시작
auth: SERVICE=auth_service
auth: start

connection: SERVICE=connection_service
connection: start

ddl: SERVICE=ddl_session_service
ddl: start

history: SERVICE=history_service
history: start

nl2sql: SERVICE=nl2sql_service
nl2sql: start

gateway: SERVICE=gateway
gateway: start

frontend: SERVICE=frontend
frontend: start

mariadb: SERVICE=mariadb
mariadb: start

# 개별 서비스별 타겟 - 중지
stop-auth: SERVICE=auth_service
stop-auth: stop

stop-connection: SERVICE=connection_service
stop-connection: stop

stop-ddl: SERVICE=ddl_session_service
stop-ddl: stop

stop-history: SERVICE=history_service
stop-history: stop

stop-nl2sql: SERVICE=nl2sql_service
stop-nl2sql: stop

stop-gateway: SERVICE=gateway
stop-gateway: stop

stop-frontend: SERVICE=frontend
stop-frontend: stop

stop-mariadb: SERVICE=mariadb
stop-mariadb: stop

# 개별 서비스별 타겟 - 재시작
restart-auth: SERVICE=auth_service
restart-auth: restart

restart-connection: SERVICE=connection_service
restart-connection: restart

restart-ddl: SERVICE=ddl_session_service
restart-ddl: restart

restart-history: SERVICE=history_service
restart-history: restart

restart-nl2sql: SERVICE=nl2sql_service
restart-nl2sql: restart

restart-gateway: SERVICE=gateway
restart-gateway: restart

restart-frontend: SERVICE=frontend
restart-frontend: restart

restart-mariadb: SERVICE=mariadb
restart-mariadb: restart 