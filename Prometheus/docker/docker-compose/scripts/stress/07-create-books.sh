#!/usr/bin/env bash

count=0
for i in {6..1000};
do
  [[ ${count} =~ [0-9]00 ]] && echo "===== sleep =====" && sleep 10;

  curl -sSL \
      -H "Content-Type: application/json" \
      -X POST \
      -d '{
          "id": '$i',
          "title": "'Titulo$i'",
          "author": "'Author$i'",
          "category": "suspense"
      }' http://localhost:3002/book/create | jq .

  echo "-----------------"
  ((count++))

done
