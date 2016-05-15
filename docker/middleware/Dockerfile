FROM ubuntu:latest
ADD . /code
WORKDIR /code 
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN pip install -r requirements.txt
