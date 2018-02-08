FROM ubuntu:16.04
MAINTAINER Andrey Fedoseev <andrey.fedoseev@gmail.com>
RUN apt-get update && apt-get install -y python2.7-dev python3.5-dev python-pip
RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r requirements-dev.txt
RUN pip install -e .
