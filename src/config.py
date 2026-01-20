from pathlib import Path

import os
import sys
from pathlib import Path

####
# DIRECTORY AND FILE PATHS
####

DIR_WXDATA  = Path("/code/wx_data")
DIR_YLDDATA = Path("/code/yld_data")
FILES_WXDATA = [f for f in Path("/code/wx_data").glob("USC*.txt")]

###
# METADATA
###
WXDATA_METADATA = {
    "site_id": "Weather Station name",
    "date":    "datetime for daily weather data",
    "tmax":    "daily maximum temperature, tenths of degrees C",
    "tmin":    "daily minimum temperature, tenths of degrees C",
    "precip":  "daily total accumulated precipitation, tenths of mm"
}

WXDATASTATS_METADATA = {
    "site_id":       "Weather Station name",
    "year":          "year for aggregate statistic",
    "tmax_yearly":   "yearly average of maximum temperature, tenths of degrees C",
    "tmin_yearly":   "yearly average of minimum temperature, tenths of degrees C",
    "precip_yearly": "yearly accumulated precipitation, tenths of mm"
}