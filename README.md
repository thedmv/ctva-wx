# CTVA Code Challenge

## Summary of Architecture

The purpose of this repo is to develop a REST API with endpoints pointing to retrieve raw weather data and another pointing to yearly statistical summaries. The chosen architecture for this was to use Pandas for data exploration, PostgreSQL for our database, SQLModel for data modeling and ingestion, and FastAPI as our framework for the REST API. This will happen using containers built using `podman`/`podman-compose`.

Note: Although un-tested at the moment, Apple CPU architecture may require specific tuning for the containers to be built in those environments. Development of this project was initially done on Windows 11 using Podman installed on Powershell. `docker`/`docker-compose` should be interchangeable with `podman`/`podman-compose` for all instances below.

## Data Considerations

Here we focus on the weather data in `./wx_data/`. The units of the data (both raw and statistical summaries) were kept in their original units.

## Installation

### 1. Base Container

We start by building the container in `Dockerfile`. This container is specifically built for geospatial applications that use GDAL and Python packages such as GeoPandas. In past experience, different versions of GDAL maybe be packaged with different Python packages. This container ensures that there is a single installation of GDAL and that all the relevant Python packages use that version.

For building the main image that is used for the debug and app containers, we first run,

```
podman build -t cwx .
```

This may take about 3-5 mins to finish successfully.

### 2. podman-compose yml

We will be setting up 4 different services for this application. Below we use their respective `service`/`container_name`. The details can be found in `docker-compose.yml`.

1. `db`/`cdb`: service for the PostgreSQL (with the PostGIS extension) database
1. `dev`/`debug`: container with a JupyterLab session for testing and development
1. `ingest`/`ingest`: container that ingests data into the database
1. `app`/`app`: container that runs the API using FastAPI.

Next we will compose our application:

```
podman-compose up -d
```

After the compose runs successfully we move on to verifying that our services worked successfully.

## Checking Installation

### 1. Testing `docker-compose.yml` services

The code blocks show what the logs are for a successful service.

```
>> podman logs cdb --tail 10
PostgreSQL Database directory appears to contain a database; Skipping initialization

2026-01-20 16:36:09.438 UTC [1] LOG:  starting PostgreSQL 17.5 (Debian 17.5-1.pgdg110+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 10.2.1-6) 10.2.1 20210110, 64-bit
2026-01-20 16:36:09.438 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
2026-01-20 16:36:09.438 UTC [1] LOG:  listening on IPv6 address "::", port 5432
2026-01-20 16:36:09.448 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
2026-01-20 16:36:09.458 UTC [26] LOG:  database system was shut down at 2026-01-20 04:39:23 UTC
2026-01-20 16:36:09.526 UTC [1] LOG:  database system is ready to accept connections
```

```
>> podman logs debug --tail 10
I 2026-01-20 16:36:26.408 ServerApp]     http://127.0.0.1:50000/lab?token=e4af4a83ee76e269f5ebbaf75f64eee363dcab58928870af
[I 2026-01-20 16:36:26.408 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 2026-01-20 16:36:26.411 ServerApp]

    To access the server, open this file in a browser:
        file:///home/dev/.local/share/jupyter/runtime/jpserver-1-open.html
    Or copy and paste one of these URLs:
        http://558da37706d0:50000/lab?token=e4af4a83ee76e269f5ebbaf75f64eee363dcab58928870af
        http://127.0.0.1:50000/lab?token=e4af4a83ee76e269f5ebbaf75f64eee363dcab58928870af
[I 2026-01-20 16:36:26.440 ServerApp] Skipped non-installed server(s): basedpyright, bash-language-server, dockerfile-language-server-nodejs, javascript-typescript-langserver, jedi-language-server, julia-language-server, pyrefly, pyright, python-language-server, python-lsp-server, r-languageserver, sql-language-server, texlab, typescript-language-server, unified-language-server, vscode-css-languageserver-bin, vscode-html-languageserver-bin, vscode-json-languageserver-bin, yaml-language-server
```

For the ingest, since the container logs are empty we check the contents of the database directly

```
>> podman exec -it ${DB_CONTAINER_NAME} psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}
```

or

```
>> podman exec -it cdb psql -U uctva -d cwx_database
```

And then we list the tables:

```
>> \dt
                 List of relations
  Schema  |           Name           | Type  | Owner
----------+--------------------------+-------+-------
 public   | spatial_ref_sys          | table | uctva
 public   | wxtable                  | table | uctva <<<
 public   | wxtablestats             | table | uctva <<<
 ...
```

And quickly inspect the first rows for each of the tables we create:

```
cwx_database=# select * from wxtable limit 5;
 id |   site_id   |        date         | tmax | tmin | precip
----+-------------+---------------------+------+------+--------
  1 | USC00110072 | 1985-01-01 00:00:00 |  -22 | -128 |     94
  2 | USC00110072 | 1985-01-02 00:00:00 | -122 | -217 |      0
  3 | USC00110072 | 1985-01-03 00:00:00 | -106 | -244 |      0
  4 | USC00110072 | 1985-01-04 00:00:00 |  -56 | -189 |      0
  5 | USC00110072 | 1985-01-05 00:00:00 |   11 |  -78 |      0
(5 rows)

cwx_database=# select * from wxtablestats limit 5;
 id |   site_id   |        year         | tmax_yearly | tmin_yearly | precip_yearly
----+-------------+---------------------+-------------+-------------+---------------
  1 | USC00110072 | 1985-01-01 00:00:00 |         153 |          43 |          7801
  2 | USC00110072 | 1986-01-01 00:00:00 |         127 |          22 |          5053
  3 | USC00110072 | 1987-01-01 00:00:00 |         178 |          63 |          7936
  4 | USC00110072 | 1988-01-01 00:00:00 |         173 |          45 |          5410
  5 | USC00110072 | 1989-01-01 00:00:00 |         157 |          40 |          7937
(5 rows)
```

We can also do other checks on our work thus far if we wish, such as inspecting the size of our database volume,

```
podman-compose exec db du -sh /var/lib/postgresql/data
```

### 2. Testing API Endpoints

Now that our application is built, we can test the endpoints with the commands below.

```
# Get data for a specific site
curl "http://localhost:8000/api/weather?site_id=USC00111436&page=1&limit=10"

# With date filtering
curl "http://localhost:8000/api/weather?site_id=USC00111436&?start_date=2020-01-01&?end_date=2020-12-31&?page=1&?limit=50"

# List all sites
curl "http://localhost:8000/api/sites"

# Get statistics
curl "http://localhost:8000/api/weather/stats?site_id=USC00111436"
```

FastAPI provides automatic documentation via the URL's below.

```
http://localhost:8000/docs
http://localhost:8000/redoc
```

### 3. Running Tests

Tests use pytest.

```
python -m pytest src/tests/tests.py
```

## Summary Table

In the top-level directory we keep the files for containerization and environment variables.

| Filename                | Purpose                              |
| ----------------------- | ------------------------------------ |
| docker-compose.yml      | Container orchestration              |
| Dockerfile              | Container definition                 |
| .env                    | Environment Variables                |
| verify_gdal_bindings.py | Verifies GDAL bindings in containers |

Within the `./src` folder we contain our workflow scripts. Note that `Analysis.ipynb` is a scratch space for debugging and testing.

| Filename     | Purpose                                        |
| ------------ | ---------------------------------------------- |
| app.py(\*)   | Runs the API service                           |
| config.py    | For hard-coded values (e.g. Paths, metadata)   |
| database.py  | DB connection management                       |
| functions.py | Utilitiy functions                             |
| ingest.py    | Data loading functions                         |
| main.py(\*)  | Main program for creating the db and ingesting |
| models.py    | Data models                                    |

Asterisks (\*) indicate the scripts that are directly ran by our services.
