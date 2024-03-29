document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Get username and password from form
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // Make an API call for authentication
    authenticateUser(username, password);
});

function authenticateUser(username, password) {
    // Example API endpoint for authentication
    var apiUrl = 'http://127.0.0.1:5000/authenticateStudent';

    // Example POST request to authenticate user
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => {
        if (response.ok) {
            // If authentication successful, display success message
            document.getElementById('login-message').innerText = 'Logged in successfully!';
            document.getElementById('login-message').style.backgroundColor = 'green';
            setTimeout(function() {
                window.location.href = '/studentDashboard';
            }, 2000); // Wait for 2 seconds
        } else {
            // If authentication failed, display error message
            document.getElementById('login-message').innerText = 'Authentication failed. Please check your credentials.';
            document.getElementById('login-message').style.backgroundColor = 'red';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle any errors that occurred during the fetch
        document.getElementById('login-message').innerText = 'An error occurred while authenticating. Please try again later.';
    });
}
