FROM postgres:alpine
# Copy SQL files to the init directory
COPY ./postgresql/migrations/*.sql /docker-entrypoint-initdb.d/
