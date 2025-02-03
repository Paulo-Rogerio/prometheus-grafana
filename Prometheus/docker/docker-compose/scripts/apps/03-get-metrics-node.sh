#!/usr/bin/env bash

curl \
  -sL \
  -X 'GET' \
  -H 'accept: application/json' \
  http://localhost:3001/metrics
