import React, { useState, useRef, useEffect } from 'react';
import MessageBubble, { TypingIndicator } from './MessageBubble';
import ChatInput from './ChatInput';
import EmptyChatState from './EmptyChatState';
import { Menu, Sparkles } from 'lucide-react';

const ChatWindow = ({ initialMessages = [], onMessagesUpdate }) => {
  const [messages, setMessages] = useState(initialMessages);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  useEffect(() => {
    if (messages.length > 0) {
      onMessagesUpdate(messages);
    }
  }, [messages]);

  const handleSendMessage = (content) => {
    const userMessage = { role: 'user', content };
    setMessages(prev => [...prev, userMessage]);
    
    setIsTyping(true);
    setTimeout(() => {
      const aiMessage = { 
        role: 'assistant', 
        content: `I received your message: "${content}". This is a dummy response since the AI endpoint is not yet connected.`
      };
      setMessages(prev => [...prev, aiMessage]);
      setIsTyping(false);
    }, 1200);
  };

  return (
    <div className="flex-1 flex flex-col h-screen bg-background relative">
      {/* Subtle ambient glow behind chat area */}
      <div className="absolute top-[10%] left-[50%] -translate-x-1/2 w-[600px] h-[300px] bg-accentPurple/[0.02] blur-[100px] rounded-full pointer-events-none" />

      {/* Mobile Header */}
      <div className="md:hidden flex items-center gap-3 p-4 border-b border-border">
        <button className="text-textMuted hover:text-textMain p-1">
          <Menu className="w-5 h-5" />
        </button>
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded-lg aurora-gradient flex items-center justify-center">
            <Sparkles className="w-3 h-3 text-white" />
          </div>
          <span className="text-sm font-semibold text-textMain">Aurora</span>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto relative">
        {messages.length === 0 ? (
          <EmptyChatState onSuggestionClick={handleSendMessage} />
        ) : (
          <div className="max-w-3xl mx-auto py-6">
            {messages.map((msg, idx) => (
              <MessageBubble key={idx} message={msg} />
            ))}
            {isTyping && <TypingIndicator />}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input */}
      <div className="flex-shrink-0 relative">
        <div className="absolute bottom-full left-0 right-0 h-12 bg-gradient-to-t from-background to-transparent pointer-events-none" />
        <ChatInput onSendMessage={handleSendMessage} disabled={isTyping} />
      </div>
    </div>
  );
};

export default ChatWindow;
