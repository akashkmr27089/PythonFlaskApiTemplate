import logging

import httpx
from src.util import ResponseModel


class Metaphorsum:

    @staticmethod
    async def get_paragraph(nos_of_para, no_of_sentence) -> ResponseModel:
        out = ResponseModel()

        if nos_of_para == 0 or no_of_sentence == 0:
            return []

        base_url = "http://metaphorpsum.com/paragraphs/"
        url = base_url + str(nos_of_para) + "/" + str(no_of_sentence)

        try:
            async with httpx.AsyncClient() as client:
                data = await client.get(url, timeout=10)  # Set the timeout value as desired

            if data.status_code == 200:
                out.data = data.text
            else:
                out.error = True
                out.message = "Some issue while getting paragraph"
                logging.warning("Some issue while getting paragraph")

        except httpx.TimeoutException:
            out.error = True
            out.message = "Timeout error occurred"
            logging.warning("Timeout error occurred")

        except httpx.NetworkError:
            out.error = True
            out.message = "Network error occurred"
            logging.warning("Network error occurred")

        return out
