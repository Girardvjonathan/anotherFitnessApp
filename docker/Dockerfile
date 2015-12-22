FROM ubuntu:14.04
MAINTAINER Jonathan Girard
RUN apt-get update && apt-get install -y \
	python3-dev \
	python3-pip \
	git \
	vim \
	ssh \
	curl \
	python-pip \
	python-dev \
	nano \
	libpq-dev \
	python-dev \
    nginx

## install our code
RUN mkdir /docker
RUN mkdir /code
WORKDIR /docker
ADD . /docker/

ENTRYPOINT ["./docker-entrypoint.sh"]