// CustomWidget.js
import React from 'react';
import './CustomWidget.css'; // Ensure you have appropriate CSS for styling

const CustomWidget = ({ payload }) => {
    const { title, content } = payload;

    return (
        <details className="custom-details">
            <summary className="custom-summary">{title}</summary>
            <div className="custom-content" dangerouslySetInnerHTML={{ __html: content }} />
        </details>
    );
};

export default CustomWidget;
