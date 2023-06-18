import logging

import httpx
from httpx import Response
from src.util import ResponseModel


class Metaphorsum:

    @staticmethod
    async def get_paragraph(nos_of_para, no_of_sentence) -> ResponseModel:
        out = ResponseModel()

        if nos_of_para == 0 or no_of_sentence == 0:
            return []

        base_url = "http://metaphorpsum.com/paragraphs/"
        url = base_url + str(nos_of_para) + "/" + str(no_of_sentence)

        data = await httpx.AsyncClient().get(url)

        if data.status_code == 200:
            out.data = data.text
        else:
            out.error = True
            out.message = "Some issue while getting paragraph"
            logging.warning("Some issue while getting paragraph")

        return out
