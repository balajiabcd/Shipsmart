'use client'

import { DataExplorer } from '@/components/DataExplorer'

export default function DataPage() {
  return (
    <div className="ml-64 min-h-screen bg-gray-50">
      <main className="p-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Data Explorer</h1>
          <p className="text-gray-600">Browse and search delivery data</p>
        </header>
        
        <DataExplorer />
      </main>
    </div>
  )
}