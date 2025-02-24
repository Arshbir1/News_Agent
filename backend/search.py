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

def search_articles(es, query):
    # Define categories for potential filtering
    CATEGORIES = ["Top", "Sports", "World", "States", "Entertainment"]

    # Check if the query matches a category exactly (case-insensitive)
    normalized_query = query.lower().strip()
    is_category_query = any(cat.lower() == normalized_query for cat in CATEGORIES)

    search_query = {
        "query": {
            "bool": {  # Use bool query for more control
                "should": [
                    # Exact match or phrase match in title (highest priority)
                    {
                        "match_phrase": {
                            "title": {
                                "query": query,
                                "boost": 10  # Boost exact title matches heavily
                            }
                        }
                    },
                    # Partial match or stemmed match in title (moderate priority)
                    {
                        "match": {
                            "title": {
                                "query": query,
                                "fuzziness": 0,  # No fuzziness for precise matches
                                "boost": 5  # Moderate boost for title
                            }
                        }
                    },
                    # Match in content (lower priority)
                    {
                        "match": {
                            "content": {
                                "query": query,
                                "fuzziness": 0,  # No fuzziness for precise matches
                                "boost": 2  # Lower boost for content
                            }
                        }
                    }
                ],
                "minimum_should_match": 1,  # At least one "should" clause must match
                "filter": []  # Optional category filter
            }
        },
        "size": 1000,
        "_source": ["title", "content", "category", "summary", "image_url", "date_publish"]
    }

    # If the query matches a category, filter results to prioritize that category
    if is_category_query:
        search_query["query"]["bool"]["filter"].append(
            {
                "match": {
                    "category": query.capitalize()  # Match the category exactly (capitalize for consistency)
                }
            }
        )

    response = es.search(index=ES_INDEX, body=search_query)
    
    # Deduplicate based on title
    seen_titles = set()
    unique_hits = []
    for hit in response['hits']['hits']:
        title = hit["_source"].get("title")
        if title not in seen_titles:
            seen_titles.add(title)
            unique_hits.append(hit)
    return unique_hits
