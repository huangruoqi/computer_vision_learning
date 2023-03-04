.PHONY: model

# check for git submodules
ifneq ($(findstring -, $(shell git submodule status)),)
$(info INFO: Initializing submodules)
$(shell git submodule update --init)
endif
ifneq ($(findstring +, $(shell git submodule status)),)
$(info INFO: New updates in submodules, reinitializing...)
$(shell git submodule update --init)
endif

setup:
	poetry install
	poetry run pip install tensorflow==2.11.0 --force-reinstall
	mkdir video data
test:
	poetry run python -B ./src/test.py

# If the first argument is "model"
ifeq (model,$(firstword $(MAKECMDGOALS)))
  MODELFILE := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(MODELFILE):;@:)
endif
model:
	poetry run python -B ./src/nn/$(MODELFILE).py

convert:
	poetry run python -B ./src/convert.py

label:
	poetry run python -B ./index.py

record:
	poetry run python -B ./src/record_video.py

black:
	poetry run black ./

predict: 
	poetry run python -B ./src/predict.py