import logging

from src.opensearch.initialize import opensearch
from src.services.frequentWordServices import FrequentWordsServices
from src.services.getServices import GetServices

from src.util import ResponseModel, FrequentWordsModel
from src.controller.conv import Conv


class Controller:

    @staticmethod
    async def get(nos_of_para: int, nos_of_sentence: int):
        data: ResponseModel = await GetServices.get_new_paragraph(nos_of_para, nos_of_sentence)
        if data.error:
            return data

        # Extract and return the relevant search results
        # hits = response['hits']['hits']

        # DTO for the object
        return Conv.dto_get_object(data)

    @staticmethod
    async def search():
        pass

    @staticmethod
    async def get_frequent_words(count: int) -> [FrequentWordsModel]:
        data: ResponseModel = await FrequentWordsServices.get_frequent_words_with_meaning(count)
        if data.error:
            return data

        # DTO for the object
        return Conv.dto_frequent_word_object(data)
