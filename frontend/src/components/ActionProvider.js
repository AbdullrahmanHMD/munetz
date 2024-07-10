class ActionProvider {
    constructor(createChatBotMessage, setStateFunc) {
        this.createChatBotMessage = createChatBotMessage;
        this.setState = setStateFunc;
    }

    handleSummarize = () => {
        const loadingMessage = this.createChatBotMessage("Loading...");
        this.updateChatbotState(loadingMessage);
        this.sendPostRequest('http://localhost:5000/api/summarize', { url: 'https://risi.muenchen.de/risi/sitzungsvorlage/detail/8524173' });
    };

    handleProjectInfo = () => {
        const message = this.createChatBotMessage("Here is some information about the project.");
        this.updateChatbotState(message);
        this.sendPostRequest('http://localhost:5000/api/project-info', { projectId: 'Your project ID here' });
    };

    sendPostRequest = async (url, data) => {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                const responseData = await response.json();
                const summaries = responseData.summaries || [];
                this.setState(prevState => {
                    const messages = prevState.messages.slice(0, -1); // Remove the loading message
                    summaries.forEach(summary => {
                        const htmlMessage = this.createChatBotMessage(
                            summary.content,  // Use summary content directly
                        );
                        messages.push(htmlMessage);
                    });
                    return { ...prevState, messages };
                });
            } else {
                console.error('Error:', response.statusText);
                const message = this.createChatBotMessage('Sorry, there was an error processing your request.');
                this.updateChatbotState(message);
            }
        } catch (error) {
            console.error('Error:', error);
            const message = this.createChatBotMessage('Sorry, there was an error processing your request.');
            this.updateChatbotState(message);
        }
    };

    updateChatbotState = (message) => {
        this.setState((prevState) => ({
            ...prevState,
            messages: [...prevState.messages, message],
        }));
    };
}

export default ActionProvider;
