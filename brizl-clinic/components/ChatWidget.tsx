'use client'

import { motion, AnimatePresence } from 'framer-motion'
import { X, Send, MessageCircle } from 'lucide-react'
import { useChat } from '@/hooks/useChat'
import { clinicInfo } from '@/lib/clinic-data'
import { useState, useRef, useEffect } from 'react'

// Vera avatar emoji
const VERA_AVATAR = '🤖'

// Quick action buttons
const quickActions = [
  { label: '🗓️ Müayinəyə yazıl', message: 'Müayinəyə yazılmaq istəyirəm' },
  { label: '👩⚕️ Həkimlər', message: 'Həkimlər haqqında məlumat ver' },
  { label: '🏥 Əməliyyatlar', message: 'Əməliyyatlar haqqında məlumat ver' },
]

export default function ChatWidget() {
  const { isOpen, isLoading, messages, toggleChat, closeChat, sendMessage } = useChat()
  const [input, setInput] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Focus input when chat opens
  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus()
    }
  }, [isOpen])

  // Handle send message
  const handleSend = async () => {
    if (!input.trim() || isLoading) return
    const message = input.trim()
    setInput('')
    await sendMessage(message)
  }

  // Handle key press
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  // Handle button click from bot message
  const handleButtonClick = async (payload: string) => {
    await sendMessage(payload)
  }

  return (
    <>
      {/* Floating Button */}
      <motion.button
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 1, type: 'spring', stiffness: 200 }}
        onClick={toggleChat}
        className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-mint text-white shadow-lg hover:bg-mint-dark transition-colors flex items-center justify-center text-2xl"
        aria-label="Open chat"
      >
        <AnimatePresence mode="wait">
          {isOpen ? (
            <motion.div
              key="close"
              initial={{ rotate: -90, opacity: 0 }}
              animate={{ rotate: 0, opacity: 1 }}
              exit={{ rotate: 90, opacity: 0 }}
            >
              <X className="w-6 h-6" />
            </motion.div>
          ) : (
            <motion.div
              key="chat"
              initial={{ rotate: 90, opacity: 0 }}
              animate={{ rotate: 0, opacity: 1 }}
              exit={{ rotate: -90, opacity: 0 }}
            >
              <MessageCircle className="w-6 h-6" />
            </motion.div>
          )}
        </AnimatePresence>
      </motion.button>

      {/* Chat Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            className="fixed bottom-24 right-6 z-50 w-[360px] max-w-[calc(100vw-48px)] h-[500px] max-h-[calc(100vh-150px)] rounded-2xl overflow-hidden shadow-2xl glass border border-mint/20 flex flex-col"
          >
            {/* Header */}
            <div className="bg-mint text-white px-4 py-3 flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center text-xl">
                {VERA_AVATAR}
              </div>
              <div className="flex-1">
                <h3 className="font-semibold text-sm">VERA</h3>
                <p className="text-xs text-white/70">Briz-L Göz Klinikası</p>
              </div>
              <button
                onClick={closeChat}
                className="w-8 h-8 rounded-full hover:bg-white/10 flex items-center justify-center transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50/50">
              {/* Welcome message if no messages */}
              {messages.length === 0 && (
                <div className="space-y-4">
                  <div className="flex gap-2">
                    <div className="w-8 h-8 rounded-full bg-mint/10 flex items-center justify-center text-sm flex-shrink-0">
                      {VERA_AVATAR}
                    </div>
                    <div className="bg-white rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm max-w-[80%]">
                      <p className="text-sm text-gray-700">
                        Salam! Mən VERA, Briz-L Göz Klinikasının virtual köməkçisiyəm. 👋 Sizə necə kömək edə bilərəm?
                      </p>
                    </div>
                  </div>
                  
                  {/* Quick Actions */}
                  <div className="flex flex-wrap gap-2 ml-10">
                    {quickActions.map((action) => (
                      <button
                        key={action.label}
                        onClick={() => sendMessage(action.message)}
                        disabled={isLoading}
                        className="px-3 py-1.5 text-xs rounded-full bg-mint/10 text-mint hover:bg-mint/20 transition-colors disabled:opacity-50"
                      >
                        {action.label}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Message list */}
              {messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex gap-2 ${msg.type === 'user' ? 'justify-end' : ''}`}
                >
                  {msg.type === 'bot' && (
                    <div className="w-8 h-8 rounded-full bg-mint/10 flex items-center justify-center text-sm flex-shrink-0">
                      {VERA_AVATAR}
                    </div>
                  )}
                  <div
                    className={`max-w-[80%] rounded-2xl px-4 py-3 shadow-sm ${
                      msg.type === 'user'
                        ? 'bg-mint text-white rounded-tr-sm'
                        : 'bg-white rounded-tl-sm'
                    }`}
                  >
                    <p className={`text-sm ${msg.type === 'user' ? 'text-white' : 'text-gray-700'}`}>
                      {msg.text}
                    </p>
                    
                    {/* Buttons */}
                    {msg.buttons && msg.buttons.length > 0 && (
                      <div className="flex flex-wrap gap-2 mt-3">
                        {msg.buttons.map((btn, idx) => (
                          <button
                            key={idx}
                            onClick={() => handleButtonClick(btn.payload)}
                            disabled={isLoading}
                            className="px-3 py-1.5 text-xs rounded-full bg-mint/10 text-mint hover:bg-mint/20 transition-colors disabled:opacity-50"
                          >
                            {btn.title}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {/* Typing indicator */}
              {isLoading && (
                <div className="flex gap-2">
                  <div className="w-8 h-8 rounded-full bg-mint/10 flex items-center justify-center text-sm flex-shrink-0">
                    {VERA_AVATAR}
                  </div>
                  <div className="bg-white rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm">
                    <div className="flex gap-1">
                      <motion.div
                        animate={{ opacity: [0.4, 1, 0.4] }}
                        transition={{ duration: 1, repeat: Infinity, delay: 0 }}
                        className="w-2 h-2 rounded-full bg-gray-400"
                      />
                      <motion.div
                        animate={{ opacity: [0.4, 1, 0.4] }}
                        transition={{ duration: 1, repeat: Infinity, delay: 0.2 }}
                        className="w-2 h-2 rounded-full bg-gray-400"
                      />
                      <motion.div
                        animate={{ opacity: [0.4, 1, 0.4] }}
                        transition={{ duration: 1, repeat: Infinity, delay: 0.4 }}
                        className="w-2 h-2 rounded-full bg-gray-400"
                      />
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-3 border-t border-gray-100 bg-white">
              <div className="flex gap-2">
                <input
                  ref={inputRef}
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Mesajınızı yazın..."
                  disabled={isLoading}
                  className="flex-1 px-4 py-2.5 rounded-xl bg-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-mint/30 disabled:opacity-50"
                />
                <button
                  onClick={handleSend}
                  disabled={!input.trim() || isLoading}
                  className="w-10 h-10 rounded-xl bg-mint text-white flex items-center justify-center hover:bg-mint-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
              
              {/* WhatsApp fallback */}
              <a
                href={clinicInfo.social.whatsapp}
                target="_blank"
                rel="noopener noreferrer"
                className="block text-center text-xs text-gray-400 hover:text-mint mt-2 transition-colors"
              >
                WhatsApp ilə əlaqə →
              </a>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}