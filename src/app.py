from datetime import datetime, date
from typing import Union, Optional
from fastapi import FastAPI, Query, Depends, HTTPException
from sqlmodel import Session, SQLModel, select
from .models import WxTable
from .database import get_db

app = FastAPI(
    title = "CTVA Weather Station API",
    description = "API for accessing CTVA weather station data and statistics",
    version = "1.0.0"
)

@app.get("/")
def read_root():
    """
    Health check endpoint
    """
    return {"status": "ok", "message": "Weather Station API"}


@app.get("/api/weather")
def get_weather_data(
    site_id:    str            = Query(..., description = "Weather station ID"),
    start_date: Optional[date] = Query(None, description = "Start date (YYYYMMDD)"), # FastAPI converts to date obj
    end_date:   Optional[date] = Query(None, description = "End date (YYYYMMDD)"),
    page:       int            = Query(1, ge = 1, description = "Page Number"),
    limit:      int            = Query(100, ge = 1, le = 1000, description = "Records per page"),
    db:         Session        = Depends(get_db) ):
    """
    Endpoint for the raw extracting wx_data.

    Inputs:
      site_id: string of the station name
      start_date: optional, start date requested
      end_date: optional, end_date requested

    Outputs:
      data: list of weather records
      page: current page number
      limit: Records per page
      total_records: Total number of matching records
      total_pages: total number of pages
    """
    # Query to send to database for site_id input
    query = select(WxTable).where(WxTable.site_id == site_id)
    if start_date: # if optional values given:
        query = query.where(WxTable.date >= start_date)
    if end_date:
        query = query.where(WxTable.date <= end_date)

    query = query.order_by(WxTable.date)

    # Count for pagination
    count_query = select(WxTable).where(WxTable.site_id == site_id)
    if start_date:
        count_query = count_query.where(WxTable.date >= start_date)
    if end_date:
        count_query = count_query.where(WxTable.date <= end_date)
    
    total_records = len(db.exec(count_query).all())

    # Check for site to have data
    if total_records == 0:
        raise HTTPException(
            status_code = 404,
            detail = f"No data found for site_id : {site_id}"
        )

    # Pagination
    total_pages = (total_records + limit - 1) // limit # ceiling division
    offset      = (page - 1) * limit
    query       = query.offset(offset).limit(limit) # apply it

    # Execute query
    results = db.exec(query).all()
    
    # Response
    return {
        "data": results,
        "pagination": {
            "page": page,
            "limit": limit,
            "total_records": total_records,
            "total_pages": total_pages
        }
    }

@app.get("/api/sites")
def get_sites(db: Session = Depends(get_db)):
    """
    Get the list of the unique Weather station ID's in the database tables.
    """
    query = select(WxTable.site_id).distinct()
    sites = db.exec(query).all()

    return {
        "sites": sites,
        "count": len(sites)
    }

@app.get("/api/weather/stats")
def get_site_stats(
    site_id:    str            = Query(..., description = "Weather station ID"),
    start_year: Optional[int] = Query(None, description = "Start year (YYYY)"),
    end_year:   Optional[int] = Query(None, description = "End year (YYYY)"),
    db:         Session        = Depends(get_db) ):
    """
    Endpoint for the yearly summary statistics for each site.
    
    Inputs:
      site_id: string of the station name
      start_date: optional, start date requested
      end_date: optional, end_date requested

    Outputs:
      data: list of weather records
      page: current page number
      limit: Records per page
      total_records: Total number of matching records
      total_pages: total number of pages
    """

    query = select(WxTableStats).where(WxTableStats.site_id == site_id)

    if start_date:
        query = query.where(WxTableStats.year >= start_year)
    if end_date:
        query = query.where(WxTableStats.year <= end_year)

    results = db.exec(query).all()

    if not results:
        raise HTTPException(
            status_code = 404,
            detail = f"No data found for site_id: {site_id}"
        )

    return {
        "data": results
    }