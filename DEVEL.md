# Developer Guide

This document describes development procedures.

# Prequequisite

Development happens in **modern** Unix-like environments. Basically, we are supporting OSX, Linux and Windows WSL. 

You need to preinstall Java v8 or v11 and C Development tools. Other tools are installed with a script we provide.

And you need to install Docker 

For Java, we use [Amazon Corretto](https://docs.aws.amazon.com/corretto/index.html), but you can use any other Java distribution.

Procedures to install development tools:

- OSX: `xcode-select --install`
- Debian or Ubuntu: `sudo apt-get install build-essential procps curl file git`
- Fedora, CentOS, or Red Hat: `sudo yum groupinstall 'Development Tools' && sudo yum install procps-ng curl file git`

# Checking out and setup

Start with

```
git clone --recurse-submodules https://github.com/nuvolaris/nuvolaris
cd nuvolaris
source setup.source
```

And you are ready!
