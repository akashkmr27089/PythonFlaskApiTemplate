import logging
import os
import time

from src.pgdb.Dao.frequent_words import FrequentWordsDao
from src.services.frequentWordServices import FrequentWordsServices
from src.util import ResponseModel

global_queue_fww = []


class FrequentWordWorker:
    @staticmethod
    def worker_function():
        while True:
            if global_queue_fww:
                time.sleep(1)
                params = global_queue_fww.pop(0)
                # Execute the function using the parameters
                FrequentWordWorker.process_frequent_words()

    @staticmethod
    def process_frequent_words() -> ResponseModel:
        out = ResponseModel()

        # Call Frequent Worker from Opensearch
        words = FrequentWordsServices.get_frequent_words(os.getenv("DEFAULT_ENTRY_PER_PAGE"))
        if words.error:
            logging.warning("Some issue with the logging ", words.error)
            return words

        # Updating it to postgres
        respFreqDao = FrequentWordsDao.create(','.join(words.data))
        if respFreqDao.error:
            return respFreqDao

        return out
