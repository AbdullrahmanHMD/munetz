// src/chatbotConfig.js
import { createChatBotMessage } from "react-chatbot-kit";
import React from "react";
import CustomOptions from "./CustomOptions";
import robot from '../robot.png';
import ChatbotMessage from "./ChatbotMessage";
import CustomWidget from "./CustomWidget";

const config = {
    botName: "MuNetz",
    initialMessages: [
        createChatBotMessage("Here are some things you can ask me:", {
            widget: "options"
        }),
    ],    customStyles: {
        botMessageBox: {
            backgroundColor: "#1B98D5"
        },
        chatButton: {
            backgroundColor: "#1B98D5",
        },
    },
    customComponents: {
        botAvatar: (props) => <img src={robot} alt="robot" className="robot" {...props} />,
    },
    widgets: [
        {
            widgetName: "options",
            widgetFunc: (props) => <CustomOptions {...props} />,
        },
        {
            widgetName: "custom",
            widgetFunc: (props) => <CustomWidget {...props} />,
        },
    ],
};

export default config;
