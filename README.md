# Code Challenge

# Rationales

1. Units: We will stay with the units defined in the problem statement of "tenths" of a degree. The choice here is to faithfully represent the raw data in the database.

# Commands

For building the main image that is used for the debug and app containers.

```
podman build -t cwx .
```

For testing the connection to the compose database

```
podman-compose up -d
podman exec -it ${DB_CONTAINER_NAME} psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}
```

or

```
podman exec -it cdb psql -U uctva -d cwx_database
```

For inspecting the size of the database volume:

```
podman-compose exec db du -sh /var/lib/postgresql/data
```

For testing the endpoints

```
# Get data for a specific site
curl "http://localhost:8000/weather?site_id=USC00111436&page=1&limit=10"

# With date filtering
curl "http://localhost:8000/weather?site_id=USC00111436&start_date=2020-01-01&end_date=2020-12-31&page=1&limit=50"

# List all sites
curl "http://localhost:8000/sites"

# Get statistics
curl "http://localhost:8000/weather/stats/USC00111436"
```

For looking at the documentation

```
http://localhost:8000/docs
http://localhost:8000/redocs
```
