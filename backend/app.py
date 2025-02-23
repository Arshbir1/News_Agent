from flask import Flask, jsonify, request, render_template
import time
try:
    from .Translator import translate_text  # Updated to match file name
    from .category import extract_articles_by_category
    from .search import search_articles
except ModuleNotFoundError as e:
    print(f"Error: Could not import module - {e}")
    print("Ensure all backend files are in the same directory as app.py")
    exit(1)

app = Flask(__name__)

# Connect to Elasticsearch once at app startup (using configuration from other files)
from elasticsearch import Elasticsearch

ES_ENDPOINT = os.getenv("ELASTICSEARCH_ENDPOINT")
ES_USERNAME = os.getenv("ELASTICSEARCH_USERNAME")
ES_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD")
ES_INDEX = "news-articles"

es = Elasticsearch(ES_ENDPOINT, basic_auth=(ES_USERNAME, ES_PASSWORD))

CATEGORIES = ["Top", "Sports", "World", "States", "Cities", "Entertainment"]
@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/category/<category>', methods=['GET'])
def get_articles(category):
    start_time = time.time()
    articles = extract_articles_by_category(es, category)
    print(f"Category {category} fetch took: {time.time() - start_time:.3f} seconds")
    return jsonify(articles)

@app.route('/search', methods=['GET'])
def search_articles_endpoint():
    query = request.args.get('q', default='')
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400
    start_time = time.time()
    results = search_articles(es, query)
    articles = [hit['_source'] for hit in results]
    print(f"Search for '{query}' took: {time.time() - start_time:.3f} seconds")
    return jsonify(articles)

@app.route('/article_page/<path:title>')
def article_page(title):
    start_time = time.time()
    
    # Use match query for flexible matching
    query = {"query": {"match": {"title": title}}}
    response = es.search(index="news-articles", body=query)
    query_time = time.time() - start_time
    print(f"ES query for '{title}' took: {query_time:.3f} seconds")
    print(f"Query sent: {query}")  # Debug: Show exact query
    
    if response['hits']['total']['value'] == 0:
        print(f"No article found for title: '{title}'")
        print(f"ES response: {response}")  # Debug: Show why it failed
        return "Article not found", 404
    
    article = response['hits']['hits'][0]['_source']
    print(f"Found article: {article}")  # Debug: Confirm article data
    
    # Use precomputed summary directly (or placeholder if none exists)
    summary_start = time.time()
    if 'summary' in article and article['summary']:
        print(f"Using precomputed summary for '{title}': {article['summary'][:50]}...")
    else:
        print(f"WARNING: No summary in ES for '{title}', using fallback")
        article['summary'] = "Summary not available (precompute externally)"
    summary_time = time.time() - summary_start
    print(f"Summary retrieval took: {summary_time:.3f} seconds")

    # Handle translation only if requested
    lang = request.args.get('lang', default=None)
    if lang:
        translate_start = time.time()
        article['title'] = translate_text(article['title'], lang) or article['title']
        article['summary'] = translate_text(article['summary'], lang) or article['summary']
        translate_time = time.time() - translate_start
        print(f"Translation for '{title}' took: {translate_time:.3f} seconds")
    else:
        print(f"No translation requested for '{title}'")

    # Render the page
    render_start = time.time()
    response = render_template('article.html', article=article, selected_lang=lang)
    render_time = time.time() - render_start
    print(f"Rendering template for '{title}' took: {render_time:.3f} seconds")
    
    total_time = time.time() - start_time
    print(f"Total time for /article_page/{title}: {total_time:.3f} seconds")
    return response

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)  # For local testing, not production
