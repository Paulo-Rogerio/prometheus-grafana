#!/usr/bin/env bash

count=0
for i in {1..10};
do
  [[ ${count} =~ [0-9]000 ]] && echo "===== sleep =====" && sleep 10;
   curl \
    -sSL \
    -H "Content-Type: application/json"  http://localhost:3003/library/book/\?search\=Titulo${i} | jq .
  ((count++))
done





