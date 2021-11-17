# docker stop rtvcc > /dev/null 2>&1
# docker image rm rtvcc > /dev/null 2>&1
docker build -t rtvcc .
docker run --name rtvcc \
  -v d:/projects/Real-Time-Voice-Cloning-Containerized/volume:/volume rtvcc
docker rm rtvcc