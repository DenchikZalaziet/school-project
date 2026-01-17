FROM mongo:latest

COPY ./dump /docker-entrypoint-initdb.d/dump/

COPY ./restore.sh /docker-entrypoint-initdb.d/restore.sh
RUN chmod +x /docker-entrypoint-initdb.d/restore.sh
