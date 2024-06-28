// src/ActionProvider.js
class ActionProvider {
    constructor(createChatBotMessage, setStateFunc) {
        this.createChatBotMessage = createChatBotMessage;
        this.setState = setStateFunc;
    }
    handleSummarize = () => {
        const message = this.createChatBotMessage("Sure, I can summarize the document for you.");
        this.updateChatbotState(message);
    };

    handleProjectInfo = () => {
        const message = this.createChatBotMessage("Here is some information about the project.");
        this.updateChatbotState(message);
    };

    updateChatbotState = (message) => {
        this.setState((prevState) => ({
            ...prevState,
            messages: [...prevState.messages, message],
        }));
    };
}

export default ActionProvider;
