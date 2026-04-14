'use client'

import { useState } from 'react'
import { Search, Filter, Download, Eye } from 'lucide-react'

interface DataRecord {
  id: string
  order_id: string
  origin: string
  destination: string
  status: string
  predicted_delay: boolean
  actual_delay: number
}

const mockData: DataRecord[] = [
  { id: '1', order_id: 'ORD-12345', origin: 'Berlin', destination: 'Munich', status: 'Delivered', predicted_delay: true, actual_delay: 15 },
  { id: '2', order_id: 'ORD-12346', origin: 'Hamburg', destination: 'Berlin', status: 'In Transit', predicted_delay: false, actual_delay: 0 },
  { id: '3', order_id: 'ORD-12347', origin: 'Frankfurt', destination: 'Stuttgart', status: 'Delivered', predicted_delay: true, actual_delay: 22 },
  { id: '4', order_id: 'ORD-12348', origin: 'Munich', destination: 'Nuremberg', status: 'Delivered', predicted_delay: false, actual_delay: 5 },
  { id: '5', order_id: 'ORD-12349', origin: 'Berlin', destination: 'Dresden', status: 'In Transit', predicted_delay: false, actual_delay: 0 },
]

export function DataExplorer() {
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')
  const [selectedRecord, setSelectedRecord] = useState<DataRecord | null>(null)

  const filteredData = mockData.filter(record => {
    const matchesSearch = record.order_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      record.origin.toLowerCase().includes(searchTerm.toLowerCase()) ||
      record.destination.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesFilter = filterStatus === 'all' || record.status === filterStatus
    return matchesSearch && matchesFilter
  })

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap gap-4">
        <div className="relative flex-1 min-w-[200px]">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search orders..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-gray-400" />
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Status</option>
            <option value="Delivered">Delivered</option>
            <option value="In Transit">In Transit</option>
            <option value="Pending">Pending</option>
          </select>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
          <Download className="w-4 h-4" />
          Export
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">Order ID</th>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">Origin</th>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">Destination</th>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">Status</th>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">Predicted</th>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">Actual (min)</th>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {filteredData.map((record) => (
              <tr key={record.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-sm font-medium text-gray-900">{record.order_id}</td>
                <td className="px-4 py-3 text-sm text-gray-600">{record.origin}</td>
                <td className="px-4 py-3 text-sm text-gray-600">{record.destination}</td>
                <td className="px-4 py-3 text-sm">
                  <span className={`px-2 py-1 rounded text-xs font-medium ${
                    record.status === 'Delivered' ? 'bg-green-100 text-green-700' :
                    record.status === 'In Transit' ? 'bg-blue-100 text-blue-700' :
                    'bg-gray-100 text-gray-700'
                  }`}>
                    {record.status}
                  </span>
                </td>
                <td className="px-4 py-3 text-sm">
                  <span className={`px-2 py-1 rounded text-xs font-medium ${
                    record.predicted_delay ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'
                  }`}>
                    {record.predicted_delay ? 'Delayed' : 'On Time'}
                  </span>
                </td>
                <td className="px-4 py-3 text-sm text-gray-600">{record.actual_delay}</td>
                <td className="px-4 py-3">
                  <button 
                    onClick={() => setSelectedRecord(record)}
                    className="p-1 text-gray-400 hover:text-gray-600"
                  >
                    <Eye className="w-4 h-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedRecord && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={() => setSelectedRecord(null)}>
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-lg font-semibold mb-4">Order Details</h3>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Order ID:</span>
                <span className="font-medium">{selectedRecord.order_id}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Origin:</span>
                <span>{selectedRecord.origin}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Destination:</span>
                <span>{selectedRecord.destination}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Status:</span>
                <span>{selectedRecord.status}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Predicted Delay:</span>
                <span>{selectedRecord.predicted_delay ? 'Yes' : 'No'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Actual Delay:</span>
                <span>{selectedRecord.actual_delay} min</span>
              </div>
            </div>
            <button 
              onClick={() => setSelectedRecord(null)}
              className="mt-4 w-full py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  )
}