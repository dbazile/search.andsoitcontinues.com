#!/bin/bash

cd $(dirname $(dirname $0))  # Return to project root

if [ "$PORT" == "" ]; then
  PORT=5000
fi

. .env/bin/activate

export REPO_URL="file:///Users/david/code/andsoitcontinues.com"
gunicorn asic_search.server:server \
  --bind localhost:$PORT \
  --reload
