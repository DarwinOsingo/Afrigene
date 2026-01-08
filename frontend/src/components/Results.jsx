import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { ConfidenceInterval, HealthMarkerCard, ResearchDisclaimer } from './Common';

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899'];

export const AncestryChart = ({ populations }) => {
  if (!populations || populations.length === 0) {
    return <div className="p-4 text-gray-600">No ancestry data available</div>;
  }

  // Bar chart data
  const barData = populations.map((p) => ({
    name: p.population_group,
    percentage: p.percentage,
    ci_lower: p.confidence_interval.lower,
    ci_upper: p.confidence_interval.upper,
  }));

  // Pie chart data
  const pieData = populations.map((p) => ({
    name: p.population_group,
    value: p.percentage,
  }));

  return (
    <div className="space-y-6">
      <div>
        <h3 className="font-semibold text-gray-900 mb-4">Ancestry Composition (Bar Chart)</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={barData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis label={{ value: 'Percentage (%)', angle: -90, position: 'insideLeft' }} />
            <Tooltip formatter={(value) => `${value.toFixed(1)}%`} />
            <Bar dataKey="percentage" fill="#3B82F6" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div>
        <h3 className="font-semibold text-gray-900 mb-4">Ancestry Distribution (Pie Chart)</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={pieData}
              cx="50%"
              cy="50%"
              labelLine={true}
              label={({ name, value }) => `${name}: ${value.toFixed(1)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {pieData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip formatter={(value) => `${value.toFixed(1)}%`} />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <div>
        <h3 className="font-semibold text-gray-900 mb-4">Detailed Ancestry Estimates with Confidence Intervals</h3>
        <div className="space-y-4">
          {populations.map((pop) => (
            <div key={pop.population_group} className="bg-gray-50 p-4 rounded-lg border border-gray-200">
              <div className="flex justify-between items-start mb-2">
                <h4 className="font-medium text-gray-900">{pop.population_group}</h4>
                <div className="text-right text-sm">
                  <p className="text-gray-600">Sample Size (Reference): <span className="font-semibold">{pop.sample_size_reference.toLocaleString()}</span></p>
                  <p className="text-gray-600">Reference Dataset: <span className="font-mono text-xs">{pop.reference_dataset}</span></p>
                </div>
              </div>
              <ConfidenceInterval 
                lower={pop.confidence_interval.lower}
                upper={pop.confidence_interval.upper}
                percentage={pop.percentage}
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export const HealthMarkersSection = ({ markers }) => {
  if (!markers || markers.length === 0) {
    return <div className="p-4 text-gray-600">No health markers identified</div>;
  }

  return (
    <div className="space-y-4">
      <h3 className="font-semibold text-gray-900 mb-4">Health-Relevant Genetic Markers</h3>
      <ResearchDisclaimer />
      <div className="space-y-4">
        {markers.map((marker, idx) => (
          <HealthMarkerCard key={`${marker.gene}-${idx}`} marker={marker} />
        ))}
      </div>
    </div>
  );
};

export const ResultsVisualization = ({ results, loading = false }) => {
  if (loading) {
    return <div className="p-8 text-center text-gray-600">Processing results...</div>;
  }

  if (!results) {
    return <div className="p-8 text-center text-gray-600">No results available</div>;
  }

  return (
    <div className="space-y-8">
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-900">
          <span className="font-semibold">Results Status:</span> {results.sample_status}
        </p>
        <p className="text-xs text-blue-800 mt-1">
          Computed: {new Date(results.results_computed_at).toLocaleString()}
        </p>
      </div>

      <div className="bg-amber-50 border-l-4 border-amber-400 p-4 rounded">
        <p className="text-sm text-amber-900">
          <span className="font-semibold">⚠️ Disclaimer:</span> {results.disclaimer}
        </p>
      </div>

      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <AncestryChart populations={results.ancestry.primary_populations} />
        
        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="bg-gray-50 p-4 rounded text-sm text-gray-700">
            <p className="mb-2">
              <span className="font-semibold">Methodology:</span> {results.ancestry.methodology}
            </p>
            <p className="mb-2">
              <span className="font-semibold">Confidence Note:</span> {results.ancestry.confidence_note}
            </p>
            <p>
              <span className="font-semibold">Limitations:</span> {results.ancestry.limitations}
            </p>
          </div>
        </div>
      </div>

      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <HealthMarkersSection markers={results.health_markers} />
      </div>
    </div>
  );
};
