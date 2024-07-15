if (window.location.hostname.includes("risi.muenchen.de")) {
    const bubble = document.createElement("div")
    bubble.className = "bubble"
    document.body.appendChild(bubble)

    const root = document.createElement("div")
    root.id = "root"
    document.body.appendChild(root)

    // Ensure the root element is fully in the DOM before loading the React script
    setTimeout(() => {
        const script = document.createElement("script")
        script.src = chrome.runtime.getURL("axiona-react/dist/react_bundle.js")
        script.onload = () => script.remove()
        ;(document.head || document.documentElement).appendChild(script)
    }, 0)

    bubble.addEventListener("click", () => {
        chrome.runtime.sendMessage({ action: "getURL" }, (response) => {
            let url = "NOT FOUND"
            if (response) {
                url = response.url.startsWith("https://risi.muenchen.de/")
                    ? response.url
                    : "Unsupported"
            } else {
                chatWindow.textContent = "Error: No response from background."
            }
            window.dispatchEvent(
                new CustomEvent("toggleChat", { detail: { url } })
            )
        })
    })

    const icon = document.createElement("img")
    icon.src = "https://cdn-icons-png.flaticon.com/512/8943/8943377.png" // Replace with your actual image URL
    bubble.appendChild(icon)
}
