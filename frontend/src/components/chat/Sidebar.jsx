import React, { useContext } from 'react';
import { AuthContext } from '../../context/AuthContext';
import { Plus, MessageSquare, LogOut, Sparkles, FileText, Trash2 } from 'lucide-react';

const Sidebar = ({ onNewChat, conversations, activeConversationId, onSelectConversation, documents = [], onDeleteDocument }) => {
  const { user, logout } = useContext(AuthContext);

  return (
    <div className="hidden md:flex flex-col w-72 glass border-r border-border h-screen">
      {/* Logo & Brand */}
      <div className="p-4 flex-shrink-0">
        <div className="flex items-center gap-3 px-2 mb-4">
          <div className="w-8 h-8 rounded-lg aurora-gradient flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-white" />
          </div>
          <span className="text-base font-semibold aurora-gradient-text">Aurora AI</span>
        </div>
        <button 
          onClick={onNewChat}
          className="w-full flex items-center gap-3 px-4 py-2.5 rounded-xl border border-border hover:border-borderLight hover:bg-surfaceHover transition-all text-sm font-medium text-textMain group"
        >
          <Plus className="w-4 h-4 text-textMuted group-hover:text-accentPurple transition-colors" />
          New chat
        </button>
      </div>

      {/* Chat History */}
      <div className="flex-1 overflow-y-auto px-3 pb-3">
        {conversations.length > 0 && (
          <>
            <div className="text-[10px] font-semibold text-textDim uppercase tracking-widest mt-2 mb-2 px-3">
              Conversations
            </div>
            <div className="space-y-0.5">
              {conversations.map((conv) => (
                <button
                  key={conv.id}
                  onClick={() => onSelectConversation(conv.id)}
                  className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all text-sm truncate text-left group ${
                    conv.id === activeConversationId
                      ? 'bg-surfaceHover text-textMain border border-border'
                      : 'text-textMuted hover:text-textMain hover:bg-surfaceHover border border-transparent'
                  }`}
                >
                  <MessageSquare className={`w-3.5 h-3.5 flex-shrink-0 transition-colors ${
                    conv.id === activeConversationId ? 'text-accentPurple' : 'text-textDim group-hover:text-textMuted'
                  }`} />
                  <span className="truncate">{conv.title}</span>
                </button>
              ))}
            </div>
          </>
        )}

        {/* Documents Section */}
        {documents.length > 0 && (
          <>
            <div className="text-[10px] font-semibold text-textDim uppercase tracking-widest mt-5 mb-2 px-3">
              Knowledge Base
            </div>
            <div className="space-y-0.5">
              {documents.map((doc) => (
                <div
                  key={doc.id}
                  className="flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-textMuted hover:bg-surfaceHover transition-all group"
                >
                  <FileText className={`w-3.5 h-3.5 flex-shrink-0 ${
                    doc.status === 'ready' ? 'text-green-400' : doc.status === 'processing' ? 'text-yellow-400' : 'text-red-400'
                  }`} />
                  <span className="truncate flex-1 text-xs">{doc.original_name}</span>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onDeleteDocument(doc.id);
                    }}
                    className="opacity-0 group-hover:opacity-100 text-textDim hover:text-danger p-0.5 rounded transition-all"
                    title="Remove document"
                  >
                    <Trash2 className="w-3 h-3" />
                  </button>
                </div>
              ))}
            </div>
          </>
        )}
      </div>

      {/* User section */}
      <div className="p-3 border-t border-border flex-shrink-0">
        <div className="flex items-center gap-3 px-3 py-2">
          <div className="w-8 h-8 rounded-full bg-surfaceHover border border-border flex items-center justify-center flex-shrink-0">
            <span className="text-xs font-semibold text-textMuted uppercase">
              {user?.username?.charAt(0) || '?'}
            </span>
          </div>
          <span className="text-sm font-medium text-textMain truncate flex-1">{user?.username}</span>
          <button 
            onClick={logout}
            className="text-textDim hover:text-danger p-1.5 rounded-lg hover:bg-surfaceHover transition-all"
            title="Log out"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
