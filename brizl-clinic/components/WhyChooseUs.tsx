'use client'

import { motion } from 'framer-motion'
import { Award, Users, Clock, Shield } from 'lucide-react'

const principles = [
  { icon: Award, label: 'Təcrübə', description: '15+ illik təcrübə' },
  { icon: Users, label: 'Pasientlər', description: '10000+ uğurlu əməliyyat' },
  { icon: Clock, label: 'Sürət', description: 'Qısa bərpa dövrü' },
  { icon: Shield, label: 'Təhlükəsizlik', description: 'Müasir avadanlıqlar' },
]

export default function WhyChooseUs() {
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
            Niyə bizi seçməlisiniz?
          </h2>
          <p className="text-gray-500 max-w-xl mx-auto">
            Hər bir pasientimizə fərdi yanaşma və ən yüksək keyfiyyətli xidmət göstəririk.
          </p>
        </motion.div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {principles.map((principle, index) => (
            <motion.div
              key={principle.label}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="glass p-6 text-center group hover:border-mint/30 transition-all duration-300"
            >
              <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-mint/10 mb-4 group-hover:bg-mint/20 transition-colors">
                <principle.icon className="w-6 h-6 text-mint" />
              </div>
              <h3 className="font-display font-semibold text-gray-800 mb-1">{principle.label}</h3>
              <p className="text-xs text-gray-500">{principle.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}