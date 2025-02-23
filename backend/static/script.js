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