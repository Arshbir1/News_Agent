from flask import Flask, jsonify, request, render_template
import time
from apscheduler.schedulers.background import BackgroundScheduler
try:
    from backend.Translator import translate_text
    from backend.category import extract_articles_by_category
    from backend.search import search_articles
except ModuleNotFoundError as e:
    print(f"Error: Could not import module - {e}")
    print("Ensure all backend files are in the same directory as app.py")
    exit(1)

from elasticsearch import Elasticsearch
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from backend.ContentSummarizer import summarize_text

app = Flask(__name__)

# Elasticsearch configuration
ES_ENDPOINT = "https://9fb474a7f57d4bfbbd9e05246ff0b8ec.asia-south1.gcp.elastic-cloud.com:443"
ES_USERNAME = "elastic"
ES_PASSWORD = "6lWF4jG8mE5IUnOSc66kmSo1"
ES_INDEX = "news-articles"
es = Elasticsearch(ES_ENDPOINT, basic_auth=(ES_USERNAME, ES_PASSWORD))

CATEGORIES = ["Top", "Sports", "World", "States", "Cities", "Entertainment"]
MAX_TOKEN_LIMIT = 1024
CHECK_INTERVAL = 60  # 1 minute for testing (change to 6*60*60 = 21600 for 6 hours in production)

# Flask Routes
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
    query = {"query": {"match": {"title": title}}}
    response = es.search(index=ES_INDEX, body=query)
    query_time = time.time() - start_time
    
    if response['hits']['total']['value'] == 0:
        print(f"No article found for title: '{title}'")
        return "Article not found", 404
    
    article = response['hits']['hits'][0]['_source']
    
    lang = request.args.get('lang', default=None)
    if lang:
        translate_start = time.time()
        article['title'] = translate_text(article['title'], lang) or article['title']
        article['summary'] = translate_text(article['summary'], lang) or article['summary']
        print(f"Translation for '{title}' took: {time.time() - translate_start:.3f} seconds")
    
    response = render_template('article.html', article=article, selected_lang=lang)
    print(f"Total time for /article_page/{title}: {time.time() - start_time:.3f} seconds")
    return response

# RSS Scraping Functions
def scrape_article_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        content = ' '.join(p.get_text(strip=True) for p in paragraphs)
        return content if content else None
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def scrape_image_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        img_tags = soup.find_all('img')
        for img in img_tags:
            src = img.get('src') or img.get('data-src')
            if src and not any(keyword in src for keyword in ['scorecardresearch', 'ad', 'pixel', 'track', 'analytics']):
                return src
        return None
    except Exception as e:
        print(f"Error scraping image from {url}: {e}")
        return None

def estimate_token_count(text):
    words = text.split()
    return int(len(words) / 0.75)

def scrape_rss_feed(rss_url, category):
    feed = feedparser.parse(rss_url)
    articles = []
    for entry in feed.entries:
        link = entry.get('link', 'No Link')
        if article_exists_in_elasticsearch(link):
            continue
        
        content = scrape_article_content(link)
        if not content:
            continue
        
        token_count = estimate_token_count(content)
        if token_count > MAX_TOKEN_LIMIT or token_count < 50:
            continue
        
        summary = summarize_text(content)
        if not summary or summary in ["No content available for summarization.", "Summarization failed due to an error."]:
            continue
        
        image_url = scrape_image_url(link) or next((m.get('url') for m in entry.get('media_content', []) if m.get('type', '').startswith('image/')), None)
        
        article = {
            'title': entry.get('title', 'No Title'),
            'link': link,
            'published': entry.get('published', 'No Date'),
            'content': content,
            'summary': summary,
            'category': category,
            'image_url': image_url,
            'last_updated': datetime.now().isoformat()
        }
        articles.append(article)
    return articles

def article_exists_in_elasticsearch(link):
    try:
        return es.exists(index=ES_INDEX, id=link)
    except Exception as e:
        print(f"Error checking if article exists: {e}")
        return False

def upload_to_elasticsearch(articles):
    new_articles_uploaded = 0
    for article in articles:
        link = article['link']
        if not article_exists_in_elasticsearch(link):
            es.index(index=ES_INDEX, id=link, document=article)
            new_articles_uploaded += 1
    return new_articles_uploaded

def scrape_and_update():
    rss_feeds = {
        "Top": "https://feeds.feedburner.com/ndtvnews-top-stories",
        "Sports": "https://feeds.feedburner.com/ndtvsports-latest",
        "World": "https://feeds.feedburner.com/ndtvnews-world-news",
        "States": "https://feeds.feedburner.com/ndtvnews-south",
        "Cities": "https://feeds.feedburner.com/ndtvnews-cities-news",
        "Entertainment": "https://example.com/entertainment-rss"
    }
    if not es.ping():
        print("❌ Could not connect to Elasticsearch.")
        return
    
    new_articles = []
    for category, url in rss_feeds.items():
        print(f"Scraping {category} feed...")
        articles = scrape_rss_feed(url, category)
        new_articles.extend(articles)
    
    if new_articles:
        new_uploaded = upload_to_elasticsearch(new_articles)
        print(f"Uploaded {new_uploaded} new articles.")
    else:
        print("No new articles found.")

# Scheduler Setup
scheduler = BackgroundScheduler()
scheduler.add_job(scrape_and_update, 'interval', seconds=CHECK_INTERVAL)
scheduler.start()

if __name__ == "__main__":
    try:
        app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
