'use client'

import { motion } from 'framer-motion'
import { ArrowDown, Phone, MapPin, Users, Briefcase, MessageCircle } from 'lucide-react'
import { clinicInfo } from '@/lib/clinic-data'
import { useChat } from '@/hooks/useChat'
import { useTranslations, useLocale } from 'next-intl'
import LanguageSwitcher from './LanguageSwitcher'

export default function Hero() {
  const { openChat } = useChat()
  const t = useTranslations('nav')
  const tHero = useTranslations('hero')
  const locale = useLocale()
  
  const navItems = [
    { name: t('doctors'), href: '#doctors', icon: Users },
    { name: t('services'), href: '#services', icon: Briefcase },
    { name: t('vera'), href: '#vera', icon: MessageCircle, isChat: true },
    { name: t('location'), href: '#location', icon: MapPin },
  ]

  return (
    <section className="min-h-screen flex flex-col items-center justify-center px-6 py-20">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-center max-w-4xl"
      >
        {/* Language Switcher */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="flex justify-center mb-8"
        >
          <LanguageSwitcher />
        </motion.div>

        {/* Brand line */}
        <h1 className="font-display text-4xl md:text-6xl lg:text-7xl font-medium tracking-tight mb-8 leading-tight">
          <span className="gradient-text">{clinicInfo.name}</span>{' '}
          {tHero('title', { name: '' })}
        </h1>

        <p className="text-gray-600 text-lg md:text-xl max-w-2xl mx-auto mb-8">
          {tHero('subtitle')}
        </p>

        {/* Navigation Pills */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="flex flex-wrap items-center justify-center gap-3 mt-8"
        >
          {navItems.map((item, index) => {
            const Icon = item.icon
            return item.isChat ? (
              <motion.button
                key={item.name}
                onClick={openChat}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: 0.4 + index * 0.1 }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.98 }}
                className="px-6 py-3 rounded-full glass border border-mint/30 text-mint font-medium text-sm md:text-base hover:border-mint/60 transition-all duration-300 inline-flex items-center gap-2"
              >
                <Icon className="w-4 h-4" />
                {item.name}
              </motion.button>
            ) : (
              <motion.a
                key={item.name}
                href={item.href}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: 0.4 + index * 0.1 }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.98 }}
                className="px-6 py-3 rounded-full glass border border-mint/30 text-mint font-medium text-sm md:text-base hover:border-mint/60 transition-all duration-300 inline-flex items-center gap-2"
              >
                <Icon className="w-4 h-4" />
                {item.name}
              </motion.a>
            )
          })}
        </motion.div>

        {/* Contact buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="flex flex-wrap items-center justify-center gap-4 mt-10"
        >
          <a
            href={`tel:${clinicInfo.phone.main}`}
            className="inline-flex items-center gap-2 px-6 py-3 bg-mint text-white rounded-xl font-medium hover:bg-mint-dark transition-colors"
          >
            <Phone className="w-4 h-4" />
            {clinicInfo.phone.main}
          </a>
          <a
            href={clinicInfo.maps.google}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-6 py-3 glass border border-gray-200 text-gray-700 rounded-xl font-medium hover:border-mint/40 transition-colors"
          >
            <MapPin className="w-4 h-4" />
            {clinicInfo.address.full}
          </a>
        </motion.div>

        {/* Scroll indicator */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 1 }}
          className="mt-16"
        >
          <motion.a
            href="#services"
            animate={{ y: [0, 8, 0] }}
            transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
            className="inline-flex flex-col items-center text-gray-400 hover:text-mint transition-colors"
          >
            <span className="text-xs mb-2 uppercase tracking-widest">{tHero('scrollToServices')}</span>
            <ArrowDown className="w-5 h-5" />
          </motion.a>
        </motion.div>
      </motion.div>
    </section>
  )
}