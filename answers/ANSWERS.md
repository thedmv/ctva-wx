# CTVA Exercise

Below are the specific answers to the Problems in the coding exercise summarized in a single document.

## Problem 1 - Data Modelling

- For our database I chose PostgreSQL, with the PostGIS extension to enable future geospatial operations such as saving the geospatial coordinates of the stations.
- For our data model we chose the SQLModel ORM framework (`models.py`).

## Problem 2 - Ingestion

- We ingested the weather data by using Pandas to explore and sanitize our data.
- The data was checked in (`Analysis.ipynb`) for duplication by checking if duplicate dates were found. None were found.
- For the logs of the ingestion we create a file `/code/src/log.out` as part of the service. As of this writing, the log file stops at about 85124 lines and took about 4-5mins for the ingestion to finish

## Problem 3 - Data Analysis

- Check `models.py` for the full details of the data models.
- The data (both the raw wx_data/ and the stats table) is processed in `main.py` using `ingest.py`.
- For the missing data, and their involvement in the statistics I have verified that the Pandas "mean" and "sum" functions ignore null values by default, but they need to be of type pd.NA (or a numpy NaN). However, the null values for ingestion need to be `None`, hence the replacements in those scripts.

## Problem 4 - REST API

- The work for this is in app.py. Here we use FastAPI to implement the API.
- I added an endpoint for the sites so that those can be queried separately.
