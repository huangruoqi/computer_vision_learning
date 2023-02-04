# check for git submodules
$(info abc)
ifneq ($(findstring -, $(shell git submodule status)),)
$(info INFO: Need to initialize git submodules)
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