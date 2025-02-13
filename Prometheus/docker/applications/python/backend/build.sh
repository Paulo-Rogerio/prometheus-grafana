#!/usr/bin/env bash

cd $(dirname $0)

docker build \
--no-cache \
-t prgs/backend-books:app \
-f Dockerfile .
