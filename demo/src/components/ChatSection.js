import React, { useState, useEffect, useRef } from 'react';

const ChatSection = ({ projectId, messages, setMessages, loading, setLoading, setError, setPresentationPlan }) => {
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);
  
  const API_BASE = 'http://localhost:8000/v1';
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  const sendMessage = async () => {
    if (!inputValue.trim() || !projectId || loading) return;
    
    const userMessage = inputValue.trim();
    setInputValue('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`${API_BASE}/projects/${projectId}/messages/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage
        })
      });
      
      if (!response.ok) {
        throw new Error('Failed to send message');
      }
      
      const result = await response.json();
      setMessages(prev => [...prev, { role: 'assistant', content: result.response }]);
      
      if (result.presentation_plan) {
        setPresentationPlan(result.presentation_plan);
      }
      
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };
  
  return (
    <div className="h-full flex flex-col bg-dark-tertiary border border-border rounded-lg min-h-0 max-h-full">
      <div className="p-4 border-b border-border">
        <h3 className="font-medium text-text-primary">Chat with AI Assistant</h3>
      </div>
      
      <div className="flex-1 p-5 overflow-y-auto flex flex-col gap-4">
        {messages.map((message, index) => {
          // Handle both API format (type: 'user'/'ai') and local format (role: 'user'/'assistant')
          const isUser = message.type === 'user' || message.role === 'user';
          
          return (
            <div
              key={index}
              className={`max-w-[80%] p-3 rounded-xl break-words ${
                isUser
                  ? 'bg-blue-600 text-white ml-auto'
                  : 'bg-border text-text-primary mr-auto'
              }`}
            >
              {message.content}
            </div>
          );
        })}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="p-5 border-t border-border">
        <div className="flex gap-3 w-full">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message..."
            disabled={!projectId || loading}
            className="flex-1 min-w-0 bg-border text-text-primary px-4 py-3 rounded-md focus:outline-none focus:ring-2 focus:ring-primary placeholder-text-secondary"
          />
          <button
            onClick={sendMessage}
            disabled={!projectId || loading || !inputValue.trim()}
            className="flex-shrink-0 bg-primary text-white px-5 py-3 rounded-md hover:bg-primary-hover disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatSection;