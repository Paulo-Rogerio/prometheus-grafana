#!/usr/bin/env bash

curl -sSL -H 'accept: application/json' \
     -X 'DELETE' 'http://localhost:3002/book/delete?id=1' | jq .
