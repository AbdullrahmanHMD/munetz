// src/App.js
import React from "react";
import Chatbot from "react-chatbot-kit";
import "react-chatbot-kit/build/main.css";
import './App.css';
import MessageParser from "./components/MessageParser";
import ActionProvider from "./components/ActionProvider"; // import the custom CSS file
import config from "./components/chatbotConfig";
function App() {
    return (
        <div className="App">
            <header className="App-header">
                    <Chatbot
                        config={config}
                        messageParser={MessageParser}
                        actionProvider={ActionProvider}
                    />
            </header>
        </div>
    );
}

export default App;
