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
	poetry install ; mkdir video data
run:
	poetry run python -B ./src/main.py

convert:
#	poetry run python -B ./code/video_to_3d_positions.py
	poetry run python -B ./index.py

record:
	poetry run python -B ./src/record_video.py

hand:
	poetry run python -B ./src/hand.py

black:
	poetry run black ./
