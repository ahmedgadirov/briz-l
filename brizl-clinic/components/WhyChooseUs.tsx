'use client'

import { motion } from 'framer-motion'
import { Award, Users, Clock, Shield } from 'lucide-react'
import { useTranslations } from 'next-intl'

const iconMap = [Award, Users, Clock, Shield]
const itemKeys = ['experience', 'technology', 'operations', 'satisfaction']

export default function WhyChooseUs() {
  const t = useTranslations('whyChooseUs')

  return (
    <section className="py-24 px-6">
      <div className="max-w-5xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h2 className="font-display text-2xl md:text-3xl font-semibold text-gray-800 mb-4">
            {t('title')}
          </h2>
          <p className="text-gray-500 max-w-xl mx-auto">
            {t('subtitle')}
          </p>
        </motion.div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {itemKeys.map((key, index) => {
            const Icon = iconMap[index] || Award
            return (
              <motion.div
                key={key}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="glass p-6 text-center group hover:border-mint/30 transition-all duration-300"
              >
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-mint/10 mb-4 group-hover:bg-mint/20 transition-colors">
                  <Icon className="w-6 h-6 text-mint" />
                </div>
                <h3 className="font-display font-semibold text-gray-800 mb-1">{t(`items.${key}.title`)}</h3>
                <p className="text-2xl font-bold text-mint mb-1">{t(`items.${key}.stat`)}</p>
                <p className="text-xs text-gray-500">{t(`items.${key}.statLabel`)}</p>
              </motion.div>
            )
          })}
        </div>
      </div>
    </section>
  )
}