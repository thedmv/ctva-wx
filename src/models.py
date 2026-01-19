import os
from typing import Optional
from pathlib import Path
from datetime import datetime
from joblib import cpu_count, Parallel, delayed
import pandas as pd
from sqlmodel import SQLModel, Field, create_engine, Session

# classes
class WxTable(SQLModel, table = True):
    id: Optional[int] = Field(default = None, primary_key = True)
    site_id: str
    date:    datetime
    tmax:    int | None
    tmin:    int | None
    precip:  int | None

# functions
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
    # print(df[df.isna().any(axis = 1)].head(3))
    return DF

# Create db engine
engine = create_engine(os.environ["DATABASE_URL"], echo = True)

def create_db_and_tables():
    """
    Create the database and tables.
    """
    SQLModel.metadata.create_all(engine)

def ingest():
    """
    Ingest all data files, one file at a time
    """
    PATH  = Path("/code/wx_data")
    FILES = [f for f in PATH.glob("USC*.txt")][0:10]
    cols = [k for k in WxTable.model_fields.keys()]
    with Session(engine) as session:
        for f in FILES:
            DF = read_wxdata(f)
            DF = DF.replace(pd.NA, None)
            rows = DF.to_dict(orient = "records")
            session.add_all(WxTable(**r) for r in rows)
            session.commit()

def main():
    create_db_and_tables()
    ingest()

if __name__ == "__main__":
    main()