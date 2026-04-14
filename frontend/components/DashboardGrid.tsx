'use client'

import { TrendingUp, AlertTriangle, Package, Clock } from 'lucide-react'
import { PredictionCard } from './PredictionCard'
import { RecentPredictions } from './RecentPredictions'
import { AlertPanel } from './AlertPanel'
import { ModelPerformance } from './ModelPerformance'

export function DashboardGrid() {
  const stats = [
    { label: 'Total Predictions', value: '1,234', icon: TrendingUp, color: 'text-blue-600' },
    { label: 'Active Alerts', value: '5', icon: AlertTriangle, color: 'text-orange-600' },
    { label: 'Deliveries Today', value: '89', icon: Package, color: 'text-green-600' },
    { label: 'Avg Delay', value: '12 min', icon: Clock, color: 'text-purple-600' },
  ]

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <div key={stat.label} className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">{stat.label}</p>
                <p className="text-2xl font-bold text-gray-900 mt-1">{stat.value}</p>
              </div>
              <stat.icon className={`w-8 h-8 ${stat.color}`} />
            </div>
          </div>
        ))}
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <PredictionCard />
        <RecentPredictions />
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AlertPanel />
        <ModelPerformance />
      </div>
    </div>
  )
}