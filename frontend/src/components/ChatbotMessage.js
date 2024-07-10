import React from 'react';

const ChatbotMessage = ({ message }) => {
    return (
        <div className="chatbot-message" dangerouslySetInnerHTML={{ __html: message }} />
    );
};

export default ChatbotMessage;
