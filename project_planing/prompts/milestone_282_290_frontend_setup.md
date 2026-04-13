# Milestone #282-290: Initialize Next.js Project and Create UI

```bash
# Set up Next.js project
npx create-next-app@latest frontend --typescript --tailwind --eslint
cd frontend
npm install @tanstack/react-query recharts lucide-react
```

```typescript
// frontend/app/page.tsx - Main Dashboard
export default function Dashboard() {
  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 p-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Shipsmart Dashboard</h1>
          <p className="text-gray-600">AI-Powered Delivery Management</p>
        </header>
        <DashboardGrid />
      </main>
    </div>
  )
}

// frontend/components/Sidebar.tsx
export function Sidebar() {
  const items = [
    { icon: Home, label: 'Dashboard', href: '/' },
    { icon: TrendingUp, label: 'Predictions', href: '/predictions' },
    { icon: AlertTriangle, label: 'Alerts', href: '/alerts' },
    { icon: Route, label: 'Routes', href: '/routes' },
    { icon: MessageSquare, label: 'AI Chat', href: '/chat' },
  ]
  
  return (
    <aside className="w-64 bg-white border-r p-4">
      <div className="text-xl font-bold text-blue-600 mb-8">Shipsmart</div>
      <nav className="space-y-2">
        {items.map(item => (
          <a href={item.href} className="flex items-center gap-3 p-3 rounded hover:bg-gray-100">
            <item.icon className="w-5 h-5" />
            {item.label}
          </a>
        ))}
      </nav>
    </aside>
  )
}

// frontend/components/PredictionForm.tsx
export function PredictionForm() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  
  const handleSubmit = async (data) => {
    setLoading(true)
    const res = await fetch('/api/predict', { method: 'POST', body: JSON.stringify(data) })
    setResult(await res.json())
    setLoading(false)
  }
  
  return (
    <form onSubmit={handleSubmit} className="space-y-4 bg-white p-6 rounded-lg shadow">
      <input name="delivery_id" placeholder="Delivery ID" className="input-field" />
      <input name="distance_km" type="number" placeholder="Distance (km)" className="input-field" />
      <select name="weather_condition" className="input-field">
        <option value="clear">Clear</option>
        <option value="rain">Rain</option>
        <option value="storm">Storm</option>
      </select>
      <button type="submit" disabled={loading} className="btn-primary">
        {loading ? 'Predicting...' : 'Get Prediction'}
      </button>
      {result && <PredictionResult data={result} />}
    </form>
  )
}
```

Commit.