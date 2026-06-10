import React, { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { Loader2, Sparkles } from 'lucide-react';

const Register = () => {
  const [formData, setFormData] = useState({ email: '', username: '', password: '' });
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { register } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData(prev => ({ ...prev, [id]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      await register(formData);
      navigate('/login');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to register. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4 relative overflow-hidden">
      {/* Background aurora glow */}
      <div className="absolute top-[-40%] right-[-15%] w-[500px] h-[500px] rounded-full bg-accentCyan/5 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-40%] left-[-15%] w-[600px] h-[600px] rounded-full bg-accentPurple/5 blur-[120px] pointer-events-none" />

      <div className="w-full max-w-sm relative z-10 animate-fade-in">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl aurora-gradient mb-4">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-textMain tracking-tight">Create account</h1>
          <p className="text-textMuted text-sm mt-1">Start your journey with Aurora</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="p-3 bg-danger/10 text-danger border border-danger/20 rounded-xl text-sm text-center animate-slide-up">
              {error}
            </div>
          )}

          <div>
            <label className="block text-xs font-medium text-textMuted mb-2 uppercase tracking-wider" htmlFor="email">
              Email
            </label>
            <input
              id="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              className="block w-full px-4 py-3 rounded-xl glass-input text-textMain placeholder-textDim focus:outline-none text-sm"
              placeholder="you@example.com"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-textMuted mb-2 uppercase tracking-wider" htmlFor="username">
              Username
            </label>
            <input
              id="username"
              type="text"
              value={formData.username}
              onChange={handleChange}
              className="block w-full px-4 py-3 rounded-xl glass-input text-textMain placeholder-textDim focus:outline-none text-sm"
              placeholder="Choose a username"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-textMuted mb-2 uppercase tracking-wider" htmlFor="password">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              className="block w-full px-4 py-3 rounded-xl glass-input text-textMain placeholder-textDim focus:outline-none text-sm"
              placeholder="Min. 8 characters"
              required
            />
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full flex justify-center items-center py-3 px-4 rounded-xl text-sm font-semibold text-white aurora-gradient transition-all hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed mt-6 shadow-lg shadow-accentPurple/20"
          >
            {isSubmitting ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Create Account'}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-textMuted">
          Already have an account?{' '}
          <Link to="/login" className="font-medium aurora-gradient-text hover:opacity-80 transition-opacity">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
