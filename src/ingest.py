import pandas as pd
import numpy as np
from config import FILES_WXDATA as FILES, logger
from functions import read_wxdata
from models import WxTable, WxTableStats
from database import engine
from sqlmodel import Session
from sqlalchemy.dialects.postgresql import insert # optimal for larger datasets

def ingest_wxdata():
    """
    Ingest data files for /code/wx_data. Create the summary statistics table. 
    See config.py for paths
    """

    # Logging initialization and total record counters
    start_ts = pd.Timestamp.utcnow() # for elapsed time
    logger.info("Ingest_wxdata start")
    total_wx_rows = 0
    total_stats_rows = 0

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

            # Match data model with units and data types
            DFstats["tmax_yearly"]   = DFstats["tmax_yearly"] / 10 # tenths of C --> C
            DFstats["tmin_yearly"]   = DFstats["tmin_yearly"] / 10 # tenths of C --> C
            DFstats["precip_yearly"] = DFstats["precip_yearly"] / 100 # tenths of mm --> cm
            DFstats = DFstats.replace(pd.NA, None).rename(columns = {"date": "year"})
            DFstats["year"] = DFstats["year"].astype(int)
            
            # Insert WxTableStats
            stats_records = DFstats.to_dict(orient = "records")
            if stats_records: # non-empty
                ins_stats = insert(WxTableStats)\
                            .values(stats_records)\
                            .on_conflict_do_nothing(
                                index_elements = ["site_id", "year"]
                            )
                result_stats = session.execute(ins_stats)
                total_stats_rows += result_stats.rowcount or 0 # increment total row count
            
            # Insert WxTable
            DF = DF.replace(pd.NA, None)
            wx_records = DF.to_dict(orient = "records")
            if wx_records:
                ins_wx = insert(WxTable)\
                        .values(wx_records)\
                        .on_conflict_do_nothing(
                            index_elements = ["site_id", "date"]
                            )
                result_wx = session.execute(ins_wx)
                total_wx_rows += result_wx.rowcount or 0 # increment
        
            session.commit()
    
    # End logging
    end_ts  = pd.Timestamp.utcnow()
    elapsed = (end_ts - start_ts).total_seconds()
    logger.info(
        f"""
        ingest_wxdata end 
        wx_rows:  {total_wx_rows} 
        stats_rows: {total_stats_rows}
        Elapsed walltime: {elapsed}
        """
    )