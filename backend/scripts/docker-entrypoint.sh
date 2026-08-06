#!/bin/sh
set -e

echo "Running database migrations and seeds..."
python scripts/init_db.py
exec "$@"
