import os
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FrequentWords(Base):
    __tablename__ = 'frequent_words'

    id = Column(Integer, primary_key=True)
    words = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<FrequentWords(id={self.id}, words='{self.words}', created_at={self.created_at}, updated_at={self.updated_at})>"



def create(engine):
    Base.metadata.create_all(engine)
