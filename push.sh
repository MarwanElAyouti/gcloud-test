#!/bin/bash

TARGET_SERVICE=$1
if [ "$TARGET_SERVICE" = "server" ]; then
    SERVICE_NAME="marwanelayouti/friendlyeats-server"
    DOCKERFILE_PATH="./services/friendlyeats-server"
fi
if [ "$TARGET_SERVICE" = "frontend" ]; then
    SERVICE_NAME="marwanelayouti/friendlyeats-frontend"
    DOCKERFILE_PATH="./services/friendlyeats-frontend"
fi

docker build  --platform linux/amd64 "$DOCKERFILE_PATH" -t "$SERVICE_NAME"

docker tag "$SERVICE_NAME" "$SERVICE_NAME"

docker push "docker.io/$SERVICE_NAME"
