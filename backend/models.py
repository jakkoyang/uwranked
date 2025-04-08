from sqlalchemy import Table, Column, Integer, String, MetaData, Float, create_engine

metadata = MetaData()

profiles = Table(
    "profiles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("education", String),
    Column("experience", String),
    Column("image_url", String),
    Column("elo", Float, default=1000.0),
)

engine = create_engine("sqlite:///tmp.db")  # fallback; won't be used
metadata.create_all(engine)