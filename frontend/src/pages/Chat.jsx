import React, { useState, useEffect } from 'react';
import Sidebar from '../components/chat/Sidebar';
import ChatWindow from '../components/chat/ChatWindow';
import { chatApi } from '../api/chatApi';

const Chat = () => {
  const [conversations, setConversations] = useState([]); // Array of { id, title, messages }
  const [activeConversationId, setActiveConversationId] = useState(null);
  const [isTyping, setIsTyping] = useState(false);

  // Fetch conversations on mount
  useEffect(() => {
    const loadChats = async () => {
      try {
        const chats = await chatApi.getChats();
        setConversations(chats);
        if (chats.length > 0) {
          handleSelectConversation(chats[0].id);
        }
      } catch (error) {
        console.error("Failed to load chats:", error);
      }
    };
    loadChats();
  }, []);

  const activeConversation = conversations.find(c => c.id === activeConversationId);
  const activeMessages = activeConversation?.messages || [];

  const handleNewChat = () => {
    setActiveConversationId(null);
  };

  const handleSelectConversation = async (id) => {
    setActiveConversationId(id);
    // Fetch details if we don't have messages yet
    const chat = conversations.find(c => c.id === id);
    if (chat && !chat.messages) {
      try {
        const detail = await chatApi.getChatDetail(id);
        setConversations(prev =>
          prev.map(c => (c.id === id ? { ...c, messages: detail.messages } : c))
        );
      } catch (error) {
        console.error("Failed to load chat details:", error);
      }
    }
  };

  const handleSendMessage = async (content) => {
    let chatId = activeConversationId;
    
    // Optimistically update UI with user message
    const optimisticUserMsg = { role: 'user', content };
    
    if (!chatId) {
      // Create new chat
      try {
        const title = content.slice(0, 40) + (content.length > 40 ? '...' : '');
        const newChat = await chatApi.createChat(title);
        chatId = newChat.id;
        setActiveConversationId(chatId);
        setConversations(prev => [{ ...newChat, messages: [optimisticUserMsg] }, ...prev]);
      } catch (error) {
        console.error("Failed to create chat:", error);
        return;
      }
    } else {
      setConversations(prev =>
        prev.map(c =>
          c.id === chatId
            ? { ...c, messages: [...(c.messages || []), optimisticUserMsg] }
            : c
        )
      );
    }

    setIsTyping(true);
    try {
      // Send message to backend
      const newMessages = await chatApi.sendMessage(chatId, content);
      // Replace optimistic message and append new AI message
      setConversations(prev =>
        prev.map(c => {
          if (c.id === chatId) {
            const oldMessages = c.messages || [];
            // Remove the last optimistic user message
            const filteredMessages = oldMessages.slice(0, -1);
            return { ...c, messages: [...filteredMessages, ...newMessages] };
          }
          return c;
        })
      );
    } catch (error) {
      console.error("Failed to send message:", error);
    } finally {
      setIsTyping(false);
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
        messages={activeMessages}
        isTyping={isTyping}
        onSendMessage={handleSendMessage}
      />
    </div>
  );
};

export default Chat;
