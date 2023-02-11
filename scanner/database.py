import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import declarative_base

load_dotenv()

database_url = URL.create(
    drivername=os.getenv('DB_DRIVER'),
    username=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
    database=os.getenv('DB_DATABASE'),
)
engine = create_engine(database_url)

Base = declarative_base()
