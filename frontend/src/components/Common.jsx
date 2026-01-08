import React from 'react';
import { useAuth } from '../context/AuthContext';

export const ConfidenceInterval = ({ lower, upper, percentage }) => {
  const width = Math.max(upper - lower, 10);
  const marginLeft = lower;
  
  return (
    <div className="mt-2">
      <div className="flex justify-between text-sm text-gray-600 mb-1">
        <span>{lower.toFixed(0)}%</span>
        <span className="font-semibold text-gray-900">{percentage.toFixed(1)}%</span>
        <span>{upper.toFixed(0)}%</span>
      </div>
      <div className="w-full h-6 bg-gray-100 rounded relative border border-gray-300">
        <div
          className="absolute h-full bg-blue-500 rounded"
          style={{
            left: `${marginLeft}%`,
            width: `${width}%`,
          }}
        />
        <div
          className="absolute top-1/2 -translate-y-1/2 w-2 h-8 border-l-2 border-blue-700"
          style={{ left: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

export const HealthMarkerCard = ({ marker }) => {
  const getSeverityColor = (significance) => {
    if (!significance) return 'bg-gray-50';
    if (significance.toLowerCase().includes('disease')) return 'bg-red-50 border-red-200';
    if (significance.toLowerCase().includes('carrier') || significance.toLowerCase().includes('trait')) 
      return 'bg-amber-50 border-amber-200';
    return 'bg-blue-50 border-blue-200';
  };

  return (
    <div className={`border rounded-lg p-4 mb-4 ${getSeverityColor(marker.clinical_significance)}`}>
      <div className="flex justify-between items-start mb-3">
        <div>
          <h4 className="font-semibold text-gray-900">{marker.gene}</h4>
          <p className="text-sm text-gray-600">{marker.variant}</p>
        </div>
        <div className="text-right">
          <p className="font-mono text-sm bg-gray-200 px-2 py-1 rounded">
            {marker.genotype}
          </p>
        </div>
      </div>

      <p className="text-sm mb-2">
        <span className="font-medium">Phenotype:</span> {marker.phenotype}
      </p>

      {marker.clinical_significance && (
        <p className="text-sm mb-2 text-gray-700">
          {marker.clinical_significance}
        </p>
      )}

      {marker.population_frequency && (
        <div className="mt-3 pt-3 border-t border-gray-300">
          <p className="text-xs font-medium text-gray-600 mb-2">Population Frequencies:</p>
          <div className="grid grid-cols-2 gap-2">
            {Object.entries(marker.population_frequency).map(([pop, freq]) => (
              <div key={pop} className="text-xs">
                <span className="text-gray-600">{pop}:</span>
                <span className="font-medium text-gray-900 ml-1">{(parseFloat(freq) * 100).toFixed(1)}%</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="mt-3 pt-3 border-t border-gray-300">
        <p className="text-xs text-gray-600 italic">{marker.disclaimer}</p>
      </div>
    </div>
  );
};

export const ResearchDisclaimer = () => (
  <div className="bg-amber-50 border-l-4 border-amber-400 p-4 rounded mb-4">
    <h3 className="font-semibold text-amber-900 mb-2">Research Use Only</h3>
    <p className="text-sm text-amber-800">
      These results are provided for research and educational purposes only. 
      They are not diagnostic. For any health concerns, consult a qualified medical professional 
      or genetic counselor.
    </p>
  </div>
);

export const ConsentBanner = () => (
  <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
    <p className="text-sm text-blue-900">
      <span className="font-semibold">Consent Status:</span> Active (Data retained per consent agreement)
    </p>
  </div>
);

export const AuditLog = ({ entries, loading = false }) => {
  if (loading) {
    return <div className="p-4 text-center text-gray-600">Loading audit logs...</div>;
  }

  if (!entries || entries.length === 0) {
    return <div className="p-4 text-center text-gray-500">No access logs</div>;
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-gray-300 bg-gray-50">
            <th className="text-left p-2 font-semibold text-gray-700">Timestamp</th>
            <th className="text-left p-2 font-semibold text-gray-700">User</th>
            <th className="text-left p-2 font-semibold text-gray-700">Action</th>
            <th className="text-left p-2 font-semibold text-gray-700">Resource</th>
            <th className="text-left p-2 font-semibold text-gray-700">IP Address</th>
          </tr>
        </thead>
        <tbody>
          {entries.map((log) => (
            <tr key={log.id} className="border-b border-gray-200 hover:bg-gray-50">
              <td className="p-2 text-gray-600">
                {new Date(log.timestamp).toLocaleString()}
              </td>
              <td className="p-2 text-gray-700">{log.user_email}</td>
              <td className="p-2">
                <span className="px-2 py-1 bg-gray-100 rounded text-gray-700 font-mono text-xs">
                  {log.action}
                </span>
              </td>
              <td className="p-2 text-gray-600 font-mono text-xs">{log.resource_accessed || '-'}</td>
              <td className="p-2 text-gray-600 text-xs">{log.ip_address || '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
