'use client'

import { motion } from 'framer-motion'
import { ArrowRight, MessageCircle } from 'lucide-react'
import { clinicInfo } from '@/lib/clinic-data'
import { useChat } from '@/hooks/useChat'
import { useTranslations } from 'next-intl'

// Map surgery IDs to icons
const iconMap: Record<string, string> = {
  excimer: '🔬',
  cataract: '👁️',
  pteregium: '🔧',
  phacic: '💎',
  cesplik: '⚡',
  cross_linking: '🔗',
  argon: '💚',
  yag: '✨',
  avastin: '💉',
  glaucoma: '🩺',
}

// Surgery IDs for iteration
const surgeryIds = ['excimer', 'cataract', 'pteregium', 'phacic', 'cesplik', 'cross_linking', 'argon', 'yag', 'avastin', 'glaucoma']

export default function Services() {
  const { openChat, sendSurgeryQuery } = useChat()
  const t = useTranslations('services')

  const handleMoreInfo = (surgeryId: string) => {
    openChat()
    setTimeout(() => {
      sendSurgeryQuery(surgeryId)
    }, 300)
  }

  return (
    <section id="services" className="py-24 px-6">
      <div className="max-w-7xl mx-auto">
        {/* Section header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="font-display text-3xl md:text-4xl font-semibold text-gray-800 mb-4">
            {t('title')}
          </h2>
          <p className="text-gray-500 text-lg max-w-2xl mx-auto">
            {t('subtitle')}
          </p>
        </motion.div>

        {/* Services grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8">
          {surgeryIds.map((surgeryId, index) => (
            <motion.div
              key={surgeryId}
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="card-glow glass p-8 md:p-10 border border-mint/20 hover:border-mint/40 transition-all duration-500 group"
            >
              {/* Icon */}
              <div className="inline-flex items-center justify-center w-14 h-14 rounded-xl bg-mint/10 mb-6 group-hover:bg-mint/20 transition-colors text-3xl">
                {iconMap[surgeryId] || '🏥'}
              </div>

              {/* Header */}
              <h3 className="font-display text-xl md:text-2xl font-semibold text-gray-800 mb-3">
                {t(`items.${surgeryId}.name`)}
              </h3>

              {/* Description */}
              <p className="text-gray-600 text-base leading-relaxed mb-6">
                {t(`items.${surgeryId}.description`)}
              </p>

              {/* Features */}
              <ul className="space-y-3 mb-8">
                {[0, 1, 2].map((i) => (
                  <li key={i} className="flex items-center gap-3 text-gray-500 text-sm">
                    <span className="w-1.5 h-1.5 rounded-full bg-mint" />
                    {t(`items.${surgeryId}.features.${i}`)}
                  </li>
                ))}
              </ul>

              {/* CTA Buttons */}
              <div className="flex flex-wrap gap-3">
                <motion.a
                  href={`tel:${clinicInfo.phone.main}`}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="inline-flex items-center gap-2 text-mint bg-mint/10 px-5 py-3 rounded-xl font-medium text-sm transition-all duration-300 hover:bg-mint/20"
                >
                  {t('bookAppointment')}
                  <ArrowRight className="w-4 h-4 opacity-60 group-hover:opacity-100 transition-opacity" />
                </motion.a>
                <motion.button
                  onClick={() => handleMoreInfo(surgeryId)}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="inline-flex items-center gap-2 text-gray-600 bg-gray-100 px-5 py-3 rounded-xl font-medium text-sm transition-all duration-300 hover:bg-gray-200"
                >
                  <MessageCircle className="w-4 h-4" />
                  {t('moreInfo')}
                </motion.button>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}