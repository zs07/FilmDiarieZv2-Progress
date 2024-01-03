// Like button click event
document.getElementById('likeButton').addEventListener('click', function () {
    // Toggle 'clicked' class for visual feedback
    var likeButton = document.getElementById('likeButton');
    likeButton.classList.toggle('clicked');
  
    // Get movie ID from data attribute
    var movieId = likeButton.getAttribute('data-movie-id');
  
    // Send POST request to like_review endpoint
    fetch(`/like_review/${movieId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),  // Include CSRF token
        },
    })
    // Parse response as JSON
    .then(response => response.json())
    // Update like count on the page
    .then(data => {
        var likeCountElement = document.getElementById('likeCount');
        likeCountElement.textContent = data.review_likes;
    });
});

// Function to get CSRF token from cookies
function getCookie(name) {
    var cookieValue = null;
    // Check if cookies exist
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        // Iterate through cookies to find the CSRF token
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Check if the cookie matches the specified name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                // Break out of the loop once the token is found
                break;
            }
        }
    }
    // Return the CSRF token value
    return cookieValue;
}
