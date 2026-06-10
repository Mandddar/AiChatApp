import React from 'react';
import { Sparkles, User } from 'lucide-react';

const MessageBubble = ({ message }) => {
  const isUser = message.role === 'user';

  if (isUser) {
    return (
      <div className="flex justify-end px-4 md:px-6 py-3 animate-slide-up">
        <div className="max-w-[75%] flex items-end gap-3">
          <div className="px-4 py-3 rounded-2xl rounded-br-md bg-userBubble border border-accentPurple/10 text-textMain text-sm leading-relaxed">
            {message.content}
          </div>
          <div className="w-7 h-7 rounded-full bg-accentPurple/20 border border-accentPurple/30 flex items-center justify-center flex-shrink-0">
            <User className="w-3.5 h-3.5 text-accentPurple" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex px-4 md:px-6 py-3 animate-slide-up">
      <div className="max-w-[85%] flex items-start gap-3">
        <div className="w-7 h-7 rounded-full aurora-gradient flex items-center justify-center flex-shrink-0 mt-0.5">
          <Sparkles className="w-3.5 h-3.5 text-white" />
        </div>
        <div className="accent-bar pl-4">
          <div className="text-xs font-semibold aurora-gradient-text mb-1.5">Aurora</div>
          <div className="text-textMain text-sm leading-relaxed whitespace-pre-wrap">
            {message.content}
          </div>
        </div>
      </div>
    </div>
  );
};

// Typing indicator with animated dots
export const TypingIndicator = () => (
  <div className="flex px-4 md:px-6 py-3 animate-fade-in">
    <div className="flex items-start gap-3">
      <div className="w-7 h-7 rounded-full aurora-gradient flex items-center justify-center flex-shrink-0 mt-0.5">
        <Sparkles className="w-3.5 h-3.5 text-white" />
      </div>
      <div className="accent-bar pl-4">
        <div className="text-xs font-semibold aurora-gradient-text mb-2">Aurora</div>
        <div className="flex gap-1.5 items-center py-1">
          <span className="w-2 h-2 rounded-full bg-accentPurple/60 animate-pulse-dot" style={{ animationDelay: '0s' }} />
          <span className="w-2 h-2 rounded-full bg-accentBlue/60 animate-pulse-dot" style={{ animationDelay: '0.2s' }} />
          <span className="w-2 h-2 rounded-full bg-accentCyan/60 animate-pulse-dot" style={{ animationDelay: '0.4s' }} />
        </div>
      </div>
    </div>
  </div>
);

export default MessageBubble;
