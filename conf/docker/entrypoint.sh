#!/bin/sh

gunicorn --worker-class aiohttp.worker.GunicornUVLoopWebWorker \
  --workers 2 \
  --bind 0.0.0.0:$NUGC_SERVER_PORT \
  ugc.main:create_app

# Run the main container process
exec "$@"
