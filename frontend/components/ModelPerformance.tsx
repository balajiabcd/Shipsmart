'use client'

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const performanceData = [
  { date: '2024-01', accuracy: 0.85, f1: 0.82, precision: 0.84, recall: 0.80 },
  { date: '2024-02', accuracy: 0.87, f1: 0.85, precision: 0.86, recall: 0.84 },
  { date: '2024-03', accuracy: 0.89, f1: 0.87, precision: 0.88, recall: 0.86 },
  { date: '2024-04', accuracy: 0.91, f1: 0.89, precision: 0.90, recall: 0.88 },
]

export function ModelPerformance() {
  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <h3 className="text-lg font-semibold mb-4 text-gray-900">Model Performance</h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={performanceData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="date" stroke="#6b7280" fontSize={12} />
            <YAxis stroke="#6b7280" fontSize={12} domain={[0.7, 1]} />
            <Tooltip 
              contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
            />
            <Line type="monotone" dataKey="accuracy" stroke="#3b82f6" strokeWidth={2} dot={false} name="Accuracy" />
            <Line type="monotone" dataKey="f1" stroke="#10b981" strokeWidth={2} dot={false} name="F1-Score" />
            <Line type="monotone" dataKey="precision" stroke="#f59e0b" strokeWidth={2} dot={false} name="Precision" />
            <Line type="monotone" dataKey="recall" stroke="#8b5cf6" strokeWidth={2} dot={false} name="Recall" />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <div className="flex justify-center gap-6 mt-4 text-sm">
        <span className="flex items-center gap-2">
          <span className="w-3 h-3 bg-blue-500 rounded-full"></span> Accuracy
        </span>
        <span className="flex items-center gap-2">
          <span className="w-3 h-3 bg-green-500 rounded-full"></span> F1-Score
        </span>
        <span className="flex items-center gap-2">
          <span className="w-3 h-3 bg-amber-500 rounded-full"></span> Precision
        </span>
        <span className="flex items-center gap-2">
          <span className="w-3 h-3 bg-purple-500 rounded-full"></span> Recall
        </span>
      </div>
    </div>
  )
}