FROM python:3
USER root
RUN apt-get update
WORKDIR /setup/
COPY requirements.txt /setup
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

