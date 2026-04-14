'use client'

import { PredictionForm } from '@/components/PredictionForm'
import { DelayAnalytics } from '@/components/DelayAnalytics'
import { SHAPVisualizer } from '@/components/SHAPVisualizer'

export default function PredictionsPage() {
  return (
    <div className="ml-64 min-h-screen bg-gray-50">
      <main className="p-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Delay Predictions</h1>
          <p className="text-gray-600">Predict and analyze delivery delays</p>
        </header>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <PredictionForm />
          <SHAPVisualizer />
        </div>
        
        <DelayAnalytics />
      </main>
    </div>
  )
}