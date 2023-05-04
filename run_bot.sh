#!/bin/sh

cd /home/server/KanyeWeast

branch=$(git rev-parse --abbrev-ref HEAD)

latest_commit=$(git rev-parse HEAD)

remote_commit=$(git ls-remote $(git config --get remote.origin.url) refs/heads/$branch | awk '{ print $1 }')

if [ $latest_commit != $remote_commit || "$1" == "--force" ]; then
    git fetch
    git reset --hard origin/$branch

    docker compose down && docker compose up -d --build
    docker compose logs -f
fi
