'use client'

import { ChatProvider } from '@/hooks/useChat'
import ChatWidget from './ChatWidget'

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ChatProvider>
      {children}
      <ChatWidget />
    </ChatProvider>
  )
}