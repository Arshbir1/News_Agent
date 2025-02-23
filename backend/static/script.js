document.addEventListener('DOMContentLoaded', () => loadCategory('Top'));

const BASE_URL = window.location.origin;

async function loadCategory(category) {
    showLoading();
    try {
        const response = await fetch(`${BASE_URL}/category/${category}`);
        const articles = await response.json();
        console.log(`Fetched articles for category '${category}':`, articles);
        renderArticles(articles);
    } catch (error) {
        console.error(`Error loading category '${category}':`, error);
        alert("Failed to load articles.");
    } finally {
        hideLoading();
    }
}

async function loadBengaluruNews() {
    showLoading();
    try {
        const response = await fetch(`${BASE_URL}/search?q=Bengaluru`);
        const articles = await response.json();
        console.log("Fetched Bengaluru news:", articles);
        renderArticles(articles);
    } catch (error) {
        console.error("Error loading Bengaluru news:", error);
        alert("Failed to load Bengaluru news.");
    } finally {
        hideLoading();
    }
}

async function loadKarnatakaNews() {
    showLoading();
    try {
        const response = await fetch(`${BASE_URL}/search?q=Karnataka`);
        const articles = await response.json();
        console.log("Fetched Karnataka news:", articles);
        renderArticles(articles);
    } catch (error) {
        console.error("Error loading Karnataka news:", error);
        alert("Failed to load Karnataka news.");
    } finally {
        hideLoading();
    }
}

async function searchArticles() {
    showLoading();
    const query = document.getElementById('searchQuery').value;
    if (!query) {
        alert("Please enter a search term.");
        hideLoading();
        return;
    }
    try {
        const response = await fetch(`${BASE_URL}/search?q=${encodeURIComponent(query)}`);
        const articles = await response.json();
        console.log(`Fetched articles for search query '${query}':`, articles);
        renderArticles(articles);
    } catch (error) {
        console.error(`Error searching articles:`, error);
        alert("Failed to search articles.");
    } finally {
        hideLoading();
    }
}

function renderArticles(articles) {
    const articlesDiv = document.getElementById('news-articles');
    articlesDiv.innerHTML = '';
    if (!articles || articles.length === 0) {
        articlesDiv.innerHTML = '<p>No articles found.</p>';
        return;
    }
    articles.forEach(article => {
        const articleDiv = document.createElement('div');
        articleDiv.className = 'article-card';
        articleDiv.innerHTML = `
            <img src="${article.image_url || 'https://via.placeholder.com/300'}" alt="${article.title}">
            <h2><a href="/article_page/${encodeURIComponent(article.title)}">${article.title}</a></h2>
            <p>${article.content.substring(0, 100)}...</p>
        `;
        articlesDiv.appendChild(articleDiv);
    });
}

function showLoading() {
    document.getElementById('loading').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}