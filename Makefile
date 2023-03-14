.PHONY: model

# check for git submodules
# ifneq ($(findstring -, $(shell git submodule status)),)
# $(info INFO: Initializing submodules)
# $(shell git submodule update --init)
# endif
# ifneq ($(findstring +, $(shell git submodule status)),)
# $(info INFO: New updates in submodules, reinitializing...)
# $(shell git submodule update --init)
# endif

setup:
	mkdir video data
test:
	python -B ./src/test.py

# If the first argument is "model"
ifeq (model,$(firstword $(MAKECMDGOALS)))
  MODELFILE := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(MODELFILE):;@:)
endif
model:
	python -B ./src/nn/$(MODELFILE).py

label:
	python -B ./GUI.py select

record:
	python -B ./src/record_video.py

black:
	black ./

predict: 
	python -B ./src/predict.py

pca:
	python -B ./src/pca.py