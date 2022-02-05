FROM ubuntu:18.04
MAINTAINER Andrey Fedoseev <andrey.fedoseev@gmail.com>
RUN apt-get update && \
    apt-get install -y \
    python3.6-dev \
    python3.8-dev \
    python3-pip
RUN mkdir /app
WORKDIR /app
ADD requirements-*.txt /app/
RUN pip3 install -r requirements-dev.txt
ADD . /app/
RUN pip3 install -e .
