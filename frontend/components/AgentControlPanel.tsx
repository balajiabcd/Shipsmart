'use client'

import { useState } from 'react'
import { Play, Pause, RotateCcw, Settings, AlertCircle } from 'lucide-react'

interface Agent {
  id: string
  name: string
  status: 'running' | 'idle' | 'error'
  tasksCompleted: number
  lastRun: string
}

const mockAgents: Agent[] = [
  { id: '1', name: 'Delay Predictor', status: 'running', tasksCompleted: 156, lastRun: '2 min ago' },
  { id: '2', name: 'Route Optimizer', status: 'running', tasksCompleted: 89, lastRun: '5 min ago' },
  { id: '3', name: 'Alert Monitor', status: 'idle', tasksCompleted: 234, lastRun: '10 min ago' },
  { id: '4', name: 'Notification Sender', status: 'error', tasksCompleted: 178, lastRun: '30 min ago' },
]

export function AgentControlPanel() {
  const [agents, setAgents] = useState(mockAgents)

  const toggleAgent = (id: string) => {
    setAgents(agents.map(a => 
      a.id === id ? { ...a, status: a.status === 'running' ? 'idle' : 'running' } : a
    ))
  }

  const statusStyles = {
    running: 'bg-green-100 text-green-700',
    idle: 'bg-gray-100 text-gray-700',
    error: 'bg-red-100 text-red-700',
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Agent Control Panel</h3>
        <button className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg">
          <Settings className="w-5 h-5" />
        </button>
      </div>

      <div className="space-y-4">
        {agents.map((agent) => (
          <div key={agent.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center gap-4">
              <button
                onClick={() => toggleAgent(agent.id)}
                className={`p-2 rounded-lg ${
                  agent.status === 'running' 
                    ? 'bg-green-100 text-green-600' 
                    : 'bg-gray-200 text-gray-500'
                }`}
              >
                {agent.status === 'running' ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
              </button>
              <div>
                <p className="font-medium text-gray-900">{agent.name}</p>
                <p className="text-sm text-gray-500">{agent.tasksCompleted} tasks • {agent.lastRun}</p>
              </div>
            </div>
            <span className={`px-3 py-1 rounded-full text-xs font-medium ${statusStyles[agent.status]}`}>
              {agent.status}
            </span>
          </div>
        ))}
      </div>

      <button className="mt-4 flex items-center gap-2 px-4 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded-lg">
        <RotateCcw className="w-4 h-4" />
        Reset All Agents
      </button>
    </div>
  )
}