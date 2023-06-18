import logging
import os
from dotenv import load_dotenv
from opensearchpy import OpenSearch

load_dotenv()

opensearch = OpenSearch(
    hosts=os.getenv('OPENSEARCH_HOST'),  # Specify the OpenSearch cluster URL
    http_auth=(os.getenv('OPENSEARCH_USERNAME'), os.getenv('OPENSEARCH_PASSWORD')),
    verify_certs=False
)