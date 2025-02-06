#!/usr/bin/env bash

cd $(dirname $0)

docker-compose down \
&& sh clean.sh \
&& docker-compose up -d 
