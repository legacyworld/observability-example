FROM python:3.10-slim
USER root
WORKDIR /src
COPY ./requirements.txt .
COPY ./ /src/services
RUN apt-get update
RUN apt-get -y install g++
RUN pip3 install -r requirements.txt
WORKDIR /src