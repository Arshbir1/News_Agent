from elasticsearch import Elasticsearch

# Elasticsearch configuration
ES_ENDPOINT = "https://9fb474a7f57d4bfbbd9e05246ff0b8ec.asia-south1.gcp.elastic-cloud.com:443"
ES_USERNAME = "elastic"
ES_PASSWORD = "6lWF4jG8mE5IUnOSc66kmSo1"  # Replace with your actual password
ES_INDEX = "news-articles"  # Name of the Elasticsearch index

def connect_to_elasticsearch():
    """
    Connect to the Elasticsearch cluster.
    """
    es = Elasticsearch(
        ES_ENDPOINT,
        basic_auth=(ES_USERNAME, ES_PASSWORD)
    )
    return es

def search_articles(es, query):
    """
    Search for articles by keywords in both the title and content fields.
    """
    search_query = {
        "query": {
            "multi_match": {
                "query": query,  # The search query
                "fields": ["title^3", "content"],  # Search in both title and content fields
                "fuzziness": "AUTO"  # Allow for some typos in the query
            }
        }
    }

    # Execute the search query
    response = es.search(index=ES_INDEX, body=search_query)
    return response['hits']['hits']  # Return the search results

# Example usage
if __name__ == "__main__":
    es = connect_to_elasticsearch()
    query = "cricket"  # Example search query
    results = search_articles(es, query)
    
    if results:
        print(f"Found {len(results)} results for '{query}':")
        for result in results:
            print(f"Title: {result['_source']['title']}")
            print(f"Content snippet: {result['_source']['content'][:200]}...")  # Show a snippet of the content
            print("-" * 50)
    else:
        print(f"No results found for '{query}'.")