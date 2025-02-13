#!/usr/bin/env bash

curl -sSL -H "Content-Type: application/json"  http://localhost:3003/library/books | jq .



