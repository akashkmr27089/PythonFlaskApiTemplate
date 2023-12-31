import logging

from src.opensearch.dao import OpensearchDao
from src.pgdb.Dao.frequent_words import FrequentWordsDao
from src.util import ResponseModel
from src.integrations.dictionary import Dictionary


class FrequentWordsServices:

    @staticmethod
    def get_frequent_words(size: int) -> ResponseModel:
        # use opensearch integration to fetch most frequent words
        wordlist = OpensearchDao.get_frequent_words(size)
        word_list_data = []

        for i in wordlist:
            word_list_data.append(i['key'])
        response = ResponseModel(**{"data": word_list_data})

        return response

    @staticmethod
    def get_frequent_words2() -> ResponseModel:
        # use opensearch integration to fetch most frequent words
        word_list_data = []
        out = ResponseModel()

        try:
            wordlist = FrequentWordsDao.get_latest_entry()

            if wordlist.words != "":
                wordlist = wordlist.words.split(',')

                for i in wordlist:
                    word_list_data.append(i.lower())

                out.data = word_list_data
        except Exception as ex:
            out.error = True
            out.message = "Some issue while getting frequent words"
            logging.info(ex)

        return out

    @staticmethod
    async def get_dictionary_words(words: list) -> ResponseModel:
        # use opensearch integration to fetch most frequent words
        response = ResponseModel()
        if len(words) == 0:
            response.data = []
        else:
            data: ResponseModel = await Dictionary.get_dictionary_meanings_by_words(words)
            if data.error:
                logging.info("Error at func get_dictionary_words")
                return data

        return data

    @staticmethod
    async def get_frequent_words_with_meaning() -> ResponseModel:
        words = FrequentWordsServices.get_frequent_words2()
        if words.error:
            return words

        words_with_meaning: ResponseModel = await FrequentWordsServices.get_dictionary_words(words.data)
        if words.error:
            return words_with_meaning

        # Pass it through dto
        return words_with_meaning
