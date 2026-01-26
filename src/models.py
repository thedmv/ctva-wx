from typing import Optional
from datetime import datetime
from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field
from config import WXDATA_METADATA as WXMETA, WXDATASTATS_METADATA as WXSTATSMETA


# Raw data model
class WxTable(SQLModel, table = True):
    __table_args__ = (UniqueConstraint("site_id", "date", name = "uq_wxtable_site_date"), )
    id:      Optional[int] = Field(default = None, primary_key = True)
    site_id: str           = Field(description = WXMETA["site_id"])
    date:    datetime      = Field(description = WXMETA["date"])
    tmax:    Optional[int] = Field(default = None, description = WXMETA["tmax"] )
    tmin:    Optional[int] = Field(default = None, description = WXMETA["tmin"] )
    precip:  Optional[int] = Field(default = None, description = WXMETA["precip"] )

# Summary data model of the statistics of the raw data
class WxTableStats(SQLModel, table = True):
    __table_args__ = (UniqueConstraint("site_id", "year", name = "uq_wxtablestats_site_year"), )
    id:            Optional[int]   = Field(default = None, primary_key = True)
    site_id:       str             = Field(description = WXSTATSMETA["site_id"])
    year:          int             = Field(description = WXSTATSMETA["year"])
    tmax_yearly:   Optional[float] = Field(default = None, description = WXSTATSMETA["tmax_yearly"] )
    tmin_yearly:   Optional[float] = Field(default = None, description = WXSTATSMETA["tmin_yearly"] )
    precip_yearly: Optional[float] = Field(default = None, description = WXSTATSMETA["precip_yearly"] )