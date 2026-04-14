'use client'

import { AlertTriangle } from 'lucide-react'

interface Alert {
  id: string
  type: string
  severity: 'critical' | 'high' | 'medium' | 'low'
  message: string
  timestamp: string
}

const mockAlerts: Alert[] = [
  { id: '1', type: 'anomaly', severity: 'high', message: 'Munich region has 35% increase in delays', timestamp: '5 min ago' },
  { id: '2', type: 'weather', severity: 'medium', message: 'Heavy rainfall expected in Berlin area', timestamp: '15 min ago' },
  { id: '3', type: 'traffic', severity: 'low', message: 'Rush hour congestion on A12 highway', timestamp: '30 min ago' },
]

const severityStyles = {
  critical: 'border-red-500 bg-red-50',
  high: 'border-orange-500 bg-orange-50',
  medium: 'border-yellow-500 bg-yellow-50',
  low: 'border-blue-500 bg-blue-50',
}

const severityTextStyles = {
  critical: 'text-red-700',
  high: 'text-orange-700',
  medium: 'text-yellow-700',
  low: 'text-blue-700',
}

export function AlertPanel() {
  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <div className="flex items-center gap-2 mb-4">
        <AlertTriangle className="w-5 h-5 text-orange-500" />
        <h3 className="text-lg font-semibold text-gray-900">Active Alerts</h3>
      </div>
      <div className="space-y-3">
        {mockAlerts.map((alert) => (
          <div 
            key={alert.id} 
            className={`p-4 rounded-lg border-l-4 ${severityStyles[alert.severity]}`}
          >
            <div className="flex items-start justify-between">
              <div>
                <span className={`text-xs font-medium uppercase ${severityTextStyles[alert.severity]}`}>
                  {alert.severity}
                </span>
                <p className="text-sm text-gray-700 mt-1">{alert.message}</p>
              </div>
              <span className="text-xs text-gray-500">{alert.timestamp}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}