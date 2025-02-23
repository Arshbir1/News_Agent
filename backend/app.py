from flask import Flask, render_template, request, jsonify
from elasticsearch import Elasticsearch
from ContentSummarizer import summarize_text
from backend.search import search_articles  # Correct import
import logging

app = Flask(__name__)

# Elasticsearch configuration
ES_ENDPOINT = "https://9fb474a7f57d4bfbbd9e05246ff0b8ec.asia-south1.gcp.elastic-cloud.com:443"
ES_USERNAME = "elastic"
ES_PASSWORD = "6lWF4jG8mE5IUnOSc66kmSo1"
ES_INDEX = "news-articles"

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def connect_to_elasticsearch():
    es = Elasticsearch(
        ES_ENDPOINT,
        basic_auth=(ES_USERNAME, ES_PASSWORD)
    )
    if not es.ping():
        raise Exception("Failed to connect to Elasticsearch")
    return es

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/category/<category>')
def category(category):
    es = connect_to_elasticsearch()
    if not es.ping():
        return jsonify({"error": "Could not connect to Elasticsearch"}), 500

    query = {
        "query": {
            "match": {
                "category": category
            }
        }
    }
    response = es.search(index=ES_INDEX, body=query, size=1000)
    articles = [hit['_source'] for hit in response['hits']['hits']]
    return jsonify(articles)

@app.route('/article/<title>')
def article(title):
    es = connect_to_elasticsearch()
    query = {
        "query": {
            "match": {
                "title": title
            }
        }
    }
    response = es.search(index=ES_INDEX, body=query)
    if response['hits']['total']['value'] > 0:
        article = response['hits']['hits'][0]['_source']
        
        # Summarize the article content
        if 'content' in article and article['content']:
            summary = summarize_text(article['content'])
            article['summary'] = summary  # Add the summary to the article object
        else:
            article['summary'] = "No content available for summarization."
        
        return jsonify(article)
    else:
        return jsonify({"error": "Article not found"}), 404

@app.route('/search')
def search():
    es = connect_to_elasticsearch()
    if not es.ping():
        logging.error("Failed to connect to Elasticsearch")
        return jsonify({"error": "Could not connect to Elasticsearch"}), 500

    # Get the search query from the URL parameters
    query = request.args.get('q')
    if not query:
        logging.error("No search query provided")
        return jsonify({"error": "No search query provided"}), 400

    try:
        # Use the search function from search.py
        results = search_articles(es, query)
        articles = [hit['_source'] for hit in results]  # Extract articles from search results
        return jsonify(articles)
    except Exception as e:
        logging.error(f"Error during search: {e}")
        return jsonify({"error": "Failed to fetch articles"}), 500

if __name__ == '__main__':
    app.run(debug=True)