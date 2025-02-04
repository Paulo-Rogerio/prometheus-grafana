#!/usr/bin/env bash

cd $(dirname $0)

docker build \
--no-cache \
-t prgs/telegrambot:app \
-f Dockerfile .
