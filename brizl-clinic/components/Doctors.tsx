'use client'

import { motion } from 'framer-motion'
import { Phone, MessageCircle, User, Bot } from 'lucide-react'
import { useChat } from '@/hooks/useChat'
import { useTranslations } from 'next-intl'

// Doctor IDs for iteration
const doctorIds = ['iltifat', 'emil', 'sabina', 'seymur']

// Doctor contact info (static data)
const doctorContacts: Record<string, { phone: string; whatsapp: string }> = {
  iltifat: { phone: '010 710 74 65', whatsapp: 'https://wa.me/994107107465' },
  emil: { phone: '051 844 76 21', whatsapp: 'https://wa.me/994518447621' },
  sabina: { phone: '055 319 75 76', whatsapp: 'https://wa.me/994553197576' },
  seymur: { phone: '070 505 00 01', whatsapp: 'https://wa.me/994705050001' },
}

export default function Doctors() {
  const { openChat, sendDoctorQuery } = useChat()
  const t = useTranslations('doctors')

  const handleAskAboutDoctor = (doctorId: string) => {
    openChat()
    setTimeout(() => {
      sendDoctorQuery(doctorId)
    }, 300)
  }

  return (
    <section id="doctors" className="py-24 px-6 bg-gradient-to-b from-transparent via-mint/5 to-transparent">
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

        {/* Doctors grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {doctorIds.map((doctorId, index) => {
            const contact = doctorContacts[doctorId]
            return (
              <motion.div
                key={doctorId}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="card-glow glass p-6 border border-mint/20 hover:border-mint/40 transition-all duration-500 group text-center"
              >
                {/* Avatar placeholder */}
                <div className="w-24 h-24 mx-auto mb-4 rounded-full bg-gradient-to-br from-mint/20 to-mint/40 flex items-center justify-center group-hover:from-mint/30 group-hover:to-mint/50 transition-all duration-300">
                  <User className="w-10 h-10 text-mint" />
                </div>

                {/* Name */}
                <h3 className="font-display text-xl font-semibold text-gray-800 mb-1">
                  {t(`items.${doctorId}.name`)}
                </h3>

                {/* Title */}
                <p className="text-mint text-sm font-medium mb-3">
                  {t(`items.${doctorId}.title`)}
                </p>

                {/* Description */}
                <p className="text-gray-500 text-sm mb-4 leading-relaxed">
                  {t(`items.${doctorId}.description`)}
                </p>

                {/* Contact buttons */}
                <div className="flex flex-wrap items-center justify-center gap-2">
                  <motion.a
                    href={`tel:${contact.phone.replace(/\s/g, '')}`}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="inline-flex items-center gap-1.5 px-3 py-2 bg-mint/10 hover:bg-mint/20 text-mint rounded-lg text-sm font-medium transition-colors"
                  >
                    <Phone className="w-4 h-4" />
                    {t('call')}
                  </motion.a>
                  <motion.a
                    href={contact.whatsapp}
                    target="_blank"
                    rel="noopener noreferrer"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="inline-flex items-center gap-1.5 px-3 py-2 bg-green-500/10 hover:bg-green-500/20 text-green-600 rounded-lg text-sm font-medium transition-colors"
                  >
                    <MessageCircle className="w-4 h-4" />
                    {t('whatsapp')}
                  </motion.a>
                  <motion.button
                    onClick={() => handleAskAboutDoctor(doctorId)}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="inline-flex items-center gap-1.5 px-3 py-2 bg-gray-100 hover:bg-gray-200 text-gray-600 rounded-lg text-sm font-medium transition-colors"
                  >
                    <Bot className="w-4 h-4" />
                    {t('vera')}
                  </motion.button>
                </div>
              </motion.div>
            )
          })}
        </div>
      </div>
    </section>
  )
}