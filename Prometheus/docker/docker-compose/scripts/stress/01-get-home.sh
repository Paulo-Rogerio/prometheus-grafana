#!/usr/bin/env bash

for _ in {0..10};
do
  curl -sSL -H "Content-Type: application/json"  http://localhost:3002 | jq .
done
