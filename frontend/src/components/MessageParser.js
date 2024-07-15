class MessageParser {
    constructor(actionProvider) {
        this.actionProvider = actionProvider;
    }

    parse(message) {
        // Handle the message parsing logic
        if (message.includes('document')) {
            this.actionProvider.handleDocumentSummary();
        } else if (message.includes('project')) {
            this.actionProvider.handleProjectInfo();
        } else {
            this.actionProvider.handleMessage(message);
        }
    }
}

export default MessageParser;
