#!/usr/bin/env bash

count=0
for i in {1..10};
do
  [[ ${count} =~ [0-9]00 ]] && echo "===== sleep =====" && sleep 10;

  curl -sSL \
      -H "Content-Type: application/json" \
      -X POST \
      -d '{
          "title": "'Titulo$i'",
          "author": "'Author$i'",
          "category": "suspense"
      }' http://localhost:3002/book | jq .

  echo "-----------------"
  ((count++))

done
