import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link, Outlet } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';

// Pages
import { HomePage, ScienceMethodology, ResearchEthics } from './pages/Public';
import { LoginPage } from './pages/Lab';
import { DashboardPage, SampleDetailPage } from './pages/Dashboard';

// Layout Components
const PublicLayout = () => (
  <div className="min-h-screen bg-white">
    <nav className="bg-gray-900 text-white shadow-lg">
      <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold">AFRO-GENOMICS</Link>
        <div className="flex gap-6 items-center">
          <Link to="/science" className="hover:text-blue-400">Science</Link>
          <Link to="/research-ethics" className="hover:text-blue-400">Ethics</Link>
          <Link to="/lab/login" className="bg-blue-600 px-4 py-2 rounded hover:bg-blue-700">Lab Portal</Link>
        </div>
      </div>
    </nav>
    <main className="max-w-6xl mx-auto px-6 py-12">
      <Outlet />
    </main>
  </div>
);

const ProtectedLayout = () => {
  const { user, logout } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-blue-600 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 hover:bg-blue-700 rounded"
            >
              ☰
            </button>
            <Link to="/lab/dashboard" className="text-xl font-bold">AFRO-GENOMICS</Link>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm">{user?.email}</span>
            <span className="text-xs bg-blue-700 px-2 py-1 rounded">{user?.role}</span>
            <button
              onClick={logout}
              className="bg-red-600 px-4 py-2 rounded hover:bg-red-700"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      <div className="flex gap-0">
        {sidebarOpen && (
          <div className="w-64 bg-gray-900 text-white p-6">
            <div className="space-y-4">
              <Link
                to="/lab/dashboard"
                className="block p-3 hover:bg-gray-700 rounded font-medium"
              >
                Dashboard
              </Link>
              <Link
                to="/lab/samples"
                className="block p-3 hover:bg-gray-700 rounded font-medium"
              >
                Samples
              </Link>
              <Link
                to="/lab/consent"
                className="block p-3 hover:bg-gray-700 rounded font-medium"
              >
                Consent
              </Link>
              <Link
                to="/lab/settings"
                className="block p-3 hover:bg-gray-700 rounded font-medium"
              >
                Settings
              </Link>
              {user?.role === 'Lab Admin' && (
                <Link
                  to="/lab/audit"
                  className="block p-3 hover:bg-gray-700 rounded font-medium border-t border-gray-700 mt-4 pt-4"
                >
                  Audit Logs
                </Link>
              )}
            </div>
          </div>
        )}

        <main className="flex-1 p-8 max-w-6xl mx-auto w-full">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

const ProtectedRoute = () => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <ProtectedLayout /> : <Navigate to="/lab/login" />;
};

// Stub pages for navigation
const PlaceholderPage = ({ title }) => (
  <div className="bg-white rounded-lg border border-gray-200 p-6">
    <h1 className="text-3xl font-bold text-gray-900">{title}</h1>
    <p className="text-gray-600 mt-4">This page is a placeholder for the demo.</p>
  </div>
);

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route element={<PublicLayout />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/science" element={<ScienceMethodology />} />
            <Route path="/research-ethics" element={<ResearchEthics />} />
            <Route path="/lab-partnerships" element={<PlaceholderPage title="Lab Partnerships" />} />
            <Route path="/pricing" element={<PlaceholderPage title="Pricing" />} />
            <Route path="/populations" element={<PlaceholderPage title="African Populations" />} />
          </Route>

          {/* Lab Routes */}
          <Route path="/lab/login" element={<LoginPage />} />

          <Route element={<ProtectedRoute />}>
            <Route path="/lab/dashboard" element={<DashboardPage />} />
            <Route path="/lab/samples/:sampleId" element={<SampleDetailPage />} />
            <Route path="/lab/samples" element={<PlaceholderPage title="Samples" />} />
            <Route path="/lab/consent" element={<PlaceholderPage title="Consent Management" />} />
            <Route path="/lab/settings" element={<PlaceholderPage title="Settings" />} />
            <Route path="/lab/audit" element={<PlaceholderPage title="Audit Logs" />} />
          </Route>

          {/* Catch all */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
