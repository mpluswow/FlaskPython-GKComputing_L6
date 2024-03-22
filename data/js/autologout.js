var logoutTimer;

    function resetLogoutTimer() {
        clearTimeout(logoutTimer);
        logoutTimer = setTimeout(logout, 60000); // 1 minute = 60,000 milliseconds
    }

    function logout() {
        // Perform logout action here, for example redirecting to logout page
        window.location.href = "/logout";
    }

    // Add event listeners for user activity
    document.addEventListener("mousemove", resetLogoutTimer);
    document.addEventListener("keypress", resetLogoutTimer);

    // Initialize timer on page load
    window.onload = function() {
        resetLogoutTimer();
    };