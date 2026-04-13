#!/bin/bash
# Shipsmart Spark Cluster Startup Script

echo "=========================================="
echo "Shipsmart Spark Cluster Startup"
echo "=========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "ERROR: docker-compose is not installed"
    exit 1
fi

# Function to start cluster
start_cluster() {
    echo "[1/3] Starting Spark cluster..."
    docker-compose -f docker/spark-compose.yml up -d
    echo "[2/3] Waiting for Spark to be ready..."
    sleep 10
    echo "[3/3] Spark cluster started!"
    echo ""
    echo "Spark Master UI: http://localhost:8080"
    echo "Spark Worker 1: http://localhost:8081"
}

# Function to stop cluster
stop_cluster() {
    echo "[1/1] Stopping Spark cluster..."
    docker-compose -f docker/spark-compose.yml down
}

# Function to check status
status_cluster() {
    echo "Checking Spark cluster status..."
    docker ps --filter "name=shipsmart-spark"
}

# Parse command
case "${1:-start}" in
    start)
        start_cluster
        ;;
    stop)
        stop_cluster
        ;;
    restart)
        stop_cluster
        sleep 5
        start_cluster
        ;;
    status)
        status_cluster
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac