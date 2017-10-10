#!/bin/bash

cd $(dirname $(dirname $0))  # Return to project root

if [ "$PORT" == "" ]; then
	PORT=5000
fi

. venv/bin/activate

export REPO_URL=~/code/bazile.org

gunicorn search.server:app \
	--bind localhost:$PORT \
	--reload
