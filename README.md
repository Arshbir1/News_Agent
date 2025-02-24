# DAL-News 📰
[DAL-NEWS](https://news-agent.onrender.com).

Welcome to *DAL-News*, an innovative news aggregation platform that brings the latest stories from diverse RSS feeds to your fingertips! Powered by Flask, Elasticsearch, and a sleek frontend, DAL-News lets you explore articles by category, search with fuzzy matching, and dive into detailed article pages with related content. Whether you're a news junkie or a developer looking to tinker, this project has something for you.

Deployed on [Render](https://render.com/), DAL-News is ready to scale, but you can also run it locally or deploy it elsewhere. Let’s get started!

## Features ✨

- *Dynamic Categories*: Browse news from "Top", "Sports", "World", "States", "Cities", "Entertainment", and custom filters like Karnataka and Bengaluru.
- *Smart Search*: Fuzzy search across titles and content for quick article discovery.
- *Article Details*: View summaries, images, and publication dates, with related articles powered by Elasticsearch’s more_like_this.
- *Multilingual Support*: Translate articles into languages like Spanish or French on the fly.
- *Real-Time Updates*: Fetch fresh RSS content with a simple API call.
- *Analytics*: Track usage with [Google Analytics](https://analytics.google.com/analytics/web/?authuser=1#/p479341129/realtime/overview?params=_u..nav%3Dmaui%26_u..comparisons%3D%5B%7B%22savedComparisonId%22:%2210304435997%22,%22name%22:%22All%20Users%22,%22isEnabled%22:true,%22filters%22:%5B%5D,%22systemDefinedSavedComparisonType%22:8,%22isSystemDefined%22:true%7D%5D). To track usage one must sign in Google analytics and send the request access email to the Admin.

## Tech Stack 🛠

- *Backend*: Flask (Python), Elasticsearch Cloud
- *Frontend*: HTML, CSS, JavaScript (with dynamic rendering)
- *Data*: RSS feeds (NDTV), parsed with feedparser
- *Deployment*: Render (with alternatives like Heroku or Docker)

## Prerequisites 📋

To build, run, or deploy DAL-News, you’ll need:
- [Python 3.11+](https://www.python.org/downloads/) - The backbone of the app.
- [Git](https://git-scm.com/downloads) - For version control and cloning.
- [Elasticsearch Cloud](https://www.elastic.co/cloud) - Sign up for a free trial or paid plan.
- A code editor (e.g., [VS Code](https://code.visualstudio.com/), [PyCharm](https://www.jetbrains.com/pycharm/)).
- Optional: [Docker](https://www.docker.com/get-started) for containerized deployment.

## Project Structure 🌳

```plaintext
DAL-News/
  ├── static/              # Frontend assets
  │   ├── styles.css       # Custom styles
  │   ├── script.js        # Dynamic JavaScript
  │   └── news_logo.jpg    # Logo image
  ├── templates/           # HTML templates
  │   ├── index.html       # Homepage
  │   └── article.html     # Article details
  ├── app.py               # Core Flask app
  ├── DataExtractor.py     # RSS scraping and indexing
  ├── Translator.py        # Language translation
  ├── category.py          # Category filtering
  ├── search.py            # Search logic
  ├── requirements.txt     # Python dependencies
  ├── Dockerfile           # Optional Docker setup
  └── README.md            # You’re here!

## Setup Instructions

sh
git clone https://github.com/your-username/DAL-News.git
cd DAL-News

### 3. Install Dependencies
markdown
sh
pip install -r requirements.txt

### 4. Set Up Elasticsearch
- Sign up for [Elasticsearch Cloud](https://www.elastic.co/cloud).
- Configure your Elasticsearch host, username, and password in app.py.

### 5. Run the Application
markdown

sh
python app.py

The app should now be running on http://127.0.0.1:5000/.

### 6. Deploy (Optional)
To deploy on Render, **Heroku, or **Docker, follow their respective guides.

---

## Contribution & Support 🌟

Interested in improving DAL-News? Feel free to fork the repo, submit pull requests, or raise issues for feature requests or bugs.

- Contribute: [GitHub Repository](https://github.com/your-username/DAL-News)
- Report Issues: Open a GitHub issue
- Contact: Reach out via email or discussions on the repository

---

## Hackathon Information 🏆

This project was made for the Flipr Hackathon 2025.

---

## Thank You! 🎉

Thank you for checking out DAL-News! Happy coding & stay informed! 📰🚀
