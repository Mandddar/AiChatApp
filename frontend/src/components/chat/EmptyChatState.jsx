import React from 'react';
import { Sparkles } from 'lucide-react';

const EmptyChatState = ({ onSuggestionClick }) => {
  return (
    <div className="flex flex-col items-center justify-center h-full max-w-2xl mx-auto px-6 animate-fade-in">
      {/* Animated logo */}
      <div className="relative mb-8">
        <div className="w-16 h-16 rounded-2xl aurora-gradient flex items-center justify-center animate-glow">
          <Sparkles className="w-8 h-8 text-white" />
        </div>
        <div className="absolute inset-0 w-16 h-16 rounded-2xl aurora-gradient opacity-20 blur-xl" />
      </div>

      <h2 className="text-2xl font-semibold text-textMain mb-2">What can I help with?</h2>
      <p className="text-textMuted text-sm mb-10 text-center max-w-md">
        Start a conversation by typing a message below.
      </p>
    </div>
  );
};

export default EmptyChatState;
