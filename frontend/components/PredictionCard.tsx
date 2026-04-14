'use client'

import { useState } from 'react'
import { Search } from 'lucide-react'

interface PredictionResult {
  order_id: string
  predicted_delay: boolean
  delay_probability: number
  delay_minutes?: number
  confidence: string
}

export function PredictionCard() {
  const [deliveryId, setDeliveryId] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<PredictionResult | null>(null)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!deliveryId.trim()) {
      setError('Please enter a delivery ID')
      return
    }
    setLoading(true)
    setError('')
    try {
      const res = await fetch('http://localhost:8000/api/v1/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ order_id: deliveryId }),
      })
      if (!res.ok) throw new Error('Failed to fetch prediction')
      const data = await res.json()
      setResult(data)
    } catch (err) {
      setError('Could not connect to API. Make sure the backend is running.')
      setResult(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <h3 className="text-lg font-semibold mb-4 text-gray-900">Quick Prediction</h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              value={deliveryId}
              onChange={(e) => setDeliveryId(e.target.value)}
              placeholder="Enter delivery ID (e.g., ORD-12345)"
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            {loading ? '...' : 'Predict'}
          </button>
        </div>
        {error && <p className="text-sm text-red-600">{error}</p>}
        {result && (
          <div className="mt-4 p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-600">Order ID:</span>
              <span className="font-medium">{result.order_id}</span>
            </div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-600">Prediction:</span>
              <span className={`font-medium ${result.predicted_delay ? 'text-red-600' : 'text-green-600'}`}>
                {result.predicted_delay ? 'Delayed' : 'On Time'}
              </span>
            </div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-600">Probability:</span>
              <span className="font-medium">{(result.delay_probability * 100).toFixed(1)}%</span>
            </div>
            {result.delay_minutes !== undefined && (
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-gray-600">Est. Delay:</span>
                <span className="font-medium">{result.delay_minutes} min</span>
              </div>
            )}
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Confidence:</span>
              <span className="font-medium capitalize">{result.confidence}</span>
            </div>
          </div>
        )}
      </form>
    </div>
  )
}