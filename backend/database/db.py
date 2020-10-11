import os

from sqlalchemy import (Column, DateTime, Boolean, Integer, MetaData, String, Table,
                        create_engine)
from sqlalchemy.sql import func

from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()
notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

inference_results = Table(
    "inference_results",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("image_uuid", String(100)),
    Column("model", String(50)),
    Column("path_name", String(255)),
    Column("completed_datetime", DateTime, default=func.now(), nullable=False),
)

# databases query builder
database = Database(DATABASE_URL)
