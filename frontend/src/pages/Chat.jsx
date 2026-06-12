import React, { useState, useEffect } from 'react';
import Sidebar from '../components/chat/Sidebar';
import ChatWindow from '../components/chat/ChatWindow';
import { chatApi } from '../api/chatApi';

const Chat = () => {
  const [conversations, setConversations] = useState([]); // Array of { id, title, messages }
  const [activeConversationId, setActiveConversationId] = useState(null);
  const [isTyping, setIsTyping] = useState(false);
  const [documents, setDocuments] = useState([]);
  const [uploadingDoc, setUploadingDoc] = useState(false);

  // Fetch conversations and documents on mount
  useEffect(() => {
    const loadData = async () => {
      try {
        const [chats, docs] = await Promise.all([
          chatApi.getChats(),
          chatApi.getDocuments(),
        ]);
        setConversations(chats);
        setDocuments(docs);
        if (chats.length > 0) {
          handleSelectConversation(chats[0].id);
        }
      } catch (error) {
        console.error("Failed to load data:", error);
      }
    };
    loadData();
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

  const handleUploadDocument = async (file) => {
    setUploadingDoc(true);
    try {
      const doc = await chatApi.uploadDocument(file);
      setDocuments(prev => [doc, ...prev]);
    } catch (error) {
      console.error("Failed to upload document:", error);
      alert("Failed to upload document. Please try again.");
    } finally {
      setUploadingDoc(false);
    }
  };

  const handleDeleteDocument = async (docId) => {
    try {
      await chatApi.deleteDocument(docId);
      setDocuments(prev => prev.filter(d => d.id !== docId));
    } catch (error) {
      console.error("Failed to delete document:", error);
    }
  };

  return (
    <div className="flex h-screen bg-background font-sans text-textMain overflow-hidden">
      <Sidebar
        onNewChat={handleNewChat}
        conversations={conversations}
        activeConversationId={activeConversationId}
        onSelectConversation={handleSelectConversation}
        documents={documents}
        onDeleteDocument={handleDeleteDocument}
      />
      <ChatWindow
        key={activeConversationId || 'new'}
        messages={activeMessages}
        isTyping={isTyping}
        onSendMessage={handleSendMessage}
        onUploadDocument={handleUploadDocument}
        uploadingDoc={uploadingDoc}
      />
    </div>
  );
};

export default Chat;
