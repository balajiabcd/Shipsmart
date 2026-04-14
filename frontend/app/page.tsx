'use client'

import { Sidebar } from '@/components/Sidebar'
import { DashboardGrid } from '@/components/DashboardGrid'

export default function Dashboard() {
  return (
    <div className="ml-64 min-h-screen bg-gray-50">
      <main className="p-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Shipsmart Dashboard</h1>
          <p className="text-gray-600">AI-Powered Delivery Management</p>
        </header>
        <DashboardGrid />
      </main>
    </div>
  )
}