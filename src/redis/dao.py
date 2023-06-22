import json
import logging

from src.redis.initialize import redis_client


class RedisDao:
    @staticmethod
    def get_by(keys: list) -> ([str], [str]):
        cached_keys_and_data = []
        keys_not_found = []
        for key in keys:
            data = redis_client.get(key)
            if data:
                cached_keys_and_data.append(json.loads(data))
            else:
                keys_not_found.append(key)

        return cached_keys_and_data, keys_not_found

    @staticmethod
    def set(key: str, value: str) -> bool:
        try:
            if key is None or key == "":
                return False
            else:
                if isinstance(value, dict):
                    value = json.dumps(value)
                resp = redis_client.set(key, value)
                return True
        except Exception as ex:
            logging.info("Exception ex {}".format(ex))
            logging.info("Some issue while setting data in redis key: {} value: {}".format(key, value))

