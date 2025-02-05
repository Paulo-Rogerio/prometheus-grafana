#!/usr/bin/env bash

curl -sSL -H "Content-Type: application/json"  http://localhost:3002/book/2 | jq .
