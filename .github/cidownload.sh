#!/bin/bash
TAG="${1:?version}"
VER="${TAG#refs/*/}"
PRE="https://github.com/nuvolaris/nuvolaris-cli/releases/download"
wget -nc $PRE/$VER/nuv-windows-amd64.zip
wget -nc $PRE/$VER/nuv-windows-amd64.zip.md5
for OS in linux darwin
do for ARC in amd64 arm64
   do wget -nc $PRE/$VER/nuv-$VER-$OS-$ARC.tar.gz
      wget -nc $PRE/$VER/nuv-$VER-$OS-$ARC.tar.gz.md5
   done
done


