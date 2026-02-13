'use client'

import { motion } from 'framer-motion'
import { Phone, MessageCircle, Calendar } from 'lucide-react'
import { clinicInfo } from '@/lib/clinic-data'

export default function BookingCTA() {
  return (
    <section className="py-24 px-6">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="card-glow glass p-8 md:p-12 border border-mint/30 text-center relative overflow-hidden"
        >
          {/* Background decoration */}
          <div className="absolute -top-20 -right-20 w-40 h-40 bg-mint/10 rounded-full blur-3xl" />
          <div className="absolute -bottom-20 -left-20 w-40 h-40 bg-mint/10 rounded-full blur-3xl" />
          
          {/* Content */}
          <div className="relative z-10">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-mint/10 mb-6">
              <Calendar className="w-8 h-8 text-mint" />
            </div>
            
            <h2 className="font-display text-2xl md:text-3xl font-semibold text-gray-800 mb-4">
              Müayinəyə yazılın
            </h2>
            
            <p className="text-gray-500 max-w-xl mx-auto mb-8">
              Göz sağlamlığınız üçün peşəkar yardım. Bizimlə əlaqə saxlayın və müayinə vaxtı təyin edin.
            </p>
            
            {/* Contact buttons */}
            <div className="flex flex-wrap items-center justify-center gap-4">
              <motion.a
                href={clinicInfo.social.whatsapp}
                target="_blank"
                rel="noopener noreferrer"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="inline-flex items-center gap-2 px-6 py-4 bg-green-500 hover:bg-green-600 text-white rounded-xl font-medium transition-colors shadow-lg shadow-green-500/20"
              >
                <MessageCircle className="w-5 h-5" />
                WhatsApp ilə yazıl
              </motion.a>
              
              <motion.a
                href={`tel:${clinicInfo.phone.main}`}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="inline-flex items-center gap-2 px-6 py-4 bg-mint hover:bg-mint-dark text-white rounded-xl font-medium transition-colors shadow-lg shadow-mint/20"
              >
                <Phone className="w-5 h-5" />
                {clinicInfo.phone.main}
              </motion.a>
            </div>
            
            {/* Additional phones */}
            <p className="text-gray-400 text-sm mt-6">
              Alternativ: {' '}
              <a href={`tel:${clinicInfo.phone.secondary}`} className="text-mint hover:underline">
                {clinicInfo.phone.secondary}
              </a>
            </p>
          </div>
        </motion.div>
      </div>
    </section>
  )
}