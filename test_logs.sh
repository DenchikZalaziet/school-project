#!/bin/bash
echo "=== Testing Docker Compose Logs ==="
echo "1. Checking if containers are running..."
docker-compose -f docker-compose.production.yml ps

echo -e "\n2. Testing backend health endpoint..."
curl -f http://localhost:8080/api/health || echo "Health check failed"

echo -e "\n3. Showing recent logs from all services..."
docker-compose -f docker-compose.production.yml logs --tail=20

echo -e "\n4. Checking nginx access logs..."
if [ -f "./nginx/logs/access.log" ]; then
    tail -5 ./nginx/logs/access.log
else
    echo "Nginx access log not found"
fi

echo -e "\n=== Log test complete ==="

read -p "Press Enter to close this window"
