#!/usr/bin/env bash

cd $(dirname $0)

sh node/build.sh
sh python/build.sh
