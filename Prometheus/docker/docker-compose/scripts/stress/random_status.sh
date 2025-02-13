#!/usr/bin/env bash

count=0
for _ in {1..100};
do
  curl -sSL \
      -H "Content-Type: application/json" \
      -X GET  http://localhost:3003/library/random_status | jq .
  ((count++))
done

