#!/usr/bin/env bash

count=0
for _ in {0..1000};
do
  [[ ${count} =~ [0-9]00 ]] && echo "===== sleep =====" && sleep 10;
  curl -sSL -H "Content-Type: application/json"  http://localhost:3002 | jq .
  ((count++))
done
