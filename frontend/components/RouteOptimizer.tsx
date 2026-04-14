'use client'

import { useState } from 'react'
import { MapPin, Play, Loader2 } from 'lucide-react'

interface Delivery {
  id: string
  address: string
  lat: number
  lng: number
}

export function RouteOptimizer() {
  const [deliveries, setDeliveries] = useState<Delivery[]>([
    { id: '1', address: 'Berlin, Hauptstraße 15', lat: 52.52, lng: 13.405 },
    { id: '2', address: 'Berlin, Invalidenstraße 100', lat: 52.53, lng: 13.38 },
    { id: '3', address: 'Berlin, Torstraße 120', lat: 52.53, lng: 13.4 },
  ])
  const [optimizedRoute, setOptimizedRoute] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const optimize = async () => {
    setLoading(true)
    try {
      const res = await fetch('http://localhost:8000/api/v1/optimize_route', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ deliveries }),
      })
      const data = await res.json()
      setOptimizedRoute(data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <h3 className="text-lg font-semibold mb-4 text-gray-900">Route Optimization</h3>
      
      <div className="mb-4 h-64 bg-gray-100 rounded-lg flex items-center justify-center">
        <div className="text-center text-gray-500">
          <MapPin className="w-12 h-12 mx-auto mb-2" />
          <p>Map visualization</p>
          <p className="text-sm">Interactive map would render here</p>
        </div>
      </div>

      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Deliveries to Optimize</h4>
        <div className="space-y-2">
          {deliveries.map((d) => (
            <div key={d.id} className="flex items-center gap-2 p-2 bg-gray-50 rounded text-sm">
              <MapPin className="w-4 h-4 text-gray-400" />
              <span>{d.address}</span>
            </div>
          ))}
        </div>
      </div>

      <button
        onClick={optimize}
        disabled={loading}
        className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
      >
        {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
        {loading ? 'Optimizing...' : 'Optimize Routes'}
      </button>

      {optimizedRoute && (
        <div className="mt-4 p-4 bg-green-50 rounded-lg">
          <h4 className="font-medium text-green-800">Optimization Complete</h4>
          <pre className="text-sm text-green-700 mt-2 overflow-auto">
            {JSON.stringify(optimizedRoute, null, 2)}
          </pre>
        </div>
      )}
    </div>
  )
}