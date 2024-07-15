class ActionProvider {
    constructor(createChatBotMessage, setStateFunc) {
        this.createChatBotMessage = createChatBotMessage
        this.setState = setStateFunc
    }

    handleSummarize = () => {
        const loadingMessage = this.createChatBotMessage("Loading...")
        this.updateChatbotState(loadingMessage)
        this.sendPostRequest("http://localhost:5000/api/summarize", {
            url: "https://risi.muenchen.de/risi/sitzungsvorlage/detail/8524173",
        })
    }

    handleProjectInfo = () => {
        const message = this.createChatBotMessage(
            "Extracting information about the project..."
        )
        this.updateChatbotState(message)
        this.sendPostRequest("http://localhost:5000/api/find-info", {
            url: "https://risi.muenchen.de/risi/sitzungsvorlage/detail/8524173",
        })
    }

    handleMessage = (message) => {
        const loadingMessage = this.createChatBotMessage("Processing your message...")
        this.updateChatbotState(loadingMessage)
        console.log("Sending message to backend:", message)
        this.sendPostRequest("http://localhost:5000/api/chatbot", { message })
    }

    sendPostRequest = async (url, data) => {
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            })

            if (response.ok) {
                const responseData = await response.json()
                if (responseData.summaries) {
                    const summaries = responseData.summaries || []
                    this.setState((prevState) => {
                        const messages = prevState.messages.slice(0, -1) // Remove the loading message
                        summaries.forEach((summary) => {
                            const htmlMessage = this.createChatBotMessage(
                                summary.content // Use summary content directly
                            )
                            messages.push(htmlMessage)
                        })
                        return { ...prevState, messages }
                    })
                } else if (responseData.reply) {
                    console.log(responseData.reply);
                    this.setState((prevState) => {
                        const messages = prevState.messages.slice(0, -1); // Remove the loading message
                        const replyMessage = this.createChatBotMessage(responseData.reply);
                        messages.push(replyMessage);
                        return { ...prevState, messages };
                    })
                } else {
                    this.setState((prevState) => {
                        const messages = prevState.messages.slice(0, -1) // Remove the loading message
                        const {
                            emails,
                            phone_numbers,
                            location,
                            author,
                            partners,
                        } = responseData
                        let infoMessage = ""
                        if (emails && emails.length)
                            infoMessage += `Emails: ${emails.join(", ")}\n`
                        if (phone_numbers && phone_numbers.length)
                            infoMessage += `Phone numbers: ${phone_numbers.join(
                                ", "
                            )}\n`
                        if (location && location.length)
                            infoMessage += `Locations: ${location.join(", ")}\n`
                        if (author && author.length)
                            infoMessage += `Authors: ${author.join(", ")}\n`
                        if (partners && partners.length)
                            infoMessage += `Partners: ${partners.join(", ")}\n`
                        const msg = this.createChatBotMessage(infoMessage)
                        messages.push(msg)
                        return { ...prevState, messages }
                    })
                }
            } else {
                console.error("Error:", response.statusText)
                const message = this.createChatBotMessage(
                    "Sorry, there was an error processing your request."
                )
                this.updateChatbotState(message)
            }
        } catch (error) {
            console.error("Error:", error)
            const message = this.createChatBotMessage(
                "Sorry, there was an error processing your request."
            )
            this.updateChatbotState(message)
        }
    }

    updateChatbotState = (message) => {
        this.setState((prevState) => ({
            ...prevState,
            messages: [...prevState.messages, message],
        }))
    }
}

export default ActionProvider
