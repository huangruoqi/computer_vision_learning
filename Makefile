setup:
	poetry install
	mkdir video data
run:
	poetry run python -B ./code/main.py

convert:
	poetry run python -B ./code/video_to_3d_positions.py

record:
	poetry run python -B ./code/record_video.py