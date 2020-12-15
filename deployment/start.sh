#!/bin/bash
app="jeec_brain"
docker build -t ${app} .
docker run -d -p 8081:80 \
  --name=${app} \
  -v $PWD:/app ${app}
