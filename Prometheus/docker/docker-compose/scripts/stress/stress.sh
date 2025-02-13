#!/usr/bin/env bash

cd $(dirname $0)

rm -rf __pycache__

locust --headless --users 35 --spawn-rate 3 -H http://localhost:3003
