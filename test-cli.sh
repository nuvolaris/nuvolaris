#!/bin/bash
VERSION="${1:?version}"
EXT="tar.gz"
EXTRACT="tar xzvf"

case "$(arch)" in
  x86_64) ARCH=amd64 ;;
  arm64) ARCH=arm64 ;;
  *) echo "unknown architecture"; exit 1 ;;
esac

case "$(uname)" in
    Darwin) OS="darwin" ;;
    Linux) OS="linux" ;;
    MINGW*)
        OS="windows"
        EXT="zip"
        ARCH="amd64"
        EXTRACT="unzip -o"
    ;;
    *) echo "unknown platform"; exit 1 ;;
esac

URL="https://github.com/nuvolaris/nuvolaris-cli/releases/download/$VERSION/nuv-$VERSION-$OS-$ARCH.$EXT"

mkdir tmp$$
cd tmp$$

curl -sL $URL >dld.$EXT
$EXTRACT "dld.$EXT"

./nuv devcluster destroy
./nuv setup --devcluster

echo 'function main(args) { return { "body": "OK" } }' >ok.js
./nuv action create ok ok.js --web true
URL="$(./nuv url ok)"

if curl -sL $URL | grep OK
then echo "SUCCESS"; exit 0
else echo "FAILED" ; exit 1
fi
