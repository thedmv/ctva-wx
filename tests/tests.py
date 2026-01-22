import os
from sqlmodel import Session, select
from .database import engine, create_db_and_tables
from .ingest import ingest_wxdata
from .models import WxTable, WxTableStats

def _count(SESSION, MODEL):
    """
    Function for counting the rows.
    """
    return len(SESSION.exec(select(MODEL)).all() )

def test_ingest():
    """
    Testing the ingestion is done correctly.
    """
    create_db_and_tables()
    ingest_wxdata()

    with Session(engine) as session:
        wx_count_1    = _count(session, WxTable)
        stats_count_1 = _count(session, WxTableStats)
    
    ingest_wxdata()

    with Session(engine) as session:
        wx_count_2    = _count(session, WxTable)
        stats_count_2 = _count(session, WxTableStats)

    assert wx_count_1 == wx_count_2
    assert stats_count_1 == stats_count_2