#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER mediagoblin;
    CREATE DATABASE mediagoblin;
    GRANT ALL PRIVILEGES ON DATABASE mediagoblin TO mediagoblin;
EOSQL