'use client'

import { RouteOptimizer } from '@/components/RouteOptimizer'

export default function RoutesPage() {
  return (
    <div className="ml-64 min-h-screen bg-gray-50">
      <main className="p-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Route Optimization</h1>
          <p className="text-gray-600">Optimize delivery routes using AI</p>
        </header>
        
        <RouteOptimizer />
      </main>
    </div>
  )
}