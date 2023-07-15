# Pull base image
FROM python:3.10.4-slim-bullseye
# Copy project
COPY ./main ./main
COPY ./requirements.txt ./requirements.txt
COPY ./start.sh ./start.sh

# Install dependencies
RUN pip install -r requirements.txt