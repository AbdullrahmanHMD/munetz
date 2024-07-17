// src/App.js
import React, { useEffect, useRef, useState } from "react"
import axionaIcon from '../../icons/axiona.png'

function App() {
    const feedEndRef = useRef(null)
    const [isOpen, setIsOpen] = useState(false) // TODO: change to false
    const [message, setMessage] = useState("")
    const [messageFeed, setMessageFeed] = useState([])
    useEffect(() => {
        const toggleChat = () => {
            setIsOpen((prev) => !prev)
        }

        const handleSummarization = (summaries) => {
            summaries.summaries.forEach((summary, index) => {
                let message = `Summary of ${summary.title}:\n${summary.content}`
                appendMessage(false, message, index === 0)
            });
        }
        const handleInfoExtraction = (info) => {
            const { emails, phone_numbers, location, author, partners } = info
            const message = `Emails:${emails}\nPhone:${phone_numbers}\nLocation:${location}\nAuthor:${author}\nPartners:${partners}\n`
            appendMessage(false, message, true)
        }
        const handleChatbot = (replyData) => {
            appendMessage(false, replyData.reply, true)
        }

        const handleExtensionMessage = (message) => {
            appendMessage(false, message)
        }

        const handleResponse = (event) => {
            const response = event.detail.response
            const data = response.data
            switch (response.type) {
                case "summarization":
                    return handleSummarization(data)
                case "info-extraction":
                    return handleInfoExtraction(data)
                case "chatbot":
                    return handleChatbot(data)
                case "extension":
                    return handleExtensionMessage(data)
            }
        }

        window.addEventListener("toggleChat", toggleChat)
        window.addEventListener("responseReceived", handleResponse)
        return () => {
            window.removeEventListener("toggleChat", toggleChat)
            window.removeEventListener("responseReceived", handleResponse)
        }
    }, [])

    const callSummarization = () => {
        window.dispatchEvent(new CustomEvent("requestSummaries"))
    }

    const callInfoExtraction = () => {
        window.dispatchEvent(new CustomEvent("requestExtraction"))
    }

    const appendMessage = (isSelf, message, removePrev) => {
        setMessageFeed((messages) => {
            let old = messages
            if (removePrev) {
                old = old.slice(0, old.length - 1)
            }
            return [...old, { isSelf, message }]
        })
    }

    const sendMessage = (e) => {
        e.preventDefault()
        let chatMessage = message
        if (!chatMessage.length) return
        appendMessage(true, chatMessage)
        window.dispatchEvent(
            new CustomEvent("requestChatbot", {
                detail: { message: chatMessage },
            })
        )
        setMessage("")
    }

    useEffect(() => {
        feedEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }, [messageFeed])

    return (
        <div className={`chat-window ${!isOpen ? "hidden" : ""}`}>
            <div className="chatbot-header">
                {/* <img
                    className="chatbot-logo"
                    src={axionaIcon}
                    alt="logo"
                /> */}
                <div className="header-title">Axiona</div>
                <div className="function-buttons">
                    <button
                        className="function-button"
                        onClick={callSummarization}
                    >
                        Summarize
                    </button>
                    <button
                        className="function-button"
                        onClick={callInfoExtraction}
                    >
                        Extract info
                    </button>
                </div>
            </div>
            <div className="chatbot-content">
                {messageFeed.map((message) => (
                    <div
                        className={`message-bubble ${
                            message.isSelf ? "self" : ""
                        }`}
                    >
                        {message.message}
                    </div>
                ))}
                <div ref={feedEndRef} />
            </div>
            <div className="chatbox-container">
                <form className="chatbox" onSubmit={sendMessage}>
                    <textarea
                        type="text"
                        value={message}
                        onChange={(event) => setMessage(event.target.value)}
                        placeholder="Message"
                    />
                    <button className="send-button">
                        send
                    </button>
                </form>
            </div>
        </div>
    )
}

export default App
