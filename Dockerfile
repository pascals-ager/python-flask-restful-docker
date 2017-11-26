FROM python:3.6.3-jessie
MAINTAINER Advith Nagappa <advith.nagappa@gmail.com>

RUN apt-get update && apt-get install -qq -y build-essential libpq-dev postgresql-client-9.4 --fix-missing --no-install-recommends


ENV INSTALL_PATH /home/vimcar

ENV ENV_SETTINGS 'TestConfig'

RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN groupadd vimcargroup && useradd -m -g vimcargroup -s /bin/bash vimcar

RUN chown -R vimcar:vimcargroup /home/vimcar

USER vimcar

#CMD gunicorn -b 0.0.0.0:8000 "app:create_app('TestConfig')"