import logging

from src.services.searchServices import SearchServices
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

        # DTO for the object
        return Conv.dto_get_object(data)

    @staticmethod
    async def search(search_or: str, search_and: str):
        parameters_with_or_conditions = string_to_array(search_or)
        parameters_with_and_conditions = string_to_array(search_and)

        data: ResponseModel = await SearchServices.search(parameters_with_or_conditions, parameters_with_and_conditions)
        if data.error:
            return data

        return Conv.dto_search(data)

    @staticmethod
    async def get_frequent_words() -> [FrequentWordsModel]:
        data: ResponseModel = await FrequentWordsServices.get_frequent_words_with_meaning()
        if data.error:
            return data

        # DTO for the object
        return Conv.dto_frequent_word_object(data)


def string_to_array(data: str) -> list:
    if data == "" or data is None:
        return []
    else:
        return [x.lstrip().rstrip() for x in data.split(",")]