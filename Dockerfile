# This is a comment
FROM ubuntu:14.04

MAINTAINER Denis Torre <denis.torre@mssm.com>

RUN apt-get update && apt-get install -y python
RUN apt-get update && apt-get install -y python-pip
RUN apt-get update && apt-get install -y python-dev

RUN pip install Flask==0.10.1
RUN pip install numpy==1.11.3
RUN pip install pandas==0.19.1
RUN pip install flask-mysql==1.4.0

RUN mkdir datasets2tools
COPY . /datasets2tools

ENTRYPOINT python /datasets2tools/flask/__init__.py