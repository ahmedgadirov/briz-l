'use client'

import { motion } from 'framer-motion'
import { Phone, MessageCircle, User, Bot } from 'lucide-react'
import { doctors } from '@/lib/clinic-data'
import { useChat } from '@/hooks/useChat'

export default function Doctors() {
  const { openChat, sendDoctorQuery } = useChat()

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
            Həkimlərimiz
          </h2>
          <p className="text-gray-500 text-lg max-w-2xl mx-auto">
            Peşəkar və təcrübəli həkim heyəti göz sağlamlığınızı etibarlı əllərə verir.
          </p>
        </motion.div>

        {/* Doctors grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {doctors.map((doctor, index) => (
            <motion.div
              key={doctor.id}
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
                {doctor.name}
              </h3>

              {/* Title */}
              <p className="text-mint text-sm font-medium mb-3">
                {doctor.title}
              </p>

              {/* Description */}
              <p className="text-gray-500 text-sm mb-4 leading-relaxed">
                {doctor.description}
              </p>

              {/* Contact buttons */}
              <div className="flex flex-wrap items-center justify-center gap-2">
                <motion.a
                  href={`tel:${doctor.phone.replace(/\s/g, '')}`}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="inline-flex items-center gap-1.5 px-3 py-2 bg-mint/10 hover:bg-mint/20 text-mint rounded-lg text-sm font-medium transition-colors"
                >
                  <Phone className="w-4 h-4" />
                  Zəng
                </motion.a>
                <motion.a
                  href={doctor.whatsapp}
                  target="_blank"
                  rel="noopener noreferrer"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="inline-flex items-center gap-1.5 px-3 py-2 bg-green-500/10 hover:bg-green-500/20 text-green-600 rounded-lg text-sm font-medium transition-colors"
                >
                  <MessageCircle className="w-4 h-4" />
                  WhatsApp
                </motion.a>
                <motion.button
                  onClick={() => handleAskAboutDoctor(doctor.id)}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="inline-flex items-center gap-1.5 px-3 py-2 bg-gray-100 hover:bg-gray-200 text-gray-600 rounded-lg text-sm font-medium transition-colors"
                >
                  <Bot className="w-4 h-4" />
                  Vera
                </motion.button>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}