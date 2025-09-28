import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

MYSQL_USER = os.getenv("MYSQL_USER", "notesuser")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "notespwd")
MYSQL_DB = os.getenv("MYSQL_DB", "notesdb")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")


print(
    f"""
        {MYSQL_USER = }
        {MYSQL_PASSWORD = }
        {MYSQL_DB = }
        {MYSQL_HOST = }
        {MYSQL_PORT = }
    """
)
DATABASE_URL = (
    f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
