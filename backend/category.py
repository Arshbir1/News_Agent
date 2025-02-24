from elasticsearch import Elasticsearch
import os
ES_ENDPOINT = os.getenv("ELASTICSEARCH_ENDPOINT")
ES_USERNAME = os.getenv("ELASTICSEARCH_USERNAME")
ES_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD")
ES_INDEX = "news-articles"

def connect_to_elasticsearch():
    es = Elasticsearch(
    hosts=[ES_ENDPOINT],
    basic_auth=(ES_USERNAME, ES_PASSWORD),
    # verify_certs=False  # Disable SSL verification
)
    return es

# def extract_articles_by_category(es, category):
#     query = {"query": {"match": {"category": category}}}
#     response = es.search(index=ES_INDEX, body=query, size=1000)
#     extracted_articles = [hit['_source'] for hit in response['hits']['hits']]
#     return extracted_articles

def extract_articles_by_category(es, category):
    """
    Extract articles of a specific category from Elasticsearch.
    """
    query = {
        "query": {
            "match": {
                "category": category
            }
        },
        "size": 1000,
        "_source": ["title", "content", "category", "summary", "image_url", "date_publish"]
    }

    # Search for articles in the specified category
    response = es.search(index=ES_INDEX, body=query)
    extracted_articles = [hit['_source'] for hit in response['hits']['hits']]
    return extracted_articles
