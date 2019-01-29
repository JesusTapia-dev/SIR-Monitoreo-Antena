#!/bin/env bash
echo "Creating database..."
psql -U postgres -c "CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';"
psql -U postgres -c "CREATE DATABASE $POSTGRES_DB_NAME;"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB_NAME to $POSTGRES_USER;"
