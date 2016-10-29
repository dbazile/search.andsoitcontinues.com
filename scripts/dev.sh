#!/bin/bash

cd $(dirname $(dirname $0))  # Return to project root

if [ "$PORT" == "" ]; then
  PORT=5000
fi

REPO_URL="file:///Users/david/Code/dbazile.github.io" \
gunicorn asic_search.server:server \
  --bind 0.0.0.0:$PORT \
  --reload \
  --worker-class aiohttp.worker.GunicornWebWorker \
