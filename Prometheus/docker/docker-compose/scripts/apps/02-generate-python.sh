#!/usr/bin/env bash

for _ in {0..10};
do
  curl \
    -sSL \
    -H 'accept: application/json' \
    http://localhost:3002/flip-coins?times=10 | jq .
done

