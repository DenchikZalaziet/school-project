#!/bin/bash
set -e

MAX_WAIT=60
DUMP_DIR="/docker-entrypoint-initdb.d/dump"
WAIT_COUNT=0

echo "Waiting for MongoDB to start (max ${MAX_WAIT}s)"

while [ $WAIT_COUNT -lt $MAX_WAIT ]; do
    if mongosh --eval "db.adminCommand('ping')" --quiet >/dev/null 2>&1; then
        echo "MongoDB is ready"
        break
    fi
    
    WAIT_COUNT=$((WAIT_COUNT + 1))
    
    if [ $WAIT_COUNT -eq $MAX_WAIT ]; then
        echo "Timeout: MongoDB not available after ${MAX_WAIT} seconds" >&2
        exit 1
    fi
    
    echo "  Still waiting... (${WAIT_COUNT}/${MAX_WAIT}s)"
    sleep 1
done

if [ ! -d "$DUMP_DIR" ]; then
    echo "Dump directory not found: $DUMP_DIR"
    echo "Skipping restore"
    exit 0
fi

if [ -z "$(ls -A $DUMP_DIR 2>/dev/null)" ]; then
    echo "Dump directory is empty: $DUMP_DIR"
    echo "Skipping restore"
    exit 0
fi

echo "Starting MongoDB restore from: $DUMP_DIR"

if mongorestore "$DUMP_DIR" --quiet; then
    echo "Restore completed successfully"
else
    echo "Restore failed with exit code: $?" >&2
    exit 1
fi
