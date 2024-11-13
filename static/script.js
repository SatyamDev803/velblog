 // Wait until the page is fully loaded
 document.addEventListener("DOMContentLoaded", function() {
    // Get all alert elements
    var alerts = document.querySelectorAll('.alert');
    
    // Loop through each alert and set a timeout to auto-dismiss
    alerts.forEach(function(alert) {
        setTimeout(function() {
            // Bootstrap 5's dismiss method for alerts
            alert.classList.remove('show'); // This triggers the fade out
            alert.classList.add('fade');    // This ensures it fades before disappearing
            setTimeout(() => alert.remove(), 500); // Removes from the DOM after fade out
        }, 3000); // Adjust 5000 ms (5 seconds) as needed
    });
});