document.addEventListener("DOMContentLoaded", function () {
  // Get all alert elements
  var alerts = document.querySelectorAll('.alert');

  // Loop through each alert and set a timeout to auto-dismiss
  alerts.forEach(function (alert) {
    setTimeout(function () {
      // Bootstrap 5's dismiss method for alerts
      alert.classList.remove('show'); // This triggers the fade out
      alert.classList.add('fade');    // This ensures it fades before disappearing
      setTimeout(() => alert.remove(), 500); // Removes from the DOM after fade out
    }, 5000); // Adjust 5000 ms (5 seconds) as needed
  });
});

function toggleReplies(commentSno) {
  var repliesSection = document.getElementById('replies-' + commentSno);
  var toggleButton = document.getElementById('toggle-button-' + commentSno);
  
  // Toggle the visibility of the replies section
  if (repliesSection.style.display === "none" || repliesSection.style.display === "") {
    repliesSection.style.display = "block";  // Show replies
    toggleButton.innerText = "Hide Replies";  // Change button text to "Hide Replies"
  } else {
    repliesSection.style.display = "none";  // Hide replies
    toggleButton.innerText = "View Replies";  // Change button text to "View Replies"
  }
}

document.addEventListener("DOMContentLoaded", function() {
  let previews = document.getElementsByClassName('preview');
  Array.from(previews).forEach((element) => {
    element.innerHTML = element.innerText;
  });
});