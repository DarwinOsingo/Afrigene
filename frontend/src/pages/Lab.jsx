import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const LoginPage = () => {
  const [email, setEmail] = useState('jane.kimani@knh.org');
  const [password, setPassword] = useState('demo_password_123');
  const [mfaCode, setMfaCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await login(email, password, mfaCode);
      navigate('/lab/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const demoAccounts = [
    { email: 'jane.kimani@knh.org', role: 'Lab Admin', institution: 'Kenyatta National Hospital' },
    { email: 'david.kipchoge@knh.org', role: 'Researcher', institution: 'Kenyatta National Hospital' },
    { email: 'oluwaseun.adeyemi@unilag.edu.ng', role: 'Researcher', institution: 'University of Lagos' },
  ];

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">AFRO-GENOMICS</h1>
          <p className="text-gray-600 mb-8">Lab Access Portal</p>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded p-4 mb-6 text-sm text-red-800">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4 mb-8">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                MFA Code (optional)
              </label>
              <input
                type="text"
                value={mfaCode}
                onChange={(e) => setMfaCode(e.target.value)}
                placeholder="6-digit code"
                className="w-full px-4 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white font-semibold py-2 rounded hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <div className="border-t pt-6">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">Demo Accounts</h3>
            <div className="space-y-2">
              {demoAccounts.map((account) => (
                <button
                  key={account.email}
                  type="button"
                  onClick={() => {
                    setEmail(account.email);
                    setPassword('demo_password_123');
                  }}
                  className="w-full text-left text-sm p-3 bg-gray-50 hover:bg-gray-100 rounded border border-gray-200"
                >
                  <div className="font-medium text-gray-900">{account.email}</div>
                  <div className="text-xs text-gray-600">{account.role} • {account.institution}</div>
                </button>
              ))}
            </div>
            <p className="text-xs text-gray-500 mt-3">
              Password for all demo accounts: <code className="bg-gray-100 px-1">demo_password_123</code>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
