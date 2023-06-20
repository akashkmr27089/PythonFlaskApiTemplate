import logging
import os
import time
from dotenv import load_dotenv
from opensearchpy import OpenSearch

load_dotenv()

opensearch = OpenSearch(
    hosts=os.getenv('OPENSEARCH_HOST'),  # Specify the OpenSearch cluster URL
    http_auth=(os.getenv('OPENSEARCH_USERNAME'), os.getenv('OPENSEARCH_PASSWORD')),
    verify_certs=False
)


def check_opensearch_status():
    while True:
        try:
            # Attempt to ping the OpenSearch cluster
            response = opensearch.ping()
            if response:
                logging.info("OpenSearch cluster is up and running")
                return
            else:
                logging.warning("Trying to Connect to Opensearch")
        except Exception as e:
            print("Failed to connect to OpenSearch:", str(e))

        # Wait for a certain period of time before retrying
        time.sleep(2)
