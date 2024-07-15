document.addEventListener('DOMContentLoaded', function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      var currentTab = tabs[0];
      if (currentTab) {
        // Check if the URL of the current tab starts with the desired base URL
        if (currentTab.url.startsWith("https://risi.muenchen.de/")) {
          document.getElementById('url').textContent = currentTab.url;
        } else {
          document.getElementById('url').textContent = "Unsupported";
        }
      }
    });
  });
  