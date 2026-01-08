import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ResultsVisualization } from '../components/Results';
import { AuditLog, ResearchDisclaimer, ConsentBanner } from '../components/Common';

export const DashboardPage = () => {
  const { user, api } = useAuth();
  const [samples, setSamples] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedStatus, setSelectedStatus] = useState(null);

  useEffect(() => {
    const fetchSamples = async () => {
      try {
        const params = selectedStatus ? { status: selectedStatus } : {};
        const response = await api.get('/samples', { params });
        setSamples(response.data.samples);
      } catch (err) {
        console.error('Failed to load samples', err);
      } finally {
        setLoading(false);
      }
    };

    fetchSamples();
  }, [api, selectedStatus]);

  const statusCounts = {
    'Received': samples.filter(s => s.status === 'Received').length,
    'Processing': samples.filter(s => s.status === 'Processing').length,
    'Results Available': samples.filter(s => s.status === 'Results Available').length,
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Lab Dashboard</h1>
        <p className="text-gray-600 mt-1">Welcome, {user?.email}</p>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <div className="text-3xl font-bold text-blue-600">{samples.length}</div>
          <div className="text-gray-700 font-medium mt-1">Total Samples</div>
        </div>

        <div className="bg-green-50 border border-green-200 rounded-lg p-6">
          <div className="text-3xl font-bold text-green-600">{statusCounts['Results Available']}</div>
          <div className="text-gray-700 font-medium mt-1">Results Available</div>
        </div>

        <div className="bg-amber-50 border border-amber-200 rounded-lg p-6">
          <div className="text-3xl font-bold text-amber-600">{statusCounts['Processing']}</div>
          <div className="text-gray-700 font-medium mt-1">Processing</div>
        </div>
      </div>

      {/* Samples Table */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Samples</h2>

        <div className="mb-4 flex gap-2">
          <button
            onClick={() => setSelectedStatus(null)}
            className={`px-4 py-2 rounded font-medium ${
              selectedStatus === null
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            All
          </button>
          {['Received', 'Processing', 'Results Available', 'Archived'].map((status) => (
            <button
              key={status}
              onClick={() => setSelectedStatus(status)}
              className={`px-4 py-2 rounded font-medium ${
                selectedStatus === status
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {status}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="p-8 text-center text-gray-600">Loading samples...</div>
        ) : samples.length === 0 ? (
          <div className="p-8 text-center text-gray-600">No samples found</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b-2 border-gray-300 bg-gray-50">
                  <th className="text-left p-3 font-semibold text-gray-700">Sample ID</th>
                  <th className="text-left p-3 font-semibold text-gray-700">Status</th>
                  <th className="text-left p-3 font-semibold text-gray-700">Uploaded</th>
                  <th className="text-left p-3 font-semibold text-gray-700">Actions</th>
                </tr>
              </thead>
              <tbody>
                {samples.map((sample) => (
                  <tr key={sample.id} className="border-b border-gray-200 hover:bg-gray-50">
                    <td className="p-3 font-mono text-sm text-gray-900">{sample.sample_id}</td>
                    <td className="p-3">
                      <span
                        className={`px-3 py-1 rounded text-sm font-medium ${
                          sample.status === 'Results Available'
                            ? 'bg-green-100 text-green-800'
                            : sample.status === 'Processing'
                            ? 'bg-amber-100 text-amber-800'
                            : 'bg-blue-100 text-blue-800'
                        }`}
                      >
                        {sample.status}
                      </span>
                    </td>
                    <td className="p-3 text-sm text-gray-600">
                      {new Date(sample.uploaded_at).toLocaleDateString()}
                    </td>
                    <td className="p-3">
                      <SampleResultLink sampleId={sample.id} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

const SampleResultLink = ({ sampleId }) => {
  const navigate = useNavigate();
  return (
    <button
      onClick={() => navigate(`/lab/samples/${sampleId}`)}
      className="text-blue-600 hover:underline font-medium text-sm"
    >
      View Results
    </button>
  );
};

export const SampleDetailPage = () => {
  const { sampleId } = useParams();
  const { api } = useAuth();
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [auditLogs, setAuditLogs] = useState([]);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const response = await api.get(`/samples/${sampleId}/results`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
        });
        setResults(response.data);
      } catch (err) {
        setError('Failed to load results');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
  }, [api, sampleId]);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Sample Results</h1>
        <p className="text-gray-600 mt-1">Sample ID: <code className="bg-gray-100 px-2 py-1 rounded font-mono">{sampleId}</code></p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded p-4 text-red-800">
          {error}
        </div>
      )}

      <ConsentBanner />
      <ResearchDisclaimer />

      <ResultsVisualization results={results} loading={loading} />

      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Data Access Audit Trail</h2>
        <p className="text-sm text-gray-600 mb-4">Complete audit log of who accessed this sample and when</p>
        <AuditLog entries={auditLogs} />
      </div>
    </div>
  );
};
