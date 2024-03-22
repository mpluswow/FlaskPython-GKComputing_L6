// get_profile.js

// Fetch user profile data from the server
fetch('/get_user_profile')
    .then(response => response.json())
    .then(data => {
        // Update user profile information in the HTML document
        document.getElementById('accountName').textContent = `${data.full_name}`;
        document.getElementById('userAge').textContent = `Age: ${data.age}`;
        document.getElementById('userTown').textContent = `Location: ${data.town}`;
    })
    .catch(error => console.error('Error fetching user profile:', error));
