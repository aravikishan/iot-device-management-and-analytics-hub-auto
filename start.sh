#!/bin/bash
set -e
echo "Starting IoT Device Management and Analytics Hub..."
uvicorn app:app --host 0.0.0.0 --port 9070 --workers 1
