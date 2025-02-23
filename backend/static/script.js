async function loadCategory(category) {
    showLoading();
    try {
        const response = await fetch(`/category/${category}`);
        const articles = await response.json();
        console.log(`Fetched articles for category '${category}':`, articles);  // Debugging
        renderArticles(articles);
    } catch (error) {
        console.error(`Error loading category '${category}':`, error);  // Debugging
        alert("Failed to load articles.");
    } finally {
        hideLoading();
    }
}

async function loadBengaluruNews() {
    showLoading();
    try {
        // Call the search endpoint with the query "Bengaluru"
        const response = await fetch(`/search?q=Bengaluru`);
        const articles = await response.json();
        console.log("Fetched Bengaluru news:", articles);  // Debugging
        renderArticles(articles);
    } catch (error) {
        console.error("Error loading Bengaluru news:", error);  // Debugging
        alert("Failed to load Bengaluru news.");
    } finally {
        hideLoading();
    }
}

async function loadKarnatakaNews() {
    showLoading();
    try {
        // Call the search endpoint with the query "Karnataka"
        const response = await fetch(`/search?q=Karnataka`);
        const articles = await response.json();
        console.log("Fetched Karnataka news:", articles);  // Debugging
        renderArticles(articles);
    } catch (error) {
        console.error("Error loading Karnataka news:", error);  // Debugging
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
        // Pass the search query as a query parameter
        const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
        const articles = await response.json();
        console.log(`Fetched articles for search query '${query}':`, articles);  // Debugging
        renderArticles(articles);
    } catch (error) {
        console.error(`Error searching articles:`, error);  // Debugging
        alert("Failed to search articles.");
    } finally {
        hideLoading();
    }
}

async function loadArticleDetails(title) {
    const detailsDiv = document.getElementById(`details-${title.replace(/ /g, '-')}`);
    if (detailsDiv.innerHTML) {
        // Toggle visibility if details are already loaded
        detailsDiv.style.display = detailsDiv.style.display === 'none' ? 'block' : 'none';
        return;
    }

    showLoading();
    try {
        // Encode the title for the URL
        const encodedTitle = encodeURIComponent(title);
        const response = await fetch(`/article/${encodedTitle}`);
        const article = await response.json();
        if (article.error) {
            alert(article.error);
            return;
        }

        // Display article details
        detailsDiv.innerHTML = `
            <p><strong>Summary:</strong> ${article.summary || "No summary available."}</p>
            <p><strong>Content:</strong> ${article.content || "No content available."}</p>
            <p><strong>Source:</strong> <a href="${article.link}" target="_blank">Read more</a></p>
            <img src="${article.image_url}" alt="${article.title}" style="width:200px;">
        `;
        detailsDiv.style.display = 'block';
    } catch (error) {
        console.error(`Error loading article details: ${error}`);
        alert("Failed to load article details.");
    } finally {
        hideLoading();
    }
}

function renderArticles(articles) {
    const articlesDiv = document.getElementById('news-articles');
    articlesDiv.innerHTML = ''; // Clear previous articles
    if (articles.length === 0) {
        articlesDiv.innerHTML = '<p>No articles found for this category.</p>';
        return;
    }
    articles.forEach(article => {
        const articleDiv = document.createElement('div');
        articleDiv.className = 'article';
        articleDiv.innerHTML = `
            <h2><a href="/article/${encodeURIComponent(article.title)}" style="text-decoration: none; color: blue;">${article.title}</a></h2>
            <img src="${article.image_url}" alt="${article.title}" style="width:200px;">
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
/* General Styles */
body {
    font-family: 'Georgia', serif; /* Classic news-style font */
    margin: 0;
    padding: 0;
    background-color: #f9f9f9; /* Light gray background */
    color: #333; /* Dark text for readability */
    line-height: 1.6;
}

h1 {
    text-align: center;
    font-size: 36px;
    color: #ff0000; /* Red heading */
    font-family: 'Helvetica', sans-serif; /* Modern sans-serif for headings */
    margin-top: 20px;
}

/* Categories Section */
#categories {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin: 20px 0;
}

#categories button {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    background-color: #000000; /* Black buttons */
    color: white;
    cursor: pointer;
    font-size: 14px;
    font-family: 'Helvetica', sans-serif; /* Modern sans-serif for buttons */
    transition: background-color 0.3s ease, transform 0.3s ease;
}

#categories button:hover {
    background-color: #333; /* Dark gray on hover */
    transform: translateY(-3px); /* Slight lift on hover */
}

/* Search Section */
#search {
    text-align: center;
    margin: 20px 0;
}

#search input {
    padding: 10px;
    border: 2px solid #ff0000; /* Red border */
    border-radius: 5px;
    font-size: 14px;
    width: 300px;
    margin-right: 10px;
}

#search button {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    background-color: #000000; /* Black button */
    color: white;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s ease, transform 0.3s ease;
}

#search button:hover {
    background-color: #333; /* Dark gray on hover */
    transform: translateY(-3px); /* Slight lift on hover */
}

/* Loading Indicator */
#loading {
    text-align: center;
    font-size: 18px;
    color: #ff0000; /* Red text */
    margin: 20px 0;
}

/* News Articles Section */
#news-articles {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    padding: 20px;
    perspective: 1000px; /* For 3D effect */
}

.article-card {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    transform-style: preserve-3d; /* Enable 3D transformations */
    transition: transform 0.5s ease, box-shadow 0.5s ease;
}

.article-card:hover {
    transform: rotateY(5deg) scale(1.02); /* Subtle 3D rotation and scale on hover */
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.article-card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    transition: transform 0.5s ease;
}

.article-card:hover img {
    transform: scale(1.1); /* Zoom effect on hover */
}

.article-card h2 {
    font-size: 20px;
    margin: 15px;
    color: #ff0000; /* Red heading */
    font-family: 'Helvetica', sans-serif; /* Modern sans-serif for headlines */
}

.article-card p {
    font-size: 14px;
    margin: 15px;
    color: #555;
}

/* Scroll Down Feature */
@keyframes scrollDown {
    0% {
        transform: translateY(0);
    }
    100% {
        transform: translateY(20px);
    }
}

.scroll-down-indicator {
    text-align: center;
    margin-top: 20px;
    font-size: 24px;
    color: #ff0000;
    animation: scrollDown 1.5s infinite; /* Scroll down animation */
}
