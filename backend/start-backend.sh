#!/bin/bash

set -e

exec gunicorn --bind "0.0.0.0:${PORT:-5555}" --workers "${WEB_CONCURRENCY:-2}" --access-logfile - app:app