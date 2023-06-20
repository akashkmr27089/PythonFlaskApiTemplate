import os
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Define a base class for declarative models
Base = declarative_base()


class Paragraph(Base):
    __tablename__ = 'paragraph'

    id = Column(Integer, primary_key=True)
    paragraph = Column(String)

    def __repr__(self):
        return f"<Paragraph(paragraph='{self.name}')>"


def create(engine):
    Base.metadata.create_all(engine)
