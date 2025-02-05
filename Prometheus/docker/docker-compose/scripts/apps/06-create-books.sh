#!/usr/bin/env bash

for i in {6..500};
do
  curl -sSL \
      -H "Content-Type: application/json" \
      -X POST \
      -d '{
          "id": '$i',
          "title": "'Titulo$i'",
          "author": "'Author$i'",
          "category": "suspense"
      }' http://localhost:3002/book/create | jq .

  [[ $? -eq 0 ]] && echo "sucessfully" || echo "error"
done
