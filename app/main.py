from minio import Minio
from peewee import PostgresqlDatabase

from app._app import create_app
from app import config
from app.config import db_name, postgres_settings, minio_settings
from app.custom_errors import BadRequestCodeError, PhotosFormatError, PhotosLimitError

db = PostgresqlDatabase(
    db_name, 
    **postgres_settings,
)

minio_client = Minio(
    **minio_settings,
)

app = create_app(db, minio_client, config)
