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
    return response.data; // Now returns a list of [userMessage, aiMessage]
  }
};
