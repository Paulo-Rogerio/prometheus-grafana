#!/usr/bin/env bash

count=0
for _ in {1..10};
do
  [[ ${count} =~ [0-9]000 ]] && echo "===== sleep =====" && sleep 10;
  curl -sSL \
      -H "Content-Type: application/json" \
      -X GET  http://localhost:3003/library/random_status | jq .
  ((count++))
done

