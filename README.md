# Code Challenge

# Commands

For testing the connection to the compose database

```
podman-compose up -d
podman exec -it ${DB_CONTAINER_NAME} psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}
```
