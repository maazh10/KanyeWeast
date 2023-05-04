#!/bin/sh

cd /home/server/KanyeWeast

git fetch
git reset --hard origin/$branch

docker compose down && docker compose up -d --build
