document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const category = urlParams.get('category');
    const searchQuery = urlParams.get('search'); // Get search parameter

    // Handle search-based categories (Karnataka, Bengaluru)
    if (searchQuery) {
        loadSearchResults(searchQuery);
    }
    // Handle standard category-based navigation
    else if (category) {
        loadCategory(category);
    }
    // Default to Top only if neither category nor search is present
    else if (window.location.pathname === '/') {
        loadCategory('Top');
    }
});

async function loadSearchResults(query) {
    showLoading();
    try {
        const response = await fetch(`${BASE_URL}/search?q=${encodeURIComponent(query)}`);
        if (!response.ok) {
            throw new Error(`Failed to load articles. Please try again later.`);
        }
        const articles = await response.json();
        console.log(`Fetched search results for '${query}':`, articles);
        renderArticles(articles);
    } catch (error) {
        console.error(`Error loading search results for '${query}':`, error);
        alert(error.message);
    } finally {
        hideLoading();
    }
}


const BASE_URL = window.location.origin;

// Load category from the article page
function loadCategoryFromArticle(category) {
    const specialCategories = ["Karnataka", "Bengaluru"];
    let newUrl;

    if (specialCategories.includes(category)) {
        newUrl = `${BASE_URL}/?search=${encodeURIComponent(category)}`;
    } else {
        newUrl = `${BASE_URL}/?category=${encodeURIComponent(category)}`;
    }

    window.location.href = newUrl; // Redirect to the correct page
}

async function loadCategory(category) {
    showLoading();
    
    // Update the URL without reloading the page
    const newUrl = `${BASE_URL}/?category=${encodeURIComponent(category)}`;
    window.history.pushState({ category }, "", newUrl);

    try {
        const response = await fetch(`${BASE_URL}/category/${category}`);
        if (!response.ok) {
            throw new Error(`Failed to load articles. Please try again later.`);
        }
        const articles = await response.json();
        console.log(`Fetched articles for category '${category}':`, articles);
        renderArticles(articles);
    } catch (error) {
        console.error(`Error loading category '${category}':`, error);
        alert(error.message);
    } finally {
        hideLoading();
    }
}

// Handle back/forward navigation
window.addEventListener("popstate", (event) => {
    if (event.state && event.state.category) {
        loadCategory(event.state.category);
    }
});


async function loadBengaluruNews() {
    showLoading();
    try {
        const response = await fetch(`${BASE_URL}/search?q=Bengaluru`);
        if (!response.ok) {
            throw new Error(`Failed to load articles. Please try again later.`);
        }
        const articles = await response.json();
        console.log("Fetched Bengaluru news:", articles);
        renderArticles(articles);
    } catch (error) {
        console.error("Error loading Bengaluru news:", error);
        alert(error.message);
    } finally {
        hideLoading();
    }
}

async function loadKarnatakaNews() {
    showLoading();
    try {
        const response = await fetch(`${BASE_URL}/search?q=Karnataka`);
        if (!response.ok) {
            throw new Error(`Failed to load articles. Please try again later.`);
        }
        const articles = await response.json();
        console.log("Fetched Karnataka news:", articles);
        renderArticles(articles);
    } catch (error) {
        console.error("Error loading Karnataka news:", error);
        alert(error.message);
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
        if (!response.ok) {
            throw new Error(`Failed to load articles. Please try again later.`);
        }
        const articles = await response.json();
        console.log(`Fetched articles for search query '${query}':`, articles);
        renderArticles(articles);
    } catch (error) {
        console.error(`Error searching articles:`, error);
        alert(error.message);
    } finally {
        hideLoading();
    }
}

function renderArticles(articles) {
    const articlesDiv = document.getElementById('news-articles');
    if (!articlesDiv) {
        console.error('Element with id "news-articles" not found. This function is intended for the homepage.');
        return;
    }
    articlesDiv.innerHTML = '';
    if (!articles || articles.length === 0) {
        articlesDiv.innerHTML = '<p>No articles found.</p>';
        return;
    }
    articles.forEach(article => {
        const articleDiv = document.createElement('div');
        articleDiv.className = 'article-card';
        articleDiv.innerHTML = `
            <h2><a href="/article_page/${encodeURIComponent(article.title)}">${article.title}</a></h2>
            <a href="/article_page/${encodeURIComponent(article.title)}">
                <img src="${article.image_url || 'https://via.placeholder.com/300'}" alt="${article.title}" class="article-image">
            </a>
            <p>${article.content.substring(0, 100)}...</p>
        `;
        articlesDiv.appendChild(articleDiv);
    });
}

function showLoading() {
    const loadingDiv = document.getElementById('loading');
    if (loadingDiv) {
        loadingDiv.style.display = 'block';
    }
}

function hideLoading() {
    const loadingDiv = document.getElementById('loading');
    if (loadingDiv) {
        loadingDiv.style.display = 'none';
    }
}

function translateArticle(lang) {
    const currentUrl = window.location.href.split('?')[0];  // Remove existing query params
    if (lang) {
        window.location.href = `${currentUrl}?lang=${lang}`;
    } else {
        window.location.href = currentUrl;  // Reset to default (no translation)
    }
}