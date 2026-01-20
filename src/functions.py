from pathlib import Path
import pandas as pd

def read_wxdata(FILE: Path) -> pd.DataFrame:
    """
    Read the wx_data.
    Input:
    - FILENAME: Path (from pathlib) object of the path of a wx_data file
    Output:
    - DF: dataframe of a wx_data
    """
    cols = ["date", "tmax", "tmin", "precip"]
    dtyp  = (str, int, int, int)
    dtypes  = {k:v for k, v in zip(cols, dtyp)}
    DF = pd.read_table(FILE,
                       delimiter = "\t",
                       header = None,
                       names  = cols, 
                       dtype  = dtypes)
    # Make time datetime obj
    DF["date"] = pd.to_datetime(DF["date"])
    # Assign a column for the site ID from the filename
    DF = DF.assign(site_id = FILE.stem)
    # Sanitize the null values
    DF = DF.replace(-9999, pd.NA)
    return DF

def calculate_wxdata_stats(FILE):
    """
    Calculates the yearly stats for 
    """