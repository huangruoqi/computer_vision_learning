FROM python:3.9
WORKDIR /workspaces/computer_vision_learning/code
COPY dist/*.whl /
RUN pip install --no-cache-dir /*.whl && rm -rf /*.whl