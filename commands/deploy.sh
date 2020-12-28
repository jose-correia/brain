docker stop jeec_brain_1
docker rm jeec_brain_1
docker build --tag jeec_brain:latest .
docker run -p 8081:8081 --name jeec_brain_1 -d jeec_brain:latest
