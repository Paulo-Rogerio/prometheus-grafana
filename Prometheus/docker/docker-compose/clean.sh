#!/usr/bin/env bash

cd $(dirname $0)

rm -rf data/postgresql/pgdata/*
rm -rf data/monitoring/alertmanager/data/*
rm -rf data/monitoring/grafana/data/*
rm -rf data/monitoring/prometheus/data/*
touch data/postgresql/.keep
touch data/monitoring/alertmanager/data/.keep
touch data/monitoring/grafana/data/.keep
touch data/monitoring/prometheus/data/.keep
