'use client'

import { motion } from 'framer-motion'
import { Eye, Sparkles, Heart, ArrowRight } from 'lucide-react'

const services = [
  {
    name: 'Katarakta əməliyyatı',
    description: 'Müasir metodlarla katarakta əməliyyatı. Süni lens yerləşdirilməsi ilə görmə qabiliyyətinin bərpası.',
    features: [
      'Fako əməliyyat üsulu',
      'Süni lens implantasiyası',
      'Qısa bərpa dövrü',
    ],
    icon: Eye,
  },
  {
    name: 'Excimer Laser',
    description: 'Lazer korreksiya ilə görmə qabiliyyətinin bərpası. Eynək və linzalardan xilas olun.',
    features: [
      'LASIK üsulu',
      'Həssas korreksiya',
      'Sürətli bərpa',
    ],
    icon: Sparkles,
  },
  {
    name: 'Qlaukoma müalicəsi',
    description: 'Qlaukoma diaqnostikası və müalicəsi. Gözdaxili təzyiqin normallaşdırılması.',
    features: [
      'Erkən diaqnostika',
      'Lazer müalicəsi',
      'Cərrahi müdaxilə',
    ],
    icon: Heart,
  },
]

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
          {services.map((service, index) => (
            <motion.div
              key={service.name}
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.15 }}
              className="card-glow glass p-8 md:p-10 border border-mint/20 hover:border-mint/40 transition-all duration-500 group"
            >
              {/* Icon */}
              <div className="inline-flex items-center justify-center w-14 h-14 rounded-xl bg-mint/10 mb-6 group-hover:bg-mint/20 transition-colors">
                <service.icon className="w-7 h-7 text-mint" />
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
                href="tel:+994502222222"
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