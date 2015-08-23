.PHONY: setup venv-setup

run:
	./scripts/run.sh

setup: 
	./scripts/setup.sh

venv-setup:
	./scripts/venv-setup.sh

init-db:
	./scripts/init-db.sh
