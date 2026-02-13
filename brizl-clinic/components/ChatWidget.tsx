'use client'

import { motion, AnimatePresence } from 'framer-motion'
import { X, Send, MessageCircle } from 'lucide-react'
import { useChat } from '@/hooks/useChat'
import { clinicInfo } from '@/lib/clinic-data'
import { useState, useRef, useEffect, useCallback } from 'react'

// Vera avatar emoji
const VERA_AVATAR = '🤖'

// Quick action buttons
const quickActions = [
  { label: '🗓️ Müayinəyə yazıl', message: 'Müayinəyə yazılmaq istəyirəm' },
  { label: '👩⚕️ Həkimlər', message: 'Həkimlər haqqında məlumat ver' },
  { label: '🏥 Əməliyyatlar', message: 'Əməliyyatlar haqqında məlumat ver' },
]

// Check for reduced motion preference
const prefersReducedMotion = () => {
  if (typeof window === 'undefined') return false
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

export default function ChatWidget() {
  const { isOpen, isLoading, messages, toggleChat, closeChat, sendMessage } = useChat()
  const [input, setInput] = useState('')
  const [isMobile, setIsMobile] = useState(false)
  const [keyboardHeight, setKeyboardHeight] = useState(0)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)
  const chatContainerRef = useRef<HTMLDivElement>(null)

  // Mobile detection
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 640)
    }
    
    checkMobile()
    window.addEventListener('resize', checkMobile)
    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  // Keyboard handler for mobile
  useEffect(() => {
    if (!isOpen || !isMobile) return

    const handleResize = () => {
      if (window.visualViewport) {
        const keyboardHeight = window.innerHeight - window.visualViewport.height
        setKeyboardHeight(keyboardHeight > 100 ? keyboardHeight : 0)
        
        // Scroll input into view when keyboard opens
        if (keyboardHeight > 100) {
          setTimeout(() => {
            inputRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
          }, 100)
        }
      }
    }

    window.visualViewport?.addEventListener('resize', handleResize)
    return () => window.visualViewport?.removeEventListener('resize', handleResize)
  }, [isOpen, isMobile])

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Focus input when chat opens
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => {
        inputRef.current?.focus()
      }, 100)
    }
  }, [isOpen])

  // Prevent body scroll when chat is open on mobile
  useEffect(() => {
    if (isOpen && isMobile) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }
    return () => {
      document.body.style.overflow = ''
    }
  }, [isOpen, isMobile])

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

  // Handle backdrop click (close chat)
  const handleBackdropClick = () => {
    closeChat()
  }

  // Handle escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        closeChat()
      }
    }
    window.addEventListener('keydown', handleEscape)
    return () => window.removeEventListener('keydown', handleEscape)
  }, [isOpen, closeChat])

  return (
    <>
      {/* Floating Button */}
      <motion.button
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 1, type: 'spring', stiffness: 200 }}
        onClick={toggleChat}
        className="fixed z-50 rounded-full bg-mint text-white shadow-lg hover:bg-mint-dark transition-colors flex items-center justify-center text-2xl"
        style={{
          width: isMobile ? '60px' : '56px',
          height: isMobile ? '60px' : '56px',
          bottom: `calc(1.5rem + env(safe-area-inset-bottom))`,
          right: `calc(1rem + env(safe-area-inset-right))`,
        }}
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
        aria-expanded={isOpen}
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

      {/* Chat Window - Mobile Fullscreen */}
      <AnimatePresence>
        {isOpen && isMobile && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: prefersReducedMotion() ? 0 : 0.2 }}
              className="fixed inset-0 bg-black/40 backdrop-blur-sm z-40"
              onClick={handleBackdropClick}
              aria-hidden="true"
            />
            
            {/* Fullscreen Chat Container */}
            <div
              ref={chatContainerRef}
              className="fixed inset-0 z-50 flex flex-col bg-white animate-slide-up"
              style={{
                paddingTop: 'env(safe-area-inset-top)',
                paddingBottom: keyboardHeight > 0 ? `${keyboardHeight}px` : 'env(safe-area-inset-bottom)',
                height: keyboardHeight > 0 ? `calc(100vh - ${keyboardHeight}px)` : '100vh',
              }}
              role="dialog"
              aria-modal="true"
              aria-label="Chat with VERA"
            >
              {/* Header */}
              <div className="bg-mint text-white px-4 py-4 flex items-center gap-3 flex-shrink-0" style={{ minHeight: '64px' }}>
                <div className="w-11 h-11 rounded-full bg-white/20 flex items-center justify-center text-xl">
                  {VERA_AVATAR}
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-base">VERA</h3>
                  <p className="text-xs text-white/70">Briz-L Göz Klinikası</p>
                </div>
                <button
                  onClick={closeChat}
                  className="w-11 h-11 rounded-full hover:bg-white/10 flex items-center justify-center transition-colors"
                  aria-label="Close chat"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Messages */}
              <div 
                className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50/50"
                role="log"
                aria-live="polite"
                aria-label="Chat messages"
              >
                {/* Welcome message if no messages */}
                {messages.length === 0 && (
                  <div className="space-y-4">
                    <div className="flex gap-2">
                      <div className="w-9 h-9 rounded-full bg-mint/10 flex items-center justify-center text-base flex-shrink-0">
                        {VERA_AVATAR}
                      </div>
                      <div className="bg-white rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm max-w-[85%]">
                        <p className="text-[15px] leading-relaxed text-gray-700">
                          Salam! Mən VERA, Briz-L Göz Klinikasının virtual köməkçisiyəm. 👋 Sizə necə kömək edə bilərəm?
                        </p>
                      </div>
                    </div>
                    
                    {/* Quick Actions */}
                    <div className="flex flex-wrap gap-2 ml-11">
                      {quickActions.map((action) => (
                        <button
                          key={action.label}
                          onClick={() => sendMessage(action.message)}
                          disabled={isLoading}
                          className="px-4 py-2.5 text-sm rounded-full bg-mint/10 text-mint hover:bg-mint/20 transition-colors disabled:opacity-50 min-h-[44px]"
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
                      <div className="w-9 h-9 rounded-full bg-mint/10 flex items-center justify-center text-base flex-shrink-0">
                        {VERA_AVATAR}
                      </div>
                    )}
                    <div
                      className={`max-w-[85%] rounded-2xl px-4 py-3 shadow-sm ${
                        msg.type === 'user'
                          ? 'bg-mint text-white rounded-tr-sm'
                          : 'bg-white rounded-tl-sm'
                      }`}
                    >
                      <p className={`text-[15px] leading-relaxed ${msg.type === 'user' ? 'text-white' : 'text-gray-700'}`}>
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
                              className="px-4 py-2 text-sm rounded-full bg-mint/10 text-mint hover:bg-mint/20 transition-colors disabled:opacity-50 min-h-[44px]"
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
                    <div className="w-9 h-9 rounded-full bg-mint/10 flex items-center justify-center text-base flex-shrink-0">
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
              <div className="p-4 border-t border-gray-100 bg-white flex-shrink-0">
                <div className="flex gap-2">
                  <input
                    ref={inputRef}
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Mesajınızı yazın..."
                    disabled={isLoading}
                    className="flex-1 px-4 py-3 rounded-xl bg-gray-100 text-[15px] focus:outline-none focus:ring-2 focus:ring-mint/30 disabled:opacity-50 min-h-[48px]"
                    aria-label="Type your message"
                  />
                  <button
                    onClick={handleSend}
                    disabled={!input.trim() || isLoading}
                    className="w-12 h-12 rounded-xl bg-mint text-white flex items-center justify-center hover:bg-mint-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex-shrink-0"
                    aria-label="Send message"
                  >
                    <Send className="w-5 h-5" />
                  </button>
                </div>
                
                {/* WhatsApp fallback */}
                <a
                  href={clinicInfo.social.whatsapp}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block text-center text-xs text-gray-400 hover:text-mint mt-3 transition-colors"
                >
                  WhatsApp ilə əlaqə →
                </a>
              </div>
            </div>
          </>
        )}
      </AnimatePresence>

      {/* Chat Window - Desktop Popup */}
      <AnimatePresence>
        {isOpen && !isMobile && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            className="fixed bottom-24 right-6 z-50 w-[360px] max-w-[calc(100vw-48px)] h-[500px] max-h-[calc(100vh-150px)] rounded-2xl overflow-hidden shadow-2xl glass border border-mint/20 flex flex-col"
            role="dialog"
            aria-modal="true"
            aria-label="Chat with VERA"
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
                aria-label="Close chat"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Messages */}
            <div 
              className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50/50"
              role="log"
              aria-live="polite"
              aria-label="Chat messages"
            >
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
                  aria-label="Type your message"
                />
                <button
                  onClick={handleSend}
                  disabled={!input.trim() || isLoading}
                  className="w-10 h-10 rounded-xl bg-mint text-white flex items-center justify-center hover:bg-mint-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  aria-label="Send message"
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