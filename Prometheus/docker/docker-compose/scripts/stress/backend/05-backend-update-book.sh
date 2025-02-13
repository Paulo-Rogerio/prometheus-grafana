#!/usr/bin/env bash

curl -sSL -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -X 'PUT' \
  -d '{
        "title": "Fulano1",
        "author": "Fulano1",
        "category": "comedia"
    }' 'http://localhost:3002/book/1' | jq .
