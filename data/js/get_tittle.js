 $(document).ready(function() {
            // Function to fetch title from the server
            function fetchTitle() {
                $.ajax({
                    url: "/get_title/2", // Assuming the title ID is 1, replace with the appropriate ID
                    type: "GET",
                    success: function(response) {
                        // Update the text content of the navbar-brand link
                        $(".navbar-brand").text(response.title);
                    },
                    error: function(xhr, status, error) {
                        console.error("Error fetching title:", error);
                    }
                });
            }

            // Call the fetchTitle function when the page loads
            fetchTitle();
        });