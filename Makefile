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
	mkdir video data
run:
	poetry run python -B ./code/main.py

convert:
	poetry run python -B ./code/video_to_3d_positions.py

record:
	poetry run python -B ./code/record_video.py

hand:
	poetry run python -B ./code/hand.py

check-and-reinit-submodules:
	@if git submodule status | egrep -q '^[-]|^[+]' ; then \
		echo ""; \
	fi