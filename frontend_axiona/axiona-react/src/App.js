// src/App.js
import React, { useEffect, useState } from "react"

function App() {
    const [isOpen, setIsOpen] = useState(false)
    const [url, setUrl] = useState("undefined")
    useEffect(() => {
        const toggleChat = (event) => {
            console.log("EVENT", event)
            setUrl(event.detail.url)
            setIsOpen((prev) => !prev)
        }

        window.addEventListener("toggleChat", toggleChat)
        return () => window.removeEventListener("toggleChat", toggleChat)
    }, [])

    return (
        <div className={`chat-window ${!isOpen ? "hidden" : ""}`}>
            {url ? <p>{url}</p> : <p>Unsupported or no URLsss</p>}
        </div>
    )
}

export default App
