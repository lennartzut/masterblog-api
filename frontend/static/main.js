// Global variable to store the current search results
let currentSearchResults = [];

// Function that runs once the window is fully loaded
window.onload = function() {
    var savedBaseUrl = localStorage.getItem('apiBaseUrl');
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
        loadPosts();
    }
}

// Function to fetch and display posts (including after search)
function loadPosts() {
    // Retrieve the base URL and save it to local storage
    var baseUrl = document.getElementById('api-base-url').value;
    localStorage.setItem('apiBaseUrl', baseUrl);

    // Use the Fetch API to send a GET request to the /posts endpoint
    fetch(baseUrl + '/posts')
        .then(response => response.json())
        .then(data => {
            displayPosts(data); // Call a separate function to handle rendering
        })
        .catch(error => console.error('Error:', error));
}

// Function to display posts (to avoid repetition)
function displayPosts(posts) {
    const postContainer = document.getElementById('post-container');
    postContainer.innerHTML = '';  // Clear previous posts
    posts.forEach(post => {
        const postDiv = document.createElement('div');
        postDiv.className = 'post';
        postDiv.innerHTML = `<h2>${post.title}</h2><p>${post.content}</p>
            <button onclick="deletePost(${post.id})">Delete</button>`;
        postContainer.appendChild(postDiv);
    });
}

// Function to add a new post
function addPost() {
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('post-title').value;
    var postContent = document.getElementById('post-content').value;

    fetch(baseUrl + '/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: postTitle, content: postContent })
    })
    .then(response => response.json())
    .then(post => {
        console.log('Post added:', post);
        loadPosts();
    })
    .catch(error => console.error('Error:', error));
}

// Function to delete a post
function deletePost(postId) {
    var baseUrl = document.getElementById('api-base-url').value;

    // Use the Fetch API to send a DELETE request to the specific post's endpoint
    fetch(baseUrl + '/posts/' + postId, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
            // Filter the current search results to remove the deleted post
            currentSearchResults = currentSearchResults.filter(post => post.id !== postId);
            displayPosts(currentSearchResults); // Display the updated list of posts
        } else {
            console.error('Error deleting post:', response);
        }
    })
    .catch(error => console.error('Error:', error)); // If an error occurs, log it to the console
}

// Function to search posts by title or content
function searchPosts() {
    var baseUrl = document.getElementById('api-base-url').value;
    var searchTitle = document.getElementById('search-title').value;
    var searchContent = document.getElementById('search-content').value;

    let searchUrl = baseUrl + '/posts/search?';
    if (searchTitle) searchUrl += `title=${searchTitle}&`;
    if (searchContent) searchUrl += `content=${searchContent}`;

    fetch(searchUrl)
        .then(response => response.json())
        .then(data => {
            currentSearchResults = data;
            displayPosts(data);
        })
        .catch(error => console.error('Error:', error));
}

// Function to sort posts
function sortPosts() {
    var baseUrl = document.getElementById('api-base-url').value;
    var sortField = document.getElementById('sort-field').value;
    var sortDirection = document.getElementById('sort-direction').value;

    // Create query string for sorting
    var queryParams = [];
    if (sortField) queryParams.push(`sort=${encodeURIComponent(sortField)}`);
    if (sortDirection) queryParams.push(`direction=${encodeURIComponent(sortDirection)}`);

    var queryString = queryParams.length ? '?' + queryParams.join('&') : '';

    fetch(baseUrl + '/posts' + queryString)
        .then(response => response.json())
        .then(data => {
            const postContainer = document.getElementById('post-container');
            postContainer.innerHTML = '';  // Clear container

            data.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';
                postDiv.innerHTML = `<h2>${post.title}</h2><p>${post.content}</p>`;
                postContainer.appendChild(postDiv);
            });
        })
        .catch(error => console.error('Error:', error));
}
