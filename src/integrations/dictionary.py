import asyncio
import json
import httpx as httpx
from src.util import ResponseModel


class Dictionary:

    @staticmethod
    async def get_dictionary_meanings_by_words(words: [str]) -> [ResponseModel]:
        base_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
        response = ResponseModel()

        try:
            words_search_urls = [base_url + word for word in words]
            response_data = []

            async with httpx.AsyncClient() as client:

                tasks = [client.get(url) for url in words_search_urls]
                responses = await asyncio.gather(*tasks)
                for resp in responses:
                    res = {}
                    if resp.status_code == 404:
                        res = {
                            "data": "",
                            "status_code": 404,
                            "message": json.loads(resp.text)["message"],
                            "error": True
                        }
                    else:
                        res = {
                            "data": json.loads(resp.text),
                            "status_code": 200,
                            "error": False,
                            "message": ""
                        }
                    response_data.append(res)

                response.data = response_data

        except Exception as ex:
            print(ex)
            response.error = True
            response.message = "Issue with finding words with dictionary"

        return response
