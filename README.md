# Code Challenge

# Rationales

1. Units: We will stay with the units defined in the problem statement of "tenths" of a degree. The choice here is to faithfully represent the raw data in the database.

# Commands

For testing the connection to the compose database

```
podman-compose up -d
podman exec -it ${DB_CONTAINER_NAME} psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}
```
