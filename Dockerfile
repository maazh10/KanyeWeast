FROM alpine:latest as git

RUN apk add git

COPY .git .

RUN git log -1 --format='%h %s' > commit_message.txt


FROM python:3.10-slim-buster

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

COPY lyrics ./lyrics
COPY roasts.txt .
COPY play.mp3 .
COPY --from=git commit_message.txt .

COPY cogs ./cogs
COPY main.py .

# Run app.py when the container launches
ENV RUNNING_IN_DOCKER=1
CMD ["python", "main.py"]
