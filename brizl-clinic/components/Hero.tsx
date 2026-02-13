'use client'

import { motion } from 'framer-motion'
import { ArrowDown, Phone, MapPin } from 'lucide-react'

const services = [
  { name: 'Katarakta', href: '#services' },
  { name: 'Excimer Laser', href: '#services' },
  { name: 'Qlaukoma', href: '#services' },
]

export default function Hero() {
  return (
    <section className="min-h-screen flex flex-col items-center justify-center px-6 py-20">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-center max-w-4xl"
      >
        {/* Brand line */}
        <h1 className="font-display text-4xl md:text-6xl lg:text-7xl font-medium tracking-tight mb-8 leading-tight">
          <span className="gradient-text">Briz-L</span> Göz Klinikası — 
          peşəkar göz sağlamlığı{' '}
          <span className="text-mint">xidmətləri</span>.
        </h1>

        <p className="text-gray-600 text-lg md:text-xl max-w-2xl mx-auto mb-8">
          Müasir texnologiyalar və təcrübəli həkimlərlə göz sağlamlığınızı etibar edin.
        </p>

        {/* Pills */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="flex flex-wrap items-center justify-center gap-3 mt-8"
        >
          {services.map((service, index) => (
            <motion.a
              key={service.name}
              href={service.href}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: 0.4 + index * 0.1 }}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.98 }}
              className="px-6 py-3 rounded-full glass border border-mint/30 text-mint font-medium text-sm md:text-base hover:border-mint/60 transition-all duration-300"
            >
              {service.name}
            </motion.a>
          ))}
        </motion.div>

        {/* Contact buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="flex flex-wrap items-center justify-center gap-4 mt-10"
        >
          <a
            href="tel:+994502222222"
            className="inline-flex items-center gap-2 px-6 py-3 bg-mint text-white rounded-xl font-medium hover:bg-mint-dark transition-colors"
          >
            <Phone className="w-4 h-4" />
            +994 50 222 22 22
          </a>
          <a
            href="https://maps.google.com"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-6 py-3 glass border border-gray-200 text-gray-700 rounded-xl font-medium hover:border-mint/40 transition-colors"
          >
            <MapPin className="w-4 h-4" />
            Bakı, Azərbaycan
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
            <span className="text-xs mb-2 uppercase tracking-widest">Xidmətlər</span>
            <ArrowDown className="w-5 h-5" />
          </motion.a>
        </motion.div>
      </motion.div>
    </section>
  )
}