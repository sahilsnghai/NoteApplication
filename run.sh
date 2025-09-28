#!/bin/bash

APP_NAME="fastapi-notes"
DB_CONTAINER="notes-mysql"

# alembic revision --autogenerate -m "Initial migration"

# Function to stop MySQL container
cleanup() {
    echo ""
    echo "Stopping MySQL container..."
    docker stop $DB_CONTAINER
    exit 0
}

# Trap Ctrl+C (SIGINT) and call cleanup
trap cleanup SIGINT

case "$1" in
  up)
    echo "Starting MySQL container..."
    docker ps -a --format '{{.Names}}' | grep -Eq "^${DB_CONTAINER}\$"
    if [ $? -eq 0 ]; then
      docker start $DB_CONTAINER
    else
      docker run --name $DB_CONTAINER \
        -e MYSQL_DATABASE=notesdb \
        -e MYSQL_USER=notesuser \
        -e MYSQL_PASSWORD=notespwd \
        -e MYSQL_ROOT_PASSWORD=rootpwd \
        -p 3306:3306 \
        -v notes_db_data:/var/lib/mysql \
        -d mysql:8.0
    fi

    echo "Starting FastAPI app..."
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ;;

  down)
    echo "Stopping FastAPI app (manual: Ctrl+C if running in foreground)"
    cleanup
    ;;

  *)
    echo "Usage: $0 {up|down}"
    ;;
esac
