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
run:
	poetry run python -B ./src/main.py

model:
	poetry run python -B ./src/LSTM.py

convert:
	poetry run python -B ./src/video_to_3d_positions.py

label:
	poetry run python -B ./index.py

record:
	poetry run python -B ./src/record_video.py

black:
	poetry run black ./

predict: 
	poetry run python -B ./src/predict.py