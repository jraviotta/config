#!/bin/bash

docker run -d \
    -v "../${PWD}:/workspace" \
    -p 8080:8080 \
    --name "ml-workspace" \
    --env AUTHENTICATE_VIA_JUPYTER="jupyter" \
    --shm-size 12g \
    --restart always \
    dagshub/ml-workspace:latest
