import asyncio
import json
import logging

import httpx as httpx
from src.util import ResponseModel
from src.redis.dao import RedisDao


class Dictionary:

    @staticmethod
    async def get_dictionary_meanings_by_words(words: list) -> ResponseModel:
        base_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
        response = ResponseModel()

        try:
            # Add Cached Response to the response_data and remove those words from the redis
            # Since the words meaning will not change, it does not make any sense of storing it
            response_data = []
            cached_keys_and_data, keys_not_found = RedisDao.get_by(keys=words)
            response_data += cached_keys_and_data

            words_search_urls = [base_url + word for word in keys_not_found]
            logging.warning("Words not found in cache : {}".format(','.join(keys_not_found)))

            async with httpx.AsyncClient(timeout=4.0) as client:
                tasks = [client.get(url) for url in words_search_urls]
                responses = await asyncio.gather(*tasks, return_exceptions=True)

                for resp in responses:
                    res = {}

                    if isinstance(resp, Exception):
                        # Handle ConnectTimeout error
                        if isinstance(resp, httpx.ConnectTimeout):
                            res = {
                                "data": "",
                                "status_code": 408,  # Request Timeout
                                "message": "Request timed out",
                                "error": True
                            }
                        else:
                            # Handle other exceptions
                            res = {
                                "data": "",
                                "status_code": 500,  # Internal Server Error
                                "message": str(resp),
                                "error": True
                            }

                    else:
                        # Handle successful response
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

                            # Add successful data in cache
                            RedisDao.set(Dictionary.get_word_from_response(resp.text), res)

                    response_data.append(res)

                response.data = response_data

        except Exception as ex:
            print(ex)
            response.error = True
            response.message = "Issue with finding words with dictionary"

        return response

    @staticmethod
    def get_word_from_response(txt: str):
        if len(txt) > 0:
            json_data = json.loads(txt)
            word = json_data[0]["word"]
            return word
        else:
            logging.info("Not able to get word for the text {}".format(txt))
            return ""
