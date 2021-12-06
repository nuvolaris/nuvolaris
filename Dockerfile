FROM ubuntu:20.04 as builder
# download required component
ENV DOCKER_URL=https://download.docker.com/linux/static/stable/x86_64/docker-18.06.3-ce.tgz
ENV WSK_URL=https://github.com/apache/openwhisk-cli/releases/download/1.2.0/OpenWhisk_CLI-1.2.0-linux-amd64.tgz
RUN apt-get update && apt-get -y install curl
RUN curl -sL $DOCKER_URL | tar xzvf -
RUN curl -sL $WSK_URL | tar xzvf -

FROM ubuntu:20.04
# configure timezone and configutations
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# add required software packaged
COPY --from=builder /docker/docker /usr/bin/docker
COPY --from=builder /wsk /usr/bin/wsk
RUN apt-get update &&\
 apt-get -y install \
   lsb-release \
   apt-utils \
   software-properties-common \
   build-essential \
   ca-certificates \
   git gnupg curl wget \
   zlib1g-dev libbz2-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev
# add java (amazon corretto)   
RUN wget -O- https://apt.corretto.aws/corretto.key | apt-key add - && \
  add-apt-repository 'deb https://apt.corretto.aws stable main' && \
  apt-get update && \
  apt-get install -y java-11-amazon-corretto-jdk
# setup and initialize the work environment
RUN useradd -m nuvolaris
USER nuvolaris
RUN git clone https://github.com/nuvolaris/nuvolaris /home/nuvolaris/nuvolaris
WORKDIR /home/nuvolaris
RUN /bin/bash -c 'source nuvolaris/setup.source'
RUN echo '. nuvolaris/setup.source' >.bashrc
CMD /bin/bash
