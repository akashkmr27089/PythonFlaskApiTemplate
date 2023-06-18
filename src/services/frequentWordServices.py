from src.opensearch.dao import OpensearchDao
from src.util import ResponseModel
from src.integrations.dictionary import Dictionary


class FrequentWordsServices:

    @staticmethod
    async def get_frequent_words(size: int) -> ResponseModel:
        # use opensearch integration to fetch most frequent words
        wordlist = OpensearchDao.get_frequent_words(size)
        word_list_data = []

        for i in wordlist:
            word_list_data.append(i['key'])
        response = ResponseModel(**{"data": word_list_data})

        return response

    @staticmethod
    async def get_dictionary_words(words: list) -> ResponseModel:
        # use opensearch integration to fetch most frequent words
        response = ResponseModel()
        if len(words) == 0:
            response.data = []
        else:
            data: ResponseModel = await Dictionary.get_dictionary_meanings_by_words(words)
            if data.error:
                pass

        return data

    @staticmethod
    async def get_frequent_words_with_meaning(count: int) -> ResponseModel:
        words = await FrequentWordsServices.get_frequent_words(count)
        if words.error:
            pass

        words_with_meaning: ResponseModel = await FrequentWordsServices.get_dictionary_words(words.data)
        if words.error:
            pass

        # Pass it through dto
        return words_with_meaning



