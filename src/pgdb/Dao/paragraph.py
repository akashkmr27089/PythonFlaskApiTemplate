import logging

from src.models.paragraph import Paragraph
from src.pgdb.initialize import get_session
from src.util import ResponseModel


class ParagraphDao:

    @staticmethod
    def create(text: str) -> ResponseModel:
        out = ResponseModel()

        try:
            session = get_session()
            frequent_words = Paragraph(paragraph=text)
            session.add(frequent_words)
            session.commit()
            out.data = frequent_words.id

            session.close()

        except Exception as err:
            out.error = True
            out.message = "Issue while creating database entry"
            logging.warning("Issue while creating database entry", err)

        return out
