#!/usr/bin/env bash

cd $(dirname $0)

docker build \
--no-cache \
-t prgs/frontend-books:app \
-f Dockerfile .
