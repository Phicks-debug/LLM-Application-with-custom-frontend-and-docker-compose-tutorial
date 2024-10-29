import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [apiStatus, setApiStatus] = useState('unknown');

  useEffect(() => {
    const checkApiStatus = async () => {
      try {
        await axios.get('http://localhost:8000/');
        console.log('API is online');
        setApiStatus('online');
      } catch (error) {
        setApiStatus('offline');
        console.error('API is offline:', error);
      }
    };
    checkApiStatus();
  }, []);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    if (apiStatus !== 'online') {
      setMessages((prevMessages) => [...prevMessages, { role: 'assistant', content: 'Error: API is not connected. Please try again later.' }]);
      return;
    }
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.get(`http://localhost:8000/chat?prompt=${encodeURIComponent(input)}`, {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      });
      const assistantMessage = { role: 'assistant', content: response.data.message };
      setMessages((prevMessages) => [...prevMessages, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      let errorMessage = 'Sorry, an error occurred. Please try again.';
      if (error.response) {
        errorMessage = `Error: ${error.response.status} - ${error.response.data.detail || error.response.statusText}`;
      } else if (error.request) {
        errorMessage = 'Error: No response received from the server. Please check if the API is running.';
      } else {
        errorMessage = `Error: ${error.message}`;
      }
      setMessages((prevMessages) => [...prevMessages, { role: 'assistant', content: errorMessage }]);
    }

    setIsLoading(false);
  };

  return (
    <div className="App">
      <h1>LLM Chat Application</h1>
      <div className={`api-status ${apiStatus}`}>
        API Status: {apiStatus === 'online' ? 'Connected' : 'Disconnected'}
      </div>
      <div className="chat-container">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            {message.content}
          </div>
        ))}
        {isLoading && <div className="message assistant">Thinking...</div>}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message here..."
        />
        <button type="submit" disabled={isLoading}>
          Send
        </button>
      </form>
    </div>
  );
}

export default App;