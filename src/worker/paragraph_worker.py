import time

from src.opensearch.dao import OpensearchDao
from src.util import ResponseModel


class ParagraphWorker:

    @staticmethod
    def generate_tokens(paragraph):
        return [x for x in paragraph.split(" ")]

    @staticmethod
    def process_paragraph(params) -> ResponseModel:
        out = ResponseModel()

        if len(params) == 2:
            index_id = params[0]
            text = params[1]

            token_data = ParagraphWorker.generate_tokens(text)

            if_entry_created = OpensearchDao.create(index_id, text, token_data)
            if not if_entry_created:
                out.error = True
                out.message = "Object not created in Opensearch"
                return out
        else:
            out.error = True
            out.message = "The data not in acceptable format"

        return out
