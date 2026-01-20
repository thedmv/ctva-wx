import pandas as pd
import numpy as np
from config import FILES_WXDATA as FILES
from functions import read_wxdata
from models import WxTable, WxTableStats
from database import engine
from sqlmodel import Session
from sqlalchemy import insert # optimal for larger datasets

def ingest_wxdata():
    """
    Ingest data files for /code/wx_data. See config.py for paths
    """
    cols = [k for k in WxTable.model_fields.keys()]
    with Session(engine) as session:
        for f in FILES:
            DF = read_wxdata(f)
            # Create aggregates
            DFstats = DF.groupby(["site_id", DF["date"].dt.year])\
                        .agg(
                            tmax_yearly   = ("tmax", "mean"),
                            tmin_yearly   = ("tmin", "mean"),
                            precip_yearly = ("precip", "sum") )\
                        .reset_index()
            rows_stats = DFstats.to_dict(orient = "records")
            # Insert WxTableStats
            DFstats = DFstats.replace(pd.NA, None).rename(columns = {"date": "year"})
            DFstats["year"] = pd.to_datetime(DFstats["year"], format = "%Y")
            session.execute(insert(WxTableStats), DFstats.to_dict(orient = "records"))
            
            # Insert WxTable
            DF = DF.replace(pd.NA, None)
            session.execute(insert(WxTable), DF.to_dict(orient = "records"))
            session.commit()