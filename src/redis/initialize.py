import logging
import os
import time
import redis


def connect_to_redis():
    while True:
        try:
            # Create Redis client
            client = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=0)

            # Ping Redis server
            response = client.ping()
            if response:
                logging.info("Connected to Redis!")
                return client

        except redis.ConnectionError:
            # Retry after 1 second if connection failed
            logging.warning("Failed to connect to Redis. Retrying in 1 second...")
            time.sleep(1)


redis_client = connect_to_redis()
