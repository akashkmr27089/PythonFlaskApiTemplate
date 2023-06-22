import os

from src.opensearch.constant import INDEX_PARA_DATA, INDEX_PARA_DATA_MODEL, TOKENS_KEYWORD, TOKENS_AGGREGATION_QUERY
from src.opensearch.initialize import opensearch
import logging

from src.opensearch.query import query_generator
from src.util import ResponseModel


class OpensearchDao:

    @staticmethod
    def migration():
        # This will make sure to create Migration Variables
        try:
            indices = opensearch.indices.get_alias("*")
            if INDEX_PARA_DATA in indices:
                return
            else:
                index_name = INDEX_PARA_DATA  # Replace with the desired name of your index
                # Create the index with the mapping
                response = opensearch.indices.create(index=index_name, body={"mappings": INDEX_PARA_DATA_MODEL})
                logging.info(response)

                if response["acknowledged"]:
                    logging.info("Document indexed successfully.")
                else:
                    logging.error("Failed to index document.")
                    raise Exception("Failed to index document.")

        except Exception as err:
            logging.error("Error while Creating index" + INDEX_PARA_DATA, err)

    @staticmethod
    def create(index, text_data, tokens) -> bool:
        document_data = {
            "text_id": index,
            "text_data": text_data,
            "tokens_data": tokens,
            # Add more fields and their values as needed
        }

        response = opensearch.index(index=INDEX_PARA_DATA, body=document_data)

        if response["result"] == "created":
            logging.info("Document indexed successfully.")
            return True
        else:
            logging.warning("Failed to index document.")
            return False

        return True

    @staticmethod
    def search_with_params(conditions_with_or_operator: [str], conditions_with_and_operator: [str]) -> ResponseModel:
        out_resp = ResponseModel()
        try:
            query = query_generator(conditions_with_or_operator, conditions_with_and_operator, "text_data")

            search_query = {
                "_source": ["text_data", "_id"],
                "size": os.getenv("DEFAULT_ENTRY_PER_PAGE"),
                "query": {
                    "query_string": {
                        "query": query
                    }
                }
            }
            logging.info("generated_query", search_query)
            response = opensearch.search(index=INDEX_PARA_DATA, body=search_query)

            # Process the search results
            out = []
            for hit in response['hits']['hits']:
                # Access the desired field from the hit
                elem = hit['_source']
                if "text_data" in elem:
                    out.append({
                        "id": hit['_id'],
                        "text": elem["text_data"]
                    })

            out_resp.data = out

        except Exception as ex:
            logging.warning("Some issues with the Opensearch Search", ex)
            out_resp.error = True
            out_resp.message = "Some issues with the Opensearch Search"

        return out_resp

    @staticmethod
    def get_frequent_words(size: int) -> []:
        # Define the index name

        # Define the aggregation query
        aggregation_query = {
            "size": 0,
            "aggs": {
                "aggregation_name": {
                    "terms": {
                        "field": TOKENS_KEYWORD,
                        "size": size
                    }
                }
            }
        }

        # aggregation_query = TOKENS_AGGREGATION_QUERY.format(TOKENS_KEYWORD, size)

        response = opensearch.search(index=INDEX_PARA_DATA, body=aggregation_query)
        aggregation_results = response["aggregations"]["aggregation_name"]["buckets"]

        return aggregation_results
