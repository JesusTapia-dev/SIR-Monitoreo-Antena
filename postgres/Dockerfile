FROM postgres:14.6-alpine
#FROM library/postgres

RUN mkdir -p "$PGDATA" && chmod 700 "$PGDATA"
#COPY ./init.sql /docker-entrypoint-initdb.d/
COPY init.sql /docker-entrypoint-initdb.d/