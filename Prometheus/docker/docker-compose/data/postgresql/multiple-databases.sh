#!/usr/bin/env bash

# set -e
# set -u

function create_user_and_database() {
    local database=$1
    echo "  Creating user and database '$database'"
    psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
        CREATE USER $database;
        CREATE DATABASE $database;
        ALTER USER $database with encrypted password '123456';
EOSQL
}

function grant_database() {
    local database=$1
    echo "  Grant database '$database'"
    psql -v ON_ERROR_STOP=1 --username postgres -d $database <<-EOSQL
        GRANT ALL PRIVILEGES ON DATABASE $database TO $database;
        GRANT ALL ON SCHEMA public TO $database;
EOSQL
}

if [[ -n "$POSTGRES_MULTIPLE_DATABASES" ]]; 
then
    echo "Multiple database creation requested: $POSTGRES_MULTIPLE_DATABASES"
    for db in $(echo $POSTGRES_MULTIPLE_DATABASES | tr ',' ' '); 
    do
        create_user_and_database $db
        grant_database $db
    done
    echo "Multiple databases created"
fi
