#!/bin/bash
set -e

echo "Creating database & user"
psql -v --username "postgres" --dbname "postgres" <<-EOSQL
	CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
	CREATE DATABASE $DB_NAME;
	GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOSQL
