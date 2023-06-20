import logging
import os
import time

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.models.models import pgdb_migration

# Database connection details
host = os.getenv('PG_HOST')
port = os.getenv('PG_PORT')
database = os.getenv('PG_DATABASE')
user = os.getenv('PG_USER')
password = os.getenv('PG_PASSWORD')

# Create a PostgresSQL engine
# Engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

retry_interval = 2
retry_count = 0

Engine, Session, Base = None, None, None


def connect():
    global retry_count, retry_interval, Engine, Session, Base

    while True:
        try:
            Engine = create_engine(
                f'postgresql://{user}:{password}@{host}:{port}/{database}'
            )
            Engine.connect().close()
            logging.info("Postgres Engine Connected")

            # Create a session factory
            Session = sessionmaker(bind=Engine)

            if os.getenv("MIGRATION"):
                pgdb_migration(engine=Engine)

            # Define a base class for declarative models
            Base = declarative_base()
            return True

        except Exception as e:
            logging.info(f"Connection failed (attempt {retry_count + 1}): {e}")
            retry_count += 1
            time.sleep(retry_interval)
            return False


def get_session():
    return Session()
