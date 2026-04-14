'use client'

import { AlertPanel } from '@/components/AlertPanel'

export default function AlertsPage() {
  return (
    <div className="ml-64 min-h-screen bg-gray-50">
      <main className="p-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Alerts</h1>
          <p className="text-gray-600">Monitor and manage system alerts</p>
        </header>
        
        <AlertPanel />
      </main>
    </div>
  )
}