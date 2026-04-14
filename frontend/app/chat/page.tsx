'use client'

import { ChatInterface } from '@/components/ChatInterface'

export default function ChatPage() {
  return (
    <div className="ml-64 min-h-screen bg-gray-50">
      <main className="p-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">AI Chat</h1>
          <p className="text-gray-600">Ask questions about deliveries, delays, and recommendations</p>
        </header>
        
        <div className="max-w-3xl">
          <ChatInterface />
        </div>
      </main>
    </div>
  )
}