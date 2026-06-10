import React, { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';

const ChatInput = ({ onSendMessage, disabled }) => {
  const [input, setInput] = useState('');
  const textareaRef = useRef(null);

  // Auto-resize textarea
  useEffect(() => {
    const el = textareaRef.current;
    if (el) {
      el.style.height = 'auto';
      el.style.height = Math.min(el.scrollHeight, 160) + 'px';
    }
  }, [input]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="px-4 md:px-0 pt-2 pb-5">
      <div className="max-w-3xl mx-auto">
        <form 
          onSubmit={handleSubmit}
          className="glass-input rounded-2xl flex items-end gap-2 p-2"
        >
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            placeholder="Ask Aurora anything..."
            className="flex-1 bg-transparent border-none resize-none focus:outline-none focus:ring-0 text-textMain placeholder-textDim text-sm py-2.5 px-3 max-h-40 min-h-[40px]"
            rows={1}
          />
          <button
            type="submit"
            disabled={!input.trim() || disabled}
            className={`p-2.5 rounded-xl transition-all flex-shrink-0 ${
              input.trim() && !disabled
                ? 'aurora-gradient text-white shadow-lg shadow-accentPurple/20 hover:opacity-90'
                : 'bg-surfaceHover text-textDim cursor-not-allowed'
            }`}
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
        <div className="text-center mt-2.5">
          <span className="text-[11px] text-textDim">Aurora can make mistakes. Consider verifying important information.</span>
        </div>
      </div>
    </div>
  );
};

export default ChatInput;
