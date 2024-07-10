// src/CustomOptions.js
import React from "react";
import "./CustomOptions.css";

const CustomOptions = (props) => {
    const options = [
        {
            text: "Summarize the document",
            handler: () => props.actionProvider.handleSummarize(),
            id: 1,
        },
        {
            text: "Project Information",
            handler: () => props.actionProvider.handleProjectInfo(),
            id: 2,
        },
    ];

    return (
        <div className="options-container">
            {options.map((option) => (
                <button key={option.id} className="option-button" onClick={option.handler}>
                    {option.text}
                </button>
            ))}
        </div>
    );
};

export default CustomOptions;
