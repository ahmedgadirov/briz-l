'use client'

import { useState, useCallback, useEffect, createContext, useContext, ReactNode } from 'react'
import { sendMessageToRasa, generateSessionId, RasaMessage, getSurgeryQuery, getDoctorQuery } from '@/lib/rasa-api'

// Chat message type for UI
export interface ChatMessage {
  id: string
  type: 'user' | 'bot'
  text: string
  buttons?: Array<{
    title: string
    payload: string
  }>
  timestamp: Date
}

// Chat context type
export interface ChatContextType {
  isOpen: boolean
  isLoading: boolean
  messages: ChatMessage[]
  sessionId: string
  openChat: () => void
  closeChat: () => void
  toggleChat: () => void
  sendMessage: (message: string) => Promise<void>
  sendSurgeryQuery: (surgeryId: string) => Promise<void>
  sendDoctorQuery: (doctorId: string) => Promise<void>
  clearMessages: () => void
}

// Create context
export const ChatContext = createContext<ChatContextType | undefined>(undefined)

// Local storage key for session
const SESSION_KEY = 'vera_session_id'
const MESSAGES_KEY = 'vera_messages'

/**
 * Simple analytics tracking
 */
function trackChatEvent(eventName: string, data?: Record<string, unknown>) {
  console.log(`[Vera Analytics] ${eventName}:`, data)
  
  if (typeof window !== 'undefined') {
    const win = window as unknown as { gtag?: (...args: unknown[]) => void }
    if (win.gtag) {
      win.gtag('event', eventName, data)
    }
  }
}

/**
 * Chat Provider - wraps the app and provides chat state
 */
export function ChatProvider({ children }: { children: ReactNode }) {
  const [isOpen, setIsOpen] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [sessionId, setSessionId] = useState<string>('')

  // Initialize session from localStorage or create new
  useEffect(() => {
    const savedSession = localStorage.getItem(SESSION_KEY)
    const savedMessages = localStorage.getItem(MESSAGES_KEY)
    
    if (savedSession) {
      setSessionId(savedSession)
    } else {
      const newSession = generateSessionId()
      setSessionId(newSession)
      localStorage.setItem(SESSION_KEY, newSession)
    }

    if (savedMessages) {
      try {
        const parsed = JSON.parse(savedMessages)
        setMessages(parsed.map((m: ChatMessage) => ({
          ...m,
          timestamp: new Date(m.timestamp)
        })))
      } catch {
        // Ignore parse errors
      }
    }
  }, [])

  // Save messages to localStorage when they change
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem(MESSAGES_KEY, JSON.stringify(messages))
    }
  }, [messages])

  // Open chat
  const openChat = useCallback(() => {
    setIsOpen(true)
  }, [])

  // Close chat
  const closeChat = useCallback(() => {
    setIsOpen(false)
  }, [])

  // Toggle chat
  const toggleChat = useCallback(() => {
    setIsOpen(prev => !prev)
  }, [])

  // Send message to Vera
  const sendMessage = useCallback(async (message: string) => {
    if (!message.trim() || isLoading) return

    // Add user message
    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      type: 'user',
      text: message.trim(),
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      // Send to Rasa
      const responses = await sendMessageToRasa(sessionId, message)

      // Add bot responses
      responses.forEach((response: RasaMessage, index: number) => {
        if (response.text) {
          const botMessage: ChatMessage = {
            id: `bot-${Date.now()}-${index}`,
            type: 'bot',
            text: response.text,
            buttons: response.buttons?.filter(b => b.type !== 'web_url'),
            timestamp: new Date()
          }
          setMessages(prev => [...prev, botMessage])
        }
      })

      // Track analytics
      trackChatEvent('message_sent', { message, responseCount: responses.length })
    } catch (error) {
      console.error('Failed to send message:', error)
      
      // Add error message
      const errorMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        type: 'bot',
        text: 'Bağışlayın, texniki xəta baş verdi. Zəhmət olmasa bir az sonra yenidən cəhd edin və ya WhatsApp ilə əlaqə saxlayın: wa.me/994555512400',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }, [sessionId, isLoading])

  // Send surgery query
  const sendSurgeryQuery = useCallback(async (surgeryId: string) => {
    const query = getSurgeryQuery(surgeryId)
    await sendMessage(query)
  }, [sendMessage])

  // Send doctor query
  const sendDoctorQuery = useCallback(async (doctorId: string) => {
    const query = getDoctorQuery(doctorId)
    await sendMessage(query)
  }, [sendMessage])

  // Clear messages
  const clearMessages = useCallback(() => {
    setMessages([])
    localStorage.removeItem(MESSAGES_KEY)
  }, [])

  const value: ChatContextType = {
    isOpen,
    isLoading,
    messages,
    sessionId,
    openChat,
    closeChat,
    toggleChat,
    sendMessage,
    sendSurgeryQuery,
    sendDoctorQuery,
    clearMessages
  }

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  )
}

/**
 * Hook to use chat context
 */
export function useChat() {
  const context = useContext(ChatContext)
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider')
  }
  return context
}

export default useChat