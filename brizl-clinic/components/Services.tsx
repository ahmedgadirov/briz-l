'use client'

import { motion } from 'framer-motion'
import { ArrowRight } from 'lucide-react'
import { surgeries, clinicInfo } from '@/lib/clinic-data'

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

export default function Services() {
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
            Xidmətlərimiz
          </h2>
          <p className="text-gray-500 text-lg max-w-2xl mx-auto">
            Müasir oftalmologiya sahəsində ən son texnologiyalar və üsullarla xidmət göstəririk.
          </p>
        </motion.div>

        {/* Services grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8">
          {surgeries.map((service, index) => (
            <motion.div
              key={service.id}
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="card-glow glass p-8 md:p-10 border border-mint/20 hover:border-mint/40 transition-all duration-500 group"
            >
              {/* Icon */}
              <div className="inline-flex items-center justify-center w-14 h-14 rounded-xl bg-mint/10 mb-6 group-hover:bg-mint/20 transition-colors text-3xl">
                {iconMap[service.id] || '🏥'}
              </div>

              {/* Header */}
              <h3 className="font-display text-xl md:text-2xl font-semibold text-gray-800 mb-3">
                {service.name}
              </h3>

              {/* Description */}
              <p className="text-gray-600 text-base leading-relaxed mb-6">
                {service.description}
              </p>

              {/* Features */}
              <ul className="space-y-3 mb-8">
                {service.features.map((feature, i) => (
                  <li key={i} className="flex items-center gap-3 text-gray-500 text-sm">
                    <span className="w-1.5 h-1.5 rounded-full bg-mint" />
                    {feature}
                  </li>
                ))}
              </ul>

              {/* CTA */}
              <motion.a
                href={`tel:${clinicInfo.phone.main}`}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="inline-flex items-center gap-2 text-mint bg-mint/10 px-5 py-3 rounded-xl font-medium text-sm transition-all duration-300 hover:bg-mint/20"
              >
                Randevu al
                <ArrowRight className="w-4 h-4 opacity-60 group-hover:opacity-100 transition-opacity" />
              </motion.a>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
