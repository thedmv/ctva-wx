from pathlib import Path

import os
import sys
from pathlib import Path
import logging 

#####
# SETUP FOR LOGGER
#####
LOGGER_NAME = "ctva_log"
LOG_LEVEL   = logging.INFO
LOG_FORMAT  = "%(asctime)s %(levelname)s %(name)s - %(message)s"
logger = logging.getLogger(LOGGER_NAME)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(handler)
logger.setLevel(LOG_LEVEL)


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
    "tmax_yearly":   "yearly average of maximum temperature, degrees C",
    "tmin_yearly":   "yearly average of minimum temperature, degrees C",
    "precip_yearly": "yearly accumulated precipitation, cm"
}