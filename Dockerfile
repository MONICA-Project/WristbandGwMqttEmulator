FROM python:3.7
ARG BUILD_DATE
LABEL build-date=$BUILD_DATE
LABEL author="Luca Mannella"

WORKDIR /wb_mqtt_emulator
EXPOSE 8000

COPY * /wb_mqtt_emulator/
#COPY setup.py /wb_mqtt_emulator

# RUN apk add libc-dev
# RUN apt-get -y install build-essential
RUN pip install -U pip
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install -e /wb_mqtt_emulator

# Enabling bash and utilities
RUN apt-get -y install bash

### local testing:
ENTRYPOINT python3 ./appmanager.py
