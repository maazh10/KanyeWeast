#!/bin/sh

cd /home/server/KanyeWeast

git fetch
git reset --hard HEAD
git merge origin/main

docker compose down && docker compose up -d --build
