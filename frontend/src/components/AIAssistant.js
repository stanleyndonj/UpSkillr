import React, { useState } from 'react';
import axios from 'axios';

const AIAssistant = () => {
    const [message, setMessage] = useState('');
    const [response, setResponse] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            const { data } = await axios.post('/api/ai/chat', { message });
            setResponse(data.response);
        } catch (error) {
            console.error('Error getting AI response:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="ai-assistant-container">
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Ask your question..."
                    className="ai-input"
                />
                <button 
                    type="submit" 
                    disabled={isLoading}
                    className="ai-submit-btn"
                >
                    {isLoading ? 'Processing...' : 'Send'}
                </button>
            </form>
            {response && (
                <div className="ai-response">
                    {response}
                </div>
            )}
        </div>
    );
};

export default AIAssistant;