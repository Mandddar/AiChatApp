/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0a0a0f',
        surface: 'rgba(255,255,255,0.03)',
        surfaceHover: 'rgba(255,255,255,0.06)',
        surfaceSolid: '#131318',
        border: 'rgba(255,255,255,0.08)',
        borderLight: 'rgba(255,255,255,0.12)',
        textMain: '#e4e4e7',
        textMuted: '#71717a',
        textDim: '#52525b',
        accentPurple: '#8b5cf6',
        accentCyan: '#06b6d4',
        accentBlue: '#3b82f6',
        userBubble: 'rgba(139,92,246,0.12)',
        aiBubble: 'rgba(255,255,255,0.02)',
        inputBg: 'rgba(255,255,255,0.05)',
        danger: '#ef4444',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      animation: {
        'aurora': 'aurora 8s ease-in-out infinite',
        'slide-up': 'slideUp 0.3s ease-out',
        'fade-in': 'fadeIn 0.4s ease-out',
        'pulse-dot': 'pulseDot 1.4s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        aurora: {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(12px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        pulseDot: {
          '0%, 80%, 100%': { opacity: '0.3', transform: 'scale(0.8)' },
          '40%': { opacity: '1', transform: 'scale(1)' },
        },
        glow: {
          '0%': { boxShadow: '0 0 20px rgba(139,92,246,0.15)' },
          '100%': { boxShadow: '0 0 30px rgba(6,182,212,0.2)' },
        },
      },
    },
  },
  plugins: [],
}
