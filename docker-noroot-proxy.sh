#!/bin/bash
/bin/sudo /usr/bin/socat \
  UNIX-LISTEN:/var/run/docker.sock,fork,mode=660,user=nuvolaris \
  UNIX-CONNECT:/var/run/docker-host.sock

