#!/usr/bin/env bash

cd $(dirname $0)

sh python/build.sh
sh golang/build.sh
