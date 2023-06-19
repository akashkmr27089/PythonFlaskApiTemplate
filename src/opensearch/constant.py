INDEX_PARA_DATA = "para_data_key"
TOKENS_KEYWORD = "tokens_data.keyword"
TOKENS_AGGREGATION_QUERY = {
    "size": 0,
    "aggs": {
        "aggregation_name": {
            "terms": {
                "field": {},
                "size": {}
            }
        }
    }
}

INDEX_PARA_DATA_MODEL = {
    "properties": {
        "text_data": {
            "type": "text"
        },
        "tokens_data": {
            "type": "text",
            "fields": {
                "keyword": {
                    "type": "keyword",
                }
            }
        },
    }
}
