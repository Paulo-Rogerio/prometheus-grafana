#!/usr/bin/env bash

count=0
for _ in {0..500};
do
  [[ ${count} == 100 ]] && sleep 3;
  curl \
    -sSL \
    -H 'accept: application/json' \
    http://localhost:3002/flip-coins?times=10 | jq .

  ((count++))  
done

