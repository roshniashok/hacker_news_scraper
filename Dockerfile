
# Base alpine image.
FROM python:3.5-alpine

MAINTAINER Roshini Ashokkumar "rosh813@gmail.com"

# Adding requirement.txt
WORKDIR /app/cli
ADD requirements.txt /app/cli

# Udating dependancies
RUN apk update python3 pip3 && \
    pip3 install --no-cache-dir -r requirements.txt

# Adding source
ADD . /app/cli

# Open a shell
ENTRYPOINT [ "/bin/sh" ]