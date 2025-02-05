#!/usr/bin/env bash

count=0
for i in {0..500};
do
  [[ ${count} =~ [0-9]00 ]] && sleep 3;
  curl \
    -sSL \
    -H "Content-Type: application/json"  http://localhost:3002/books/\?search\=Author${i} | jq .
  ((count++))
done
