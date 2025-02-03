#!/usr/bin/env bash

cd $(dirname $0)

docker build \
--no-cache \
-t prgs/python:app \
-f Dockerfile .
