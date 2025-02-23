import feedparser
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from elasticsearch import Elasticsearch

# Interval between checks (in seconds)
CHECK_INTERVAL = 60  # 1 minute

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
        basic_auth=(ES_USERNAME, ES_PASSWORD))
    return es

def scrape_article_content(url):
    """
    Scrape the content of an article from its URL.
    Extracts text between <p> tags and joins it.
    Handles 500 Server Errors and other exceptions.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes (4xx, 5xx)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text between <p> tags and join them
        paragraphs = soup.find_all('p')
        content = ' '.join(p.get_text(strip=True) for p in paragraphs)
        
        return content
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error scraping {url}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
    except Exception as e:
        print(f"Unexpected error scraping {url}: {e}")
    return None

def scrape_image_url(url):
    """
    Scrape the image URL from the article's webpage, excluding tracking pixels and ads.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for all <img> tags
        img_tags = soup.find_all('img')
        
        # Filter out tracking pixels and ads
        for img in img_tags:
            src = img.get('src') or img.get('data-src')
            if src and not any(keyword in src for keyword in ['scorecardresearch', 'ad', 'pixel', 'track', 'analytics']):
                return src
        
        # If no valid image is found, return None
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error scraping image from {url}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error scraping image from {url}: {e}")
    except Exception as e:
        print(f"Unexpected error scraping image from {url}: {e}")
    return None

def scrape_rss_feed(rss_url, category):
    """
    Parse the RSS feed and scrape content for each article.
    Adds a 'category' field and 'image_url' to each article.
    """
    feed = feedparser.parse(rss_url)
    
    articles = []
    
    for entry in feed.entries:
        # Scrape the article content
        content = scrape_article_content(entry.get('link'))
        
        # Extract image URL from the RSS feed (if available)
        image_url = None
        if 'media_content' in entry and entry.media_content:
            # Check if the media content is an image
            for media in entry.media_content:
                if media.get('type', '').startswith('image/'):
                    image_url = media.get('url')
                    break
        
        # If no image URL is found in the RSS feed, scrape it from the article's webpage
        if not image_url:
            image_url = scrape_image_url(entry.get('link'))
        
        article = {
            'title': entry.get('title', 'No Title'),
            'link': entry.get('link', 'No Link'),
            'published': entry.get('published', 'No Date'),
            'content': content,
            'category': category,  # Add category based on the RSS feed
            'image_url': image_url,  # Add image URL
            'last_updated': datetime.now().isoformat()  # Track when the article was last updated
        }
        
        if article['content']:  # Only add articles with successfully scraped content
            articles.append(article)
        # time.sleep(1)  # Add a delay to avoid overwhelming the server
    
    return articles

def article_exists_in_elasticsearch(es, link, index_name=ES_INDEX):
    """
    Check if an article with the given link already exists in Elasticsearch.
    """
    try:
        return es.exists(index=index_name, id=link)
    except Exception as e:
        print(f"Error checking if article exists in Elasticsearch: {e}")
        return False

def upload_to_elasticsearch(es, articles, index_name=ES_INDEX):
    """
    Upload articles to Elasticsearch.
    Deduplicates articles based on the 'link' field.
    """
    # Track the number of new articles uploaded
    new_articles_uploaded = 0

    for article in articles:
        link = article['link']
        
        # Check if the article already exists in Elasticsearch
        if not article_exists_in_elasticsearch(es, link, index_name):
            # Upload the article if it doesn't exist
            response = es.index(index=index_name, id=link, document=article)
            print(f"Uploaded article: {response['result']} (ID: {link})")
            new_articles_uploaded += 1
        else:
            print(f"Article already exists in Elasticsearch (ID: {link}). Skipping.")

    return new_articles_uploaded

def main():
    """
    Main function to scrape RSS feeds and upload new articles to Elasticsearch.
    """
    # Define your RSS feeds and their categories
    rss_feeds = {
        "Top": "https://feeds.feedburner.com/ndtvnews-top-stories",
        "Sports": "https://feeds.feedburner.com/ndtvsports-latest",
        "World": "https://feeds.feedburner.com/ndtvnews-world-news",
        "States": "https://feeds.feedburner.com/ndtvnews-south",
        "Cities": "https://feeds.feedburner.com/ndtvnews-cities-news",
        "Entertainment": "https://example.com/entertainment-rss"
    }

    # Connect to Elasticsearch
    es = connect_to_elasticsearch()
    if not es.ping():
        print("❌ Could not connect to Elasticsearch. Check your credentials and endpoint.")
        return

    # Scrape articles from each RSS feed
    new_articles = []
    for category, url in rss_feeds.items():
        print(f"Scraping {category} feed...")
        articles = scrape_rss_feed(url, category)
        new_articles.extend(articles)
        print(f"Found {len(articles)} articles in {category} feed.")

    # Upload only new articles to Elasticsearch
    if new_articles:
        new_articles_uploaded = upload_to_elasticsearch(es, new_articles)
        print(f"Uploaded {new_articles_uploaded} new articles to Elasticsearch.")
    else:
        print("No new articles found.")

# Run the script continuously
if __name__ == "__main__":
    while True:
        print(f"Starting RSS feed check at {datetime.now().isoformat()}")
        main()
        print(f"Waiting for {CHECK_INTERVAL // 60} minute(s) before the next check...")
        time.sleep(CHECK_INTERVAL)