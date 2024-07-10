chrome.runtime.sendMessage({ action: 'getCurrentTabUrl' }, (response) => {
    if (response && response.url) {
        // Do something with the URL or send it to your ActionProvider
        window.postMessage({ type: 'TAB_URL', url: response.url }, '*');
    }
});
