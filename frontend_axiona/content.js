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

    const returnResponse = (response) => {
        window.dispatchEvent(
            new CustomEvent("responseReceived", { detail: { response } })
        )
    }

    const sendExtensionMessage = (message) => {
        returnResponse({ type: "extension", data: message })
    }

    const grabUrl = (callback) => {
        chrome.runtime.sendMessage({ action: "getURL" }, (response) => {
            let url = null
            if (response) {
                url = response.url.startsWith("https://risi.muenchen.de/")
                    ? response.url
                    : "Unsupported"
            }
            if (url) callback(url)
            else log.error("Could not grab page URL")
        })
    }

    window.addEventListener("requestSummaries", () => {
        const callSummarization = async (url) => {
            const endpoint =
                "https://lxmzr818ca.execute-api.eu-central-1.amazonaws.com/main/summarize"
            console.log("Calling summarize on:", url) // This should show in the console when the function is triggered
            try {
                const response = await fetch(endpoint, {
                    method: "POST",
                    body: JSON.stringify({
                        url,
                    }),
                    headers: {
                        "Content-Type": "application/json",
                        "x-api-key": "pYMgUqFcOo9G76djh6olL9xRWOQ3iCjy5Q1pCipW",
                    },
                })
                const json = await response.json()
                console.log("Response:", json) // Log response for debugging
                if (response.ok) {
                    returnResponse({ type: "summarization", data: json })
                } else {
                    console.log("Error fetching summary:", json)
                }
            } catch (error) {
                console.error("Fetch error:", error)
            }
        }
        sendExtensionMessage("Summarizing documents...")
        grabUrl((url) => callSummarization(url))
    })

    window.addEventListener("requestChatbot", (event) => {
        const callChatbot = async (message) => {
            const endpoint =
                "https://lxmzr818ca.execute-api.eu-central-1.amazonaws.com/main/chatbot"
            console.log("Calling chatbot with:", message) // This should show in the console when the function is triggered
            try {
                const response = await fetch(endpoint, {
                    method: "POST",
                    body: JSON.stringify({
                        prompt: message,
                    }),
                    headers: {
                        "Content-Type": "application/json",
                        "x-api-key": "pYMgUqFcOo9G76djh6olL9xRWOQ3iCjy5Q1pCipW",
                    },
                })
                const json = await response.json()
                console.log("Response:", json) // Log response for debugging
                if (response.ok) {
                    returnResponse({ type: "chatbot", data: json })
                } else {
                    console.log("Error fetching summary:", json)
                }
            } catch (error) {
                console.error("Fetch error:", error)
            }
        }
        sendExtensionMessage("...")
        const msg = event.detail.message
        if (msg) callChatbot(msg)
    })

    window.addEventListener("requestExtraction", () => {
        const callInfoExtraction = async (url) => {
            const endpoint =
                "https://lxmzr818ca.execute-api.eu-central-1.amazonaws.com/main/find-info"
            console.log("Calling extract on:", url) // This should show in the console when the function is triggered
            try {
                const response = await fetch(endpoint, {
                    method: "POST",
                    body: JSON.stringify({
                        url: "https://risi.muenchen.de/risi/sitzungsvorlage/detail/8524173",
                    }),
                    headers: {
                        "Content-Type": "application/json",
                        "x-api-key": "pYMgUqFcOo9G76djh6olL9xRWOQ3iCjy5Q1pCipW",
                    },
                })
                const json = await response.json()
                console.log("Response:", json) // Log response for debugging
                if (response.ok) {
                    returnResponse({ type: "info-extraction", data: json })
                } else {
                    console.log("Error fetching extraction:", json)
                }
            } catch (error) {
                console.error("Fetch error:", error)
            }
        }
        sendExtensionMessage("Extracting information...")
        grabUrl((url) => callInfoExtraction(url))
    })

    bubble.addEventListener("click", () => {
        window.dispatchEvent(new CustomEvent("toggleChat"))
    })

    const icon = document.createElement("img")
    icon.src = "https://gcdnb.pbrd.co/images/J6EbqP5W2JkS.png?o=1" // Replace with your actual image URL
    bubble.appendChild(icon)
}
