var inactivityTimeout = 150000; // 2.5 minutes
var timeoutTimer;

function resetTimer() {
    clearTimeout(timeoutTimer);
    timeoutTimer = setTimeout(logout, inactivityTimeout);
}

document.addEventListener("mousemove", resetTimer);
document.addEventListener("keypress", resetTimer);

function logout() {
    // Redirect to the logout URL
    window.location.href = '/logout';
}

// Start the timer on page load
resetTimer();
