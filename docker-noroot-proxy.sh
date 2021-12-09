#!/bin/bash
sudo socat \
  UNIX-LISTEN:/var/run/docker.sock,fork,mode=660,user=nuvolaris \
  UNIX-CONNECT:/dev/run/docker-host.sock 2>&1 |\
  sudo tee -a /var/log/socat.log > /dev/null &
exec "$@"
