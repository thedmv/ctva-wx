from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from config import WXDATA_METADATA as WXMETA, WXDATASTATS_METADATA as WXSTATSMETA


# Raw data model
class WxTable(SQLModel, table = True):
    id:      Optional[int] = Field(default = None, primary_key = True)
    site_id: str           = Field(description = WXMETA["site_id"])
    date:    datetime      = Field(description = WXMETA["date"])
    tmax:    Optional[int] = Field(default = None, description = WXMETA["tmax"] )
    tmin:    Optional[int] = Field(default = None, description = WXMETA["tmin"] )
    precip:  Optional[int] = Field(default = None, description = WXMETA["precip"] )

# Summary data model of the statistics of the raw data
class WxTableStats(SQLModel, table = True):
    id:            Optional[int] = Field(default = None, primary_key = True)
    site_id:       str           = Field(description = WXSTATSMETA["site_id"])
    year:          datetime      = Field(description = WXSTATSMETA["year"])
    tmax_yearly:   Optional[int] = Field(default = None, description = WXSTATSMETA["tmax_yearly"] )
    tmin_yearly:   Optional[int] = Field(default = None, description = WXSTATSMETA["tmin_yearly"] )
    precip_yearly: Optional[int] = Field(default = None, description = WXSTATSMETA["precip_yearly"] )