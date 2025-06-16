# Makefile for Alembic Migration in auth_service

SERVICE_NAME=auth_service
ALEMBIC=alembic

.PHONY: help migrate upgrade downgrade history current heads

help:
	@echo ""
	@echo "🛠  Alembic migration commands:"
	@echo ""
	@echo "  make migrate name=message   - Create a new migration revision with message"
	@echo "  make upgrade                - Apply all pending migrations"
	@echo "  make downgrade rev=base     - Downgrade to given revision (e.g., rev=base or rev=-1)"
	@echo "  make history                - Show migration history"
	@echo "  make current                - Show current migration state"
	@echo "  make heads                  - Show current head(s)"
	@echo ""

migrate:
	@if [ -z "$(name)" ]; then \
		echo "❌ name=<revision_name> is required"; exit 1; \
	fi
	$(ALEMBIC) revision --autogenerate -m "$(name)"

upgrade:
	$(ALEMBIC) upgrade head

downgrade:
	@if [ -z "$(rev)" ]; then \
		echo "❌ rev=<revision> is required (e.g., rev=base or rev=-1)"; exit 1; \
	fi
	$(ALEMBIC) downgrade $(rev)

history:
	$(ALEMBIC) history --verbose

current:
	$(ALEMBIC) current

heads:
	$(ALEMBIC) heads