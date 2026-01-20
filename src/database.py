import os
from sqlmodel import SQLModel, create_engine, Session

# Create db engine
engine = create_engine(os.environ["DATABASE_URL"], echo = True)

def create_db_and_tables():
    """
    Create the database and tables.
    """
    SQLModel.metadata.drop_all(engine) # for initial dev work only
    SQLModel.metadata.create_all(engine)

def get_db():
    """
    Dependency for FastAPI: provides database session.
    Automatically closes after request.
    """
    with Session(engine) as session:
        yield session