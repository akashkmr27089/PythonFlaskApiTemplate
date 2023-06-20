import logging
import time
from typing import Dict

from src.integrations.metaphorpsum import Metaphorsum
from src.models.paragraph import Paragraph
from src.opensearch.dao import OpensearchDao
from src.pgdb.Dao.paragraph import ParagraphDao
from src.util import ResponseModel
from fastapi import BackgroundTasks
from src.models.frequent_words import FrequentWords
from src.pgdb.initialize import Session, get_session

from src.worker.paragraph_worker import global_queue
from src.worker.frequent_word_worker import global_queue_fww
from src.worker.worker import queue


class GetServices:
    @staticmethod
    def create_frequent_words(id_primary, words: list) -> Dict:
        session = get_session()
        frequent_words = FrequentWords(words=words)
        session.add(frequent_words)
        session.commit()
        session.close()

        return frequent_words

    @staticmethod
    async def get_new_paragraph(nos_of_paragraph, nos_of_sentence) -> ResponseModel:
        out = ResponseModel()

        para_response = await Metaphorsum.get_paragraph(nos_of_paragraph, nos_of_sentence)
        if para_response.error:
            return para_response

        # Save the Data Onto Opensearch
        paragraph_data = para_response.data

        pgdb_data_created_id = ParagraphDao.create(paragraph_data)
        if pgdb_data_created_id.error:
            return pgdb_data_created_id

        # global_queue.append([pgdb_data_created_id.data, paragraph_data])
        # global_queue_fww.append(pgdb_data_created_id.data)

        queue.append({"name": "paragraph", "data": [pgdb_data_created_id.data, paragraph_data]})
        queue.append({"name": "frequent_word", "data": [pgdb_data_created_id.data, paragraph_data]})

        out.data = paragraph_data
        return out
