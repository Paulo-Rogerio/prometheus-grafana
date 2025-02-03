#!/usr/bin/env bash

curl \
  -sL \
  -X 'GET' \
  -H 'accept: application/json' \
  http://localhost:9093/api/v2/alerts | jq .
