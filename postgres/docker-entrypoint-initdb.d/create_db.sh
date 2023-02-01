#!/bin/bash
set -e

echo "Creating database & user"
psql -v --username "docker" --dbname "radarsys" <<-EOSQL
	CREATE USER docker WITH PASSWORD 'docker';
	CREATE DATABASE radarsys;
	GRANT ALL PRIVILEGES ON DATABASE radarsys TO docker;
EOSQL
