FROM docker.uclv.cu/python:latest

COPY ./requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

RUN apt update

RUN apt install spim -y

RUN mkdir cool-compiler-2021

WORKDIR /cool-compiler-2021
