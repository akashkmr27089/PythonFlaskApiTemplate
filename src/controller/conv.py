from src.util import FrequentWordsModel, ResponseModel
import logging


class Conv:

    @staticmethod
    def dto_frequent_word_object(data: ResponseModel) -> [FrequentWordsModel]:
        resp_data = data.data
        out = []

        for i in resp_data:
            if not i['error']:
                dat = i['data'][0]
                out_elem = FrequentWordsModel()
                out_elem.word = dat['word']
                out_elem.meanings = dat['meanings']
                out.append(out_elem)
            else:
                logging.warning("Issue while getting meaning for a word", i["message"])

        return out

    @staticmethod
    def dto_get_object(data: ResponseModel):
        return data

    @staticmethod
    def dto_search(data: ResponseModel):
        return data
