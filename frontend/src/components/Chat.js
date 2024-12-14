import React, { useState } from 'react';

const Chat = () => {
  const [messages, setMessages] = useState([]); 
  const [message, setMessage] = useState(''); 

  const sendMessage = () => {
    if (message.trim()) {
      setMessages([...messages, { text: message, sender: 'You' }]); 
      setMessage(''); 
  };

  return (
    <div className="p-6 max-w-md mx-auto bg-white rounded-xl shadow-md">
      <h2 className="text-xl font-semibold mb-4">Chat with Your Match</h2>
      
      {/* Display Messages */}
      <div className="mb-4">
        {messages.map((msg, index) => (
          <div key={index} className="flex space-x-2 mb-2">
            <span className="font-semibold">{msg.sender}:</span>
            <span>{msg.text}</span>
          </div>
        ))}
      </div>

      {/* Input Field and Button */}
      <input
        type="text"
        className="border p-2 w-full rounded"
        value={message}
        onChange={(e) => setMessage(e.target.value)} 
        placeholder="Type a message"
      />
      <button
        onClick={sendMessage}
        className="mt-2 px-4 py-2 bg-blue-600 text-white rounded w-full"
      >
        Send
      </button>
    </div>
  );
};
}
export default Chat;
