from database import create_db_and_tables
from ingest import ingest_wxdata

def main():
    """
    Creates (or resets for dev) database and tables. See database.py
    Then performs ingestion. See ingest.py
    """
    create_db_and_tables()
    ingest_wxdata()

if __name__ == "__main__":
    main()