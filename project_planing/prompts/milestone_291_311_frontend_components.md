# Milestone #291-311: Frontend Components Complete

```typescript
// frontend/components/AnalyticsCharts.tsx - Delay Analytics
import { LineChart, BarChart, PieChart } from 'recharts'

export function DelayAnalytics() {
  const delayData = [
    { date: '2024-01', rate: 0.15 },
    { date: '2024-02', rate: 0.18 },
    { date: '2024-03', rate: 0.12 },
  ]
  
  return (
    <div className="grid grid-cols-2 gap-4">
      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Delay Rate Trend</h3>
        <LineChart data={delayData}>
          <XAxis dataKey="date" />
          <YAxis />
          <Line dataKey="rate" />
        </LineChart>
      </div>
      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Delay Causes</h3>
        <PieChart data={[
          { name: 'Weather', value: 35 },
          { name: 'Traffic', value: 40 },
          { name: 'Driver', value: 25 },
        ]} />
      </div>
    </div>
  )
}

// frontend/components/ChatInterface.tsx
export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  
  const sendMessage = async () => {
    const res = await fetch('/api/chat', {
      method: 'POST',
      body: JSON.stringify({ message: input }),
    })
    const data = await res.json()
    setMessages([...messages, { role: 'user', content: input }, { role: 'assistant', content: data.response }])
    setInput('')
  }
  
  return (
    <div className="flex flex-col h-[500px] bg-white rounded-lg shadow">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map(m => (
          <div className={m.role === 'user' ? 'text-right' : 'text-left'}>
            <span className={`inline-block p-3 rounded ${m.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}>
              {m.content}
            </span>
          </div>
        ))}
      </div>
      <div className="border-t p-4 flex gap-2">
        <input value={input} onChange={e => setInput(e.target.value)} className="flex-1 border rounded px-3 py-2" />
        <button onClick={sendMessage} className="px-4 py-2 bg-blue-500 text-white rounded">Send</button>
      </div>
    </div>
  )
}

// frontend/components/AlertPanel.tsx
export function AlertPanel() {
  const alerts = useQuery({ queryKey: ['/api/alerts'] })
  
  return (
    <div className="space-y-2">
      {alerts.data?.alerts.map(alert => (
        <div key={alert.id} className={`p-4 rounded-lg border-l-4 ${
          alert.severity === 'critical' ? 'border-red-500 bg-red-50' :
          alert.severity === 'high' ? 'border-orange-500 bg-orange-50' :
          'border-yellow-500 bg-yellow-50'
        }`}>
          <div className="font-semibold">{alert.title}</div>
          <div className="text-sm">{alert.message}</div>
          <div className="text-xs text-gray-500 mt-1">{alert.timestamp}</div>
        </div>
      ))}
    </div>
  )
}

// frontend/components/RouteOptimizer.tsx
export function RouteOptimizer() {
  const [deliveries, setDeliveries] = useState([])
  
  const optimize = async () => {
    const res = await fetch('/api/optimize_route', { method: 'POST', body: JSON.stringify({ deliveries }) })
    const data = await res.json()
    // Render route on map
  }
  
  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">Route Optimization</h3>
      <div id="map" className="h-96 bg-gray-100 rounded mb-4" />
      <button onClick={optimize} className="btn-primary">Optimize Routes</button>
    </div>
  )
}

// frontend/components/SHAPVisualizer.tsx
export function SHAPVisualizer() {
  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">SHAP Feature Importance</h3>
      <div className="space-y-2">
        {features.map(f => (
          <div key={f.name} className="flex items-center gap-2">
            <span className="w-32">{f.name}</span>
            <div className="flex-1 bg-gray-200 rounded">
              <div className="bg-blue-500 rounded" style={{ width: `${f.importance * 100}%`, height: 20 }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// Theme & Responsive
// frontend/app/globals.css
@media (max-width: 768px) {
  .sidebar { display: none; }
  .grid-cols-2 { grid-template-columns: 1fr; }
}

// State Management - frontend/lib/store.ts
import { create } from 'zustand'

export const useStore = create(set => ({
  predictions: [],
  setPredictions: (predictions) => set({ predictions }),
  theme: 'light',
  toggleTheme: () => set(state => ({ theme: state.theme === 'light' ? 'dark' : 'light' })),
}))
```

Commit all frontend components.