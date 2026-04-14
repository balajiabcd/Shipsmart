'use client'

interface Prediction {
  id: string
  order_id: string
  predicted_delay: boolean
  probability: number
  timestamp: string
}

const mockPredictions: Prediction[] = [
  { id: '1', order_id: 'ORD-12345', predicted_delay: true, probability: 0.78, timestamp: '2 min ago' },
  { id: '2', order_id: 'ORD-12346', predicted_delay: false, probability: 0.12, timestamp: '5 min ago' },
  { id: '3', order_id: 'ORD-12347', predicted_delay: true, probability: 0.65, timestamp: '8 min ago' },
  { id: '4', order_id: 'ORD-12348', predicted_delay: false, probability: 0.23, timestamp: '12 min ago' },
  { id: '5', order_id: 'ORD-12349', predicted_delay: false, probability: 0.08, timestamp: '15 min ago' },
]

export function RecentPredictions() {
  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <h3 className="text-lg font-semibold mb-4 text-gray-900">Recent Predictions</h3>
      <div className="space-y-3">
        {mockPredictions.map((pred) => (
          <div key={pred.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div>
              <span className="font-medium text-gray-900">{pred.order_id}</span>
              <span className="text-sm text-gray-500 ml-2">{pred.timestamp}</span>
            </div>
            <div className="flex items-center gap-3">
              <span className={`px-2 py-1 rounded text-xs font-medium ${
                pred.predicted_delay 
                  ? 'bg-red-100 text-red-700' 
                  : 'bg-green-100 text-green-700'
              }`}>
                {pred.predicted_delay ? 'Delayed' : 'On Time'}
              </span>
              <span className="text-sm text-gray-600">{(pred.probability * 100).toFixed(0)}%</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}