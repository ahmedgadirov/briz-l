'use client'

import { motion, AnimatePresence } from 'framer-motion'
import { X, Send, Sparkles, Calendar, Users, Stethoscope, Phone, MapPin, Clock, ChevronRight, LucideIcon } from 'lucide-react'
import { useChat } from '@/hooks/useChat'
import { clinicInfo } from '@/lib/clinic-data'
import { useState, useRef, useEffect } from 'react'

// Quick action type definition
interface QuickAction {
  icon: LucideIcon
  label: string
  message: string
  gradient: string
  href?: string
  urgent?: boolean
}

// Custom VERA Avatar SVG Component
const VERAAvatar = ({ size = 40, className = '' }: { size?: number; className?: string }) => (
  <div 
    className={`relative flex items-center justify-center ${className}`}
    style={{ width: size, height: size }}
  >
    {/* Glow effect */}
    <div 
      className="absolute inset-0 rounded-full bg-gradient-to-br from-mint to-teal-600 opacity-20 blur-md"
      style={{ width: size * 1.2, height: size * 1.2 }}
    />
    {/* Avatar container */}
    <div className="relative w-full h-full rounded-full bg-gradient-to-br from-mint to-teal-600 flex items-center justify-center overflow-hidden">
      {/* Eye icon */}
      <svg 
        viewBox="0 0 24 24" 
        fill="none" 
        className="text-white"
        style={{ width: size * 0.5, height: size * 0.5 }}
      >
        <path 
          d="M2 12C2 12 5 5 12 5C19 5 22 12 22 12C22 12 19 19 12 19C5 19 2 12 2 12Z" 
          stroke="currentColor" 
          strokeWidth="2" 
          strokeLinecap="round" 
          strokeLinejoin="round"
        />
        <circle cx="12" cy="12" r="3" fill="currentColor" />
      </svg>
    </div>
  </div>
)

// Online status indicator
const OnlineIndicator = () => (
  <motion.div 
    className="absolute -bottom-0.5 -right-0.5 w-3.5 h-3.5 bg-green-500 rounded-full border-2 border-white"
    animate={{ scale: [1, 1.1, 1] }}
    transition={{ duration: 2, repeat: Infinity }}
  />
)

// Get time-based greeting
const getTimeBasedGreeting = () => {
  const hour = new Date().getHours()
  if (hour >= 5 && hour < 12) return { emoji: '🌅', text: 'Sabahınız xeyir!' }
  if (hour >= 12 && hour < 17) return { emoji: '☀️', text: 'Günortanız xeyir!' }
  if (hour >= 17 && hour < 21) return { emoji: '🌇', text: 'Axşamınız xeyir!' }
  return { emoji: '🌙', text: 'Gecəniz xeyir!' }
}

// Smart quick actions based on context
const getSmartQuickActions = (messages: Array<{ type: string; text: string }>): QuickAction[] => {
  const greeting = getTimeBasedGreeting()
  
  // Base actions
  const baseActions: QuickAction[] = [
    { 
      icon: Calendar, 
      label: 'Müayinəyə yazıl', 
      message: 'Müayinəyə yazılmaq istəyirəm',
      gradient: 'from-mint to-teal-600'
    },
    { 
      icon: Users, 
      label: 'Həkimlər', 
      message: 'Həkimlər haqqında məlumat ver',
      gradient: 'from-blue-500 to-indigo-600'
    },
    { 
      icon: Stethoscope, 
      label: 'Əməliyyatlar', 
      message: 'Əməliyyatlar haqqında məlumat ver',
      gradient: 'from-purple-500 to-pink-600'
    },
    { 
      icon: Phone, 
      label: 'Zəng et', 
      message: '',
      href: `tel:${clinicInfo.phone.main}`,
      gradient: 'from-orange-500 to-red-500'
    },
  ]

  // Check last messages for context
  const lastUserMessage = [...messages].reverse().find(m => m.type === 'user')
  
  if (lastUserMessage) {
    const text = lastUserMessage.text.toLowerCase()
    
    // Context: User mentioned pain or urgency
    if (text.includes('ağrı') || text.includes('problem') || text.includes('təcili')) {
      return [
        { 
          icon: Clock, 
          label: 'Təcili qəbul', 
          message: 'Təcili müayinəyə ehtiyacım var',
          gradient: 'from-red-500 to-orange-500',
          urgent: true
        },
        ...baseActions.slice(0, 2)
      ]
    }
    
    // Context: User asked about prices
    if (text.includes('qiymət') || text.includes('price') || text.includes('neçə')) {
      return [
        { 
          icon: Sparkles, 
          label: 'Qiymət siyahısı', 
          message: 'Qiymətlər haqqında məlumat ver',
          gradient: 'from-amber-500 to-orange-500'
        },
        ...baseActions.slice(0, 2)
      ]
    }
  }

  return baseActions
}

// Message timestamp component
const MessageTime = ({ timestamp }: { timestamp?: Date }) => {
  if (!timestamp) return null
  const time = timestamp.toLocaleTimeString('az-AZ', { hour: '2-digit', minute: '2-digit' })
  return (
    <span className="text-[10px] text-gray-400 mt-1 block">
      {time}
    </span>
  )
}

// Typing indicator with wave animation
const TypingIndicator = () => (
  <div className="flex gap-1 items-center h-5">
    {[0, 1, 2].map((i) => (
      <motion.div
        key={i}
        className="w-2 h-2 rounded-full bg-mint"
        animate={{ y: [-2, 2, -2], opacity: [0.5, 1, 0.5] }}
        transition={{ 
          duration: 0.8, 
          repeat: Infinity, 
          delay: i * 0.15,
          ease: 'easeInOut'
        }}
      />
    ))}
  </div>
)

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
  const [showTooltip, setShowTooltip] = useState(true)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)
  const chatContainerRef = useRef<HTMLDivElement>(null)

  // Get smart actions based on conversation
  const quickActions = getSmartQuickActions(messages)
  const greeting = getTimeBasedGreeting()

  // Mobile detection
  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth < 640)
    checkMobile()
    window.addEventListener('resize', checkMobile)
    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  // Hide tooltip after first interaction
  useEffect(() => {
    if (isOpen) setShowTooltip(false)
  }, [isOpen])

  // Keyboard handler for mobile
  useEffect(() => {
    if (!isOpen || !isMobile) return
    const handleResize = () => {
      if (window.visualViewport) {
        const kbHeight = window.innerHeight - window.visualViewport.height
        setKeyboardHeight(kbHeight > 100 ? kbHeight : 0)
        if (kbHeight > 100) {
          setTimeout(() => inputRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 100)
        }
      }
    }
    window.visualViewport?.addEventListener('resize', handleResize)
    return () => window.visualViewport?.removeEventListener('resize', handleResize)
  }, [isOpen, isMobile])

  // Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Focus input
  useEffect(() => {
    if (isOpen) setTimeout(() => inputRef.current?.focus(), 100)
  }, [isOpen])

  // Prevent body scroll on mobile
  useEffect(() => {
    if (isOpen && isMobile) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }
    return () => { document.body.style.overflow = '' }
  }, [isOpen, isMobile])

  // Escape key handler
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) closeChat()
    }
    window.addEventListener('keydown', handleEscape)
    return () => window.removeEventListener('keydown', handleEscape)
  }, [isOpen, closeChat])

  const handleSend = async () => {
    if (!input.trim() || isLoading) return
    const message = input.trim()
    setInput('')
    await sendMessage(message)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleButtonClick = async (payload: string) => {
    await sendMessage(payload)
  }

  const handleActionClick = (action: { message: string; href?: string }) => {
    if (action.href) {
      window.open(action.href, '_blank')
    } else if (action.message) {
      sendMessage(action.message)
    }
  }

  return (
    <>
      {/* Floating Button */}
      <motion.button
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ delay: 1, type: 'spring', stiffness: 200 }}
        onClick={toggleChat}
        className="fixed z-50 rounded-2xl shadow-2xl transition-all duration-300 group"
        style={{
          width: isMobile ? '60px' : '64px',
          height: isMobile ? '60px' : '64px',
          bottom: `calc(1.5rem + env(safe-area-inset-bottom))`,
          right: `calc(1rem + env(safe-area-inset-right))`,
        }}
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
        aria-expanded={isOpen}
      >
        {/* Glass background */}
        <div className="absolute inset-0 rounded-2xl bg-white/80 backdrop-blur-xl border border-mint/20 shadow-lg" />
        
        {/* Gradient overlay on hover */}
        <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-mint to-teal-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        
        {/* Content */}
        <div className="relative z-10 flex items-center justify-center h-full">
          <AnimatePresence mode="wait">
            {isOpen ? (
              <motion.div
                key="close"
                initial={{ rotate: -90, opacity: 0 }}
                animate={{ rotate: 0, opacity: 1 }}
                exit={{ rotate: 90, opacity: 0 }}
                className="text-mint group-hover:text-white transition-colors"
              >
                <X className="w-6 h-6" />
              </motion.div>
            ) : (
              <motion.div
                key="chat"
                initial={{ rotate: 90, opacity: 0 }}
                animate={{ rotate: 0, opacity: 1 }}
                exit={{ rotate: -90, opacity: 0 }}
                className="text-mint group-hover:text-white transition-colors"
              >
                <Sparkles className="w-6 h-6" />
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Pulse ring animation */}
        {!isOpen && (
          <motion.div
            className="absolute inset-0 rounded-2xl border-2 border-mint/50"
            animate={{ scale: [1, 1.15, 1], opacity: [0.5, 0, 0.5] }}
            transition={{ duration: 2, repeat: Infinity }}
          />
        )}

        {/* Tooltip */}
        {showTooltip && !isOpen && (
          <motion.div
            initial={{ opacity: 0, x: 10 }}
            animate={{ opacity: 1, x: 0 }}
            className="absolute right-full mr-3 top-1/2 -translate-y-1/2 whitespace-nowrap"
          >
            <div className="bg-white/90 backdrop-blur-lg px-4 py-2 rounded-xl shadow-lg border border-mint/10">
              <p className="text-sm font-medium text-gray-800">VERA ilə söhbət et</p>
              <p className="text-xs text-gray-500">Sualınız var? 👋</p>
            </div>
          </motion.div>
        )}
      </motion.button>

      {/* Chat Window - Mobile Fullscreen */}
      <AnimatePresence>
        {isOpen && isMobile && (
          <motion.div
            ref={chatContainerRef}
            initial={{ y: '100%' }}
            animate={{ y: 0 }}
            exit={{ y: '100%' }}
            transition={{ type: 'spring', damping: 30, stiffness: 300 }}
            className="fixed inset-0 z-50 flex flex-col bg-gradient-to-b from-gray-50 to-white"
            style={{
              paddingBottom: keyboardHeight > 0 ? `${keyboardHeight}px` : 'env(safe-area-inset-bottom)',
              height: keyboardHeight > 0 ? `calc(100vh - ${keyboardHeight}px)` : '100vh',
            }}
            role="dialog"
            aria-modal="true"
            aria-label="Chat with VERA"
          >
            {/* Header */}
            <div className="relative overflow-hidden">
              {/* Gradient background */}
              <div className="absolute inset-0 bg-gradient-to-r from-mint via-teal-600 to-mint" />
              
              {/* Animated gradient overlay */}
              <motion.div
                className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent"
                animate={{ x: ['-100%', '100%'] }}
                transition={{ duration: 3, repeat: Infinity, repeatDelay: 2 }}
              />
              
              <div className="relative px-4 py-4 flex items-center gap-3">
                {/* Avatar with status */}
                <div className="relative">
                  <VERAAvatar size={48} />
                  <OnlineIndicator />
                </div>
                
                <div className="flex-1">
                  <h3 className="font-semibold text-lg text-white tracking-wide">VERA</h3>
                  <div className="flex items-center gap-1.5">
                    <motion.span
                      animate={{ opacity: [0.7, 1, 0.7] }}
                      transition={{ duration: 2, repeat: Infinity }}
                      className="text-xs text-white/80"
                    >
                      Hər zaman buradayam • Briz-L
                    </motion.span>
                  </div>
                </div>
                
                <button
                  onClick={closeChat}
                  className="w-10 h-10 rounded-xl bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors backdrop-blur-sm"
                  aria-label="Close chat"
                >
                  <X className="w-5 h-5 text-white" />
                </button>
              </div>
            </div>

            {/* Messages */}
            <div 
              className="flex-1 overflow-y-auto p-4 space-y-4"
              role="log"
              aria-live="polite"
            >
              {/* Welcome message */}
              {messages.length === 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="space-y-4"
                >
                  {/* Greeting card */}
                  <div className="flex gap-3">
                    <VERAAvatar size={36} />
                    <div className="flex-1">
                      <div className="bg-white rounded-2xl rounded-tl-lg px-4 py-3 shadow-sm border border-gray-100">
                        <p className="text-[15px] text-gray-700 leading-relaxed">
                          {greeting.emoji} {greeting.text}<br />
                          Mən VERA, Briz-L Göz Klinikasının virtual köməkçisiyəm. Sizə necə kömək edə bilərəm?
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Quick Actions */}
                  <div className="flex flex-wrap gap-2 ml-12">
                    {quickActions.map((action, idx) => {
                      const Icon = action.icon
                      return (
                        <motion.button
                          key={action.label}
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: idx * 0.1 }}
                          onClick={() => handleActionClick(action)}
                          disabled={isLoading}
                          className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 disabled:opacity-50 min-h-[44px] ${
                            action.urgent 
                              ? 'bg-gradient-to-r from-red-500 to-orange-500 text-white shadow-lg shadow-red-500/25' 
                              : 'bg-white border border-gray-200 text-gray-700 hover:border-mint/40 hover:shadow-md'
                          }`}
                        >
                          <Icon className="w-4 h-4" />
                          {action.label}
                        </motion.button>
                      )
                    })}
                  </div>
                </motion.div>
              )}

              {/* Message list */}
              {messages.map((msg, idx) => (
                <motion.div
                  key={msg.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.05 }}
                  className={`flex gap-2 ${msg.type === 'user' ? 'justify-end' : ''}`}
                >
                  {msg.type === 'bot' && <VERAAvatar size={32} />}
                  
                  <div className={`max-w-[85%] ${msg.type === 'user' ? 'order-first' : ''}`}>
                    <div
                      className={`px-4 py-3 ${
                        msg.type === 'user'
                          ? 'bg-gradient-to-br from-mint to-teal-600 text-white rounded-2xl rounded-tr-lg shadow-lg shadow-mint/20'
                          : 'bg-white rounded-2xl rounded-tl-lg shadow-sm border border-gray-100'
                      }`}
                    >
                      <p className={`text-[15px] leading-relaxed ${msg.type === 'user' ? 'text-white' : 'text-gray-700'}`}>
                        {msg.text}
                      </p>
                      
                      {/* Buttons */}
                      {msg.buttons && msg.buttons.length > 0 && (
                        <div className="flex flex-wrap gap-2 mt-3">
                          {msg.buttons.map((btn, btnIdx) => (
                            <motion.button
                              key={btnIdx}
                              whileHover={{ scale: 1.02 }}
                              whileTap={{ scale: 0.98 }}
                              onClick={() => handleButtonClick(btn.payload)}
                              disabled={isLoading}
                              className="px-4 py-2 text-sm rounded-xl bg-mint/10 text-mint hover:bg-mint/20 transition-colors disabled:opacity-50 min-h-[40px] font-medium"
                            >
                              {btn.title}
                            </motion.button>
                          ))}
                        </div>
                      )}
                    </div>
                    <MessageTime timestamp={msg.timestamp} />
                  </div>
                </motion.div>
              ))}

              {/* Typing indicator */}
              {isLoading && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex gap-2 items-end"
                >
                  <VERAAvatar size={32} />
                  <div className="bg-white rounded-2xl rounded-tl-lg px-4 py-3 shadow-sm border border-gray-100">
                    <TypingIndicator />
                  </div>
                </motion.div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Quick Actions Bar */}
            {messages.length > 0 && (
              <div className="px-4 py-2 border-t border-gray-100 bg-white/80 backdrop-blur-sm overflow-x-auto">
                <div className="flex gap-2">
                  {quickActions.slice(0, 3).map((action) => {
                    const Icon = action.icon
                    return (
                      <button
                        key={action.label}
                        onClick={() => handleActionClick(action)}
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gray-100 text-gray-600 text-xs font-medium whitespace-nowrap hover:bg-mint/10 hover:text-mint transition-colors"
                      >
                        <Icon className="w-3.5 h-3.5" />
                        {action.label}
                      </button>
                    )
                  })}
                </div>
              </div>
            )}

            {/* Input */}
            <div className="p-4 border-t border-gray-100 bg-white">
              <div className="flex gap-2">
                <div className="flex-1 relative">
                  <input
                    ref={inputRef}
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Mesajınızı yazın..."
                    disabled={isLoading}
                    className="w-full px-4 py-3 rounded-xl bg-gray-100 text-[15px] focus:outline-none focus:ring-2 focus:ring-mint/30 focus:bg-white transition-all disabled:opacity-50 min-h-[48px] pr-10"
                    aria-label="Type your message"
                  />
                  {/* Character hint */}
                  {input.length > 0 && (
                    <span className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-gray-400">
                      {input.length}/500
                    </span>
                  )}
                </div>
                
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleSend}
                  disabled={!input.trim() || isLoading}
                  className="w-12 h-12 rounded-xl bg-gradient-to-br from-mint to-teal-600 text-white flex items-center justify-center shadow-lg shadow-mint/30 disabled:opacity-40 disabled:shadow-none transition-all flex-shrink-0"
                  aria-label="Send message"
                >
                  <Send className="w-5 h-5" />
                </motion.button>
              </div>
              
              {/* WhatsApp fallback */}
              <a
                href={clinicInfo.social.whatsapp}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-center gap-2 text-xs text-gray-400 hover:text-green-600 mt-3 transition-colors"
              >
                <Phone className="w-3.5 h-3.5" />
                WhatsApp ilə əlaqə
                <ChevronRight className="w-3 h-3" />
              </a>
            </div>
          </motion.div>
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
            className="fixed bottom-24 right-6 z-50 w-[380px] max-w-[calc(100vw-48px)] h-[550px] max-h-[calc(100vh-150px)] rounded-2xl overflow-hidden shadow-2xl flex flex-col"
            role="dialog"
            aria-modal="true"
            aria-label="Chat with VERA"
          >
            {/* Glass background */}
            <div className="absolute inset-0 bg-white/90 backdrop-blur-xl" />
            <div className="absolute inset-0 border border-mint/10 rounded-2xl" />
            
            {/* Content */}
            <div className="relative flex flex-col h-full">
              {/* Header */}
              <div className="relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-r from-mint via-teal-600 to-mint" />
                <motion.div
                  className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent"
                  animate={{ x: ['-100%', '100%'] }}
                  transition={{ duration: 3, repeat: Infinity, repeatDelay: 2 }}
                />
                
                <div className="relative px-4 py-3 flex items-center gap-3">
                  <div className="relative">
                    <VERAAvatar size={42} />
                    <OnlineIndicator />
                  </div>
                  
                  <div className="flex-1">
                    <h3 className="font-semibold text-white">VERA</h3>
                    <span className="text-xs text-white/80">Briz-L Göz Klinikası</span>
                  </div>
                  
                  <button
                    onClick={closeChat}
                    className="w-8 h-8 rounded-lg bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors"
                    aria-label="Close chat"
                  >
                    <X className="w-4 h-4 text-white" />
                  </button>
                </div>
              </div>

              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-transparent">
                {messages.length === 0 && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="space-y-3"
                  >
                    <div className="flex gap-2">
                      <VERAAvatar size={30} />
                      <div className="bg-white/80 backdrop-blur-sm rounded-2xl rounded-tl-lg px-3 py-2.5 shadow-sm border border-gray-100 max-w-[80%]">
                        <p className="text-sm text-gray-700 leading-relaxed">
                          {greeting.emoji} {greeting.text}<br />
                          Mən VERA, Briz-L Göz Klinikasının virtual köməkçisiyəm. Sizə necə kömək edə bilərəm?
                        </p>
                      </div>
                    </div>

                    <div className="flex flex-wrap gap-2 ml-9">
                      {quickActions.map((action, idx) => {
                        const Icon = action.icon
                        return (
                          <motion.button
                            key={action.label}
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: idx * 0.05 }}
                            onClick={() => handleActionClick(action)}
                            disabled={isLoading}
                            className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all disabled:opacity-50 ${
                              action.urgent
                                ? 'bg-gradient-to-r from-red-500 to-orange-500 text-white'
                                : 'bg-white/80 backdrop-blur-sm border border-gray-200 text-gray-700 hover:border-mint/40'
                            }`}
                          >
                            <Icon className="w-3.5 h-3.5" />
                            {action.label}
                          </motion.button>
                        )
                      })}
                    </div>
                  </motion.div>
                )}

                {messages.map((msg, idx) => (
                  <motion.div
                    key={msg.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: idx * 0.03 }}
                    className={`flex gap-2 ${msg.type === 'user' ? 'justify-end' : ''}`}
                  >
                    {msg.type === 'bot' && <VERAAvatar size={26} />}
                    
                    <div className={`max-w-[80%] ${msg.type === 'user' ? 'order-first' : ''}`}>
                      <div
                        className={`px-3 py-2 ${
                          msg.type === 'user'
                            ? 'bg-gradient-to-br from-mint to-teal-600 text-white rounded-xl rounded-tr-sm shadow-md shadow-mint/20'
                            : 'bg-white/80 backdrop-blur-sm rounded-xl rounded-tl-sm shadow-sm border border-gray-100'
                        }`}
                      >
                        <p className={`text-sm leading-relaxed ${msg.type === 'user' ? 'text-white' : 'text-gray-700'}`}>
                          {msg.text}
                        </p>
                        
                        {msg.buttons && msg.buttons.length > 0 && (
                          <div className="flex flex-wrap gap-2 mt-2">
                            {msg.buttons.map((btn, btnIdx) => (
                              <button
                                key={btnIdx}
                                onClick={() => handleButtonClick(btn.payload)}
                                disabled={isLoading}
                                className="px-3 py-1 text-xs rounded-lg bg-mint/10 text-mint hover:bg-mint/20 transition-colors disabled:opacity-50 font-medium"
                              >
                                {btn.title}
                              </button>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  </motion.div>
                ))}

                {isLoading && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="flex gap-2 items-end"
                  >
                    <VERAAvatar size={26} />
                    <div className="bg-white/80 backdrop-blur-sm rounded-xl rounded-tl-sm px-3 py-2 shadow-sm border border-gray-100">
                      <TypingIndicator />
                    </div>
                  </motion.div>
                )}

                <div ref={messagesEndRef} />
              </div>

              {/* Quick Actions Bar */}
              {messages.length > 0 && (
                <div className="px-3 py-2 border-t border-gray-100 bg-white/50 overflow-x-auto">
                  <div className="flex gap-1.5">
                    {quickActions.slice(0, 3).map((action) => {
                      const Icon = action.icon
                      return (
                        <button
                          key={action.label}
                          onClick={() => handleActionClick(action)}
                          className="flex items-center gap-1 px-2.5 py-1 rounded-md bg-gray-100/80 text-gray-600 text-xs font-medium whitespace-nowrap hover:bg-mint/10 hover:text-mint transition-colors"
                        >
                          <Icon className="w-3 h-3" />
                          {action.label}
                        </button>
                      )
                    })}
                  </div>
                </div>
              )}

              {/* Input */}
              <div className="p-3 border-t border-gray-100 bg-white/50">
                <div className="flex gap-2">
                  <input
                    ref={inputRef}
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Mesajınızı yazın..."
                    disabled={isLoading}
                    className="flex-1 px-3 py-2.5 rounded-xl bg-white border border-gray-200 text-sm focus:outline-none focus:border-mint/40 focus:ring-2 focus:ring-mint/10 transition-all disabled:opacity-50"
                    aria-label="Type your message"
                  />
                  
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleSend}
                    disabled={!input.trim() || isLoading}
                    className="w-10 h-10 rounded-xl bg-gradient-to-br from-mint to-teal-600 text-white flex items-center justify-center shadow-md shadow-mint/20 disabled:opacity-40 disabled:shadow-none transition-all"
                    aria-label="Send message"
                  >
                    <Send className="w-4 h-4" />
                  </motion.button>
                </div>
                
                <a
                  href={clinicInfo.social.whatsapp}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center justify-center gap-1.5 text-xs text-gray-400 hover:text-green-600 mt-2 transition-colors"
                >
                  <Phone className="w-3 h-3" />
                  WhatsApp ilə əlaqə
                  <ChevronRight className="w-3 h-3" />
                </a>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}