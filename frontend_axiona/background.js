chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "getURL") {
      chrome.tabs.query({active: true, currentWindow: true}, tabs => {
        if (tabs.length > 0 && tabs[0].url) {
          sendResponse({url: tabs[0].url});
        } else {
          sendResponse({url: "No active tab"});
        }
      });
      return true;  // Keep the message channel open
    }
  });
  