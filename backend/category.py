from elasticsearch import Elasticsearch
import json

# Elasticsearch configuration
ES_ENDPOINT = "https://9fb474a7f57d4bfbbd9e05246ff0b8ec.asia-south1.gcp.elastic-cloud.com:443"
ES_USERNAME = "elastic"
ES_PASSWORD = "6lWF4jG8mE5IUnOSc66kmSo1"  # Replace with your actual password
ES_INDEX = "news-articles"  # Name of the Elasticsearch index

# Output file
OUTPUT_FILE = "extracted_data.json"

def connect_to_elasticsearch():
    """
    Connect to the Elasticsearch cluster.
    """
    es = Elasticsearch(
        ES_ENDPOINT,
        basic_auth=(ES_USERNAME, ES_PASSWORD)
    )
    return es

def extract_articles_by_category(es, category):
    """
    Extract articles of a specific category from Elasticsearch.
    """
    query = {
        "query": {
            "match": {
                "category": category
            }
        }
    }

    # Search for articles in the specified category
    response = es.search(index=ES_INDEX, body=query, size=1000)  # Adjust size as needed
    extracted_articles = [hit['_source'] for hit in response['hits']['hits']]
    return extracted_articles

def save_articles(articles, json_file):
    """
    Save articles to a JSON file.
    """
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=4, ensure_ascii=False)
    print(f"✅ Extracted articles saved to '{json_file}'.")

def main():
    """
    Main function to extract articles by category from Elasticsearch and save them to a file.
    """
    # Connect to Elasticsearch
    es = connect_to_elasticsearch()
    if not es.ping():
        print("❌ Could not connect to Elasticsearch. Check your credentials and endpoint.")
        return

    # Get the category from the user
    category = input("Enter the category to extract (e.g., Top, Sports, World, Business, etc.): ").strip()

    # Extract articles of the specified category
    extracted_articles = extract_articles_by_category(es, category)

    if not extracted_articles:
        print(f"No articles found for category: '{category}'.")
        return

    # Save the extracted articles to a new file
    save_articles(extracted_articles, OUTPUT_FILE)

# Run the script
if __name__ == "__main__":
    main()