import React, { useState, useEffect } from 'react';
import axios from '../axiosConfig'; // Ensure you have this configured

const Chat = ({ currentUserId, matchUserId, matchUserName }) => {
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState('');

  // Fetch messages on mount or when user changes
  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const response = await axios.get('/messages/between', {
          params: { sender_id: currentUserId, receiver_id: matchUserId },
        });
        setMessages(response.data);
      } catch (error) {
        console.error('Error fetching messages:', error);
      }
    };

    if (currentUserId && matchUserId) {
      fetchMessages();
    }
  }, [currentUserId, matchUserId]);

  // Polling mechanism for real-time updates
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const response = await axios.get('/messages/between', {
          params: { sender_id: currentUserId, receiver_id: matchUserId },
        });
        setMessages(response.data);
      } catch (error) {
        console.error('Error fetching new messages:', error);
      }
    }, 3000); // Poll every 3 seconds
    return () => clearInterval(interval);
  }, [currentUserId, matchUserId]);

  const sendMessage = async () => {
    if (message.trim() && currentUserId && matchUserId) {
      try {
        const response = await axios.post('/messages', {
          sender_id: currentUserId,
          receiver_id: matchUserId,
          content: message,
        });

        const newMessage = {
          id: response.data.message_id,
          sender_id: currentUserId,
          receiver_id: matchUserId,
          content: message,
          timestamp: new Date().toISOString(),
        };

        setMessages([...messages, newMessage]);
        setMessage('');
      } catch (error) {
        console.error('Error sending message:', error);
      }
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto bg-white rounded-xl shadow-md">
      <h2 className="text-xl font-semibold mb-4">Chat with {matchUserName}</h2>

      {/* Display Messages */}
      <div className="mb-4 h-64 overflow-y-auto">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex space-x-2 mb-2 ${
              msg.sender_id === currentUserId ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`p-2 rounded ${
                msg.sender_id === currentUserId ? 'bg-blue-100' : 'bg-gray-100'
              }`}
            >
              <span>{msg.content}</span>
              <br />
              <small className="text-gray-500 text-xs">
                {new Date(msg.timestamp).toLocaleString()}
              </small>
            </div>
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

export default Chat;
