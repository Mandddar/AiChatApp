import React, { useState } from 'react';
import Sidebar from '../components/chat/Sidebar';
import ChatWindow from '../components/chat/ChatWindow';

const Chat = () => {
  const [conversations, setConversations] = useState([]); // Array of { id, title, messages }
  const [activeConversationId, setActiveConversationId] = useState(null);

  const activeConversation = conversations.find(c => c.id === activeConversationId);
  const activeMessages = activeConversation?.messages || [];

  const handleNewChat = () => {
    setActiveConversationId(null);
  };

  const handleSelectConversation = (id) => {
    setActiveConversationId(id);
  };

  const handleMessagesUpdate = (newMessages) => {
    if (newMessages.length === 0) return;

    if (activeConversationId) {
      // Update existing conversation
      setConversations(prev =>
        prev.map(c =>
          c.id === activeConversationId
            ? { ...c, messages: newMessages }
            : c
        )
      );
    } else {
      // Create a new conversation from the first user message
      const firstUserMsg = newMessages.find(m => m.role === 'user');
      const title = firstUserMsg
        ? firstUserMsg.content.slice(0, 40) + (firstUserMsg.content.length > 40 ? '...' : '')
        : 'New Chat';
      const newId = Date.now();
      setConversations(prev => [{ id: newId, title, messages: newMessages }, ...prev]);
      setActiveConversationId(newId);
    }
  };

  return (
    <div className="flex h-screen bg-background font-sans text-textMain overflow-hidden">
      <Sidebar
        onNewChat={handleNewChat}
        conversations={conversations}
        activeConversationId={activeConversationId}
        onSelectConversation={handleSelectConversation}
      />
      <ChatWindow
        key={activeConversationId || 'new'}
        initialMessages={activeMessages}
        onMessagesUpdate={handleMessagesUpdate}
      />
    </div>
  );
};

export default Chat;
