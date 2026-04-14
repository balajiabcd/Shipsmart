'use client'

interface SHAPFeature {
  name: string
  importance: number
  direction: 'positive' | 'negative'
}

const mockFeatures: SHAPFeature[] = [
  { name: 'Weather Condition', importance: 0.85, direction: 'positive' },
  { name: 'Traffic Level', importance: 0.72, direction: 'positive' },
  { name: 'Distance', importance: 0.65, direction: 'positive' },
  { name: 'Time of Day', importance: 0.48, direction: 'positive' },
  { name: 'Driver Rating', importance: 0.35, direction: 'negative' },
  { name: 'Route Complexity', importance: 0.28, direction: 'positive' },
  { name: 'Warehouse Load', importance: 0.22, direction: 'positive' },
  { name: 'Vehicle Type', importance: 0.15, direction: 'negative' },
]

export function SHAPVisualizer() {
  const maxImportance = Math.max(...mockFeatures.map(f => f.importance))

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <h3 className="text-lg font-semibold mb-4 text-gray-900">SHAP Feature Importance</h3>
      <p className="text-sm text-gray-600 mb-4">Feature impact on delay prediction</p>
      
      <div className="space-y-3">
        {mockFeatures.map((feature) => (
          <div key={feature.name} className="flex items-center gap-4">
            <span className="w-32 text-sm text-gray-700 truncate">{feature.name}</span>
            <div className="flex-1 bg-gray-200 rounded-full h-4 overflow-hidden">
              <div 
                className={`h-full rounded-full ${feature.direction === 'positive' ? 'bg-red-500' : 'bg-blue-500'}`}
                style={{ width: `${(feature.importance / maxImportance) * 100}%` }}
              />
            </div>
            <span className="w-12 text-sm text-gray-600 text-right">
              {feature.importance.toFixed(2)}
            </span>
          </div>
        ))}
      </div>

      <div className="mt-4 flex gap-4 text-sm">
        <span className="flex items-center gap-2">
          <span className="w-3 h-3 bg-red-500 rounded-full"></span> Increases delay risk
        </span>
        <span className="flex items-center gap-2">
          <span className="w-3 h-3 bg-blue-500 rounded-full"></span> Decreases delay risk
        </span>
      </div>
    </div>
  )
}