import api from './axios';

export const chatApi = {
  // Fetch all chats for the current user
  getChats: async () => {
    const response = await api.get('/chats/');
    return response.data;
  },

  // Fetch a specific chat along with its messages
  getChatDetail: async (chatId) => {
    const response = await api.get(`/chats/${chatId}`);
    return response.data;
  },

  // Create a new chat
  createChat: async (title = "New Chat") => {
    const response = await api.post('/chats/', { title });
    return response.data;
  },

  // Send a message and get the AI response back
  sendMessage: async (chatId, content) => {
    const response = await api.post(`/chats/${chatId}/messages`, { content });
    return response.data; // Returns a list of [userMessage, aiMessage]
  },

  // Upload a PDF document for RAG
  uploadDocument: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  // List all uploaded documents
  getDocuments: async () => {
    const response = await api.get('/documents/');
    return response.data;
  },

  // Delete a document
  deleteDocument: async (documentId) => {
    await api.delete(`/documents/${documentId}`);
  },
};
