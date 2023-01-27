export PYTHONDONTWRITEBYTECODE=1
.PHONY: start status code stop build run

FOLDER=computer_vision_learning
NAME=cv

run:
	poetry run python -B ./code/main.py

build:
	poetry add --dev poetry-lock-package
	poetry build
	poetry run poetry-lock-package --build

IS_CONTAINER=$(shell docker ps -a -f name=$(NAME) | wc -l)
IS_RUNNING=$(shell docker ps -f name=$(NAME) | wc -l)

status:
	@echo "CONTAINER:$(IS_CONTAINER)"
	@echo "RUNNING  :$(IS_RUNNING)"

dir=$(shell pwd)
hex=$(shell printf $(dir) | od -A n -t x1 | tr -d '[\n\t ]')

ifneq ($(IS_RUNNING), 2)
code: start
endif

code:
	@code --folder-uri="vscode-remote://dev-container+${hex}/workspaces/$(FOLDER)"

stop:
	@docker stop $(NAME) > /dev/null
	@docker cp $(NAME):/workspaces/$(FOLDER)/code/ ./

start:
	@docker start $(NAME) > /dev/null
