#!/bin/bash

git pull

docker stop jeec_brain_dev
docker rm jeec_brain_dev
docker build -t jeec_brain:dev .
docker run --name jeec_brain_dev -d -p 8083:8081 jeec_brain:dev
