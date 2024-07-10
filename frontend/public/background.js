chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'getCurrentTabUrl') {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            let activeTab = tabs[0];
            let activeTabUrl = activeTab.url;
            sendResponse({ url: activeTabUrl });
        });
        return true; // This is required to indicate you wish to send a response asynchronously
    }
});
