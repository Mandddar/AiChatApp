import React, { useState, useRef, useEffect } from 'react';
import { Send, Paperclip, X, FileText, Loader2 } from 'lucide-react';

const ChatInput = ({ onSendMessage, onUploadDocument, disabled, uploadingDoc }) => {
  const [input, setInput] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const textareaRef = useRef(null);
  const fileInputRef = useRef(null);

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

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
    } else if (file) {
      alert('Only PDF files are supported');
    }
    // Reset file input
    e.target.value = '';
  };

  const handleFileUpload = async () => {
    if (selectedFile && onUploadDocument) {
      await onUploadDocument(selectedFile);
      setSelectedFile(null);
    }
  };

  const handleCancelFile = () => {
    setSelectedFile(null);
  };

  return (
    <div className="px-4 md:px-0 pt-2 pb-5">
      <div className="max-w-3xl mx-auto">
        {/* Selected file preview */}
        {selectedFile && (
          <div className="mb-2 flex items-center gap-2 p-2.5 rounded-xl glass-input animate-slide-up">
            <FileText className="w-4 h-4 text-accentPurple flex-shrink-0" />
            <span className="text-sm text-textMain truncate flex-1">{selectedFile.name}</span>
            <span className="text-xs text-textDim">{(selectedFile.size / 1024).toFixed(0)} KB</span>
            {uploadingDoc ? (
              <Loader2 className="w-4 h-4 text-accentPurple animate-spin flex-shrink-0" />
            ) : (
              <>
                <button
                  onClick={handleFileUpload}
                  className="text-xs px-3 py-1 rounded-lg aurora-gradient text-white hover:opacity-90 transition-opacity"
                >
                  Upload
                </button>
                <button
                  onClick={handleCancelFile}
                  className="text-textDim hover:text-textMain p-0.5 rounded transition-colors"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              </>
            )}
          </div>
        )}

        <form 
          onSubmit={handleSubmit}
          className="glass-input rounded-2xl flex items-end gap-2 p-2"
        >
          {/* Hidden file input */}
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            onChange={handleFileSelect}
            className="hidden"
          />

          {/* Paperclip button */}
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={disabled || uploadingDoc}
            className="p-2.5 rounded-xl text-textDim hover:text-accentPurple hover:bg-surfaceHover transition-all flex-shrink-0 disabled:opacity-40"
            title="Upload PDF"
          >
            <Paperclip className="w-4 h-4" />
          </button>

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
