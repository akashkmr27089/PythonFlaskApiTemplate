import logging
from sqlalchemy import desc

from src.models.frequent_words import FrequentWords
from src.pgdb.initialize import get_session
from src.util import ResponseModel


class FrequentWordsDao:

    @staticmethod
    def create(words: str) -> ResponseModel:
        out = ResponseModel()

        try:
            session = get_session()
            frequent_words = FrequentWords(words=words)
            session.add(frequent_words)
            session.commit()
            out.data = frequent_words.id

            session.close()

        except Exception as err:
            out.error = True
            out.message = "Issue while creating database entry"
            logging.warning("Issue while creating database entry", err)

        return out

    @staticmethod
    def get_latest_entry() -> FrequentWords:
        session = get_session()
        latest_frequent_words = session.query(FrequentWords).order_by(desc(FrequentWords.updated_at)).first()
        session.close()

        return latest_frequent_words
