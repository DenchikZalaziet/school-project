#!/bin/bash
set -e

echo "Waiting for MongoDB to start"
until mongosh --eval "print(\"waited for connection\")" 2>/dev/null; do
    sleep 1
done

echo "Starting restore"
mongorestore /docker-entrypoint-initdb.d/dump/ || echo "Restore failed"

echo "Restore completed!"
