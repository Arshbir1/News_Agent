from elasticsearch import Elasticsearch

ES_ENDPOINT = "https://9fb474a7f57d4bfbbd9e05246ff0b8ec.asia-south1.gcp.elastic-cloud.com:443"
ES_USERNAME = "elastic"
ES_PASSWORD = "6lWF4jG8mE5IUnOSc66kmSo1"
ES_INDEX = "news-articles"

def connect_to_elasticsearch():
    es = Elasticsearch(ES_ENDPOINT, basic_auth=(ES_USERNAME, ES_PASSWORD))
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