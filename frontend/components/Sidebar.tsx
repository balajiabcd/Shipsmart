import { Home, TrendingUp, AlertTriangle, Route, MessageSquare, Settings, User, Database } from 'lucide-react'

export function Sidebar() {
  const items = [
    { icon: Home, label: 'Dashboard', href: '/' },
    { icon: TrendingUp, label: 'Predictions', href: '/predictions' },
    { icon: AlertTriangle, label: 'Alerts', href: '/alerts' },
    { icon: Route, label: 'Routes', href: '/routes' },
    { icon: Database, label: 'Data', href: '/data' },
    { icon: MessageSquare, label: 'AI Chat', href: '/chat' },
  ]
  
  return (
    <aside className="w-64 bg-white border-r border-gray-200 p-4 h-screen fixed left-0 top-0">
      <div className="text-xl font-bold text-blue-600 mb-8">Shipsmart</div>
      <nav className="space-y-2">
        {items.map((item) => (
          <a 
            key={item.label} 
            href={item.href} 
            className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-100 text-gray-700 hover:text-gray-900 transition-colors"
          >
            <item.icon className="w-5 h-5" />
            {item.label}
          </a>
        ))}
      </nav>
      <div className="absolute bottom-4 left-4 w-56">
        <a href="/settings" className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-100 text-gray-700">
          <Settings className="w-5 h-5" />
          Settings
        </a>
        <a href="/profile" className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-100 text-gray-700">
          <User className="w-5 h-5" />
          Profile
        </a>
      </div>
    </aside>
  )
}