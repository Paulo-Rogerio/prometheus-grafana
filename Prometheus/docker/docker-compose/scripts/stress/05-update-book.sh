#!/usr/bin/env bash

curl -sSL -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -X 'PUT' \
  -d '{
        "id": 1,
        "title": "Titulo1",
        "author": "Fulano",
        "category": "comedia"
    }' 'http://localhost:3002/book/update' | jq .