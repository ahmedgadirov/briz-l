'use client'

import { motion } from 'framer-motion'
import { MapPin, Clock, Phone } from 'lucide-react'
import { clinicInfo } from '@/lib/clinic-data'
import { useTranslations } from 'next-intl'

export default function Location() {
  const t = useTranslations('location')

  return (
    <section id="location" className="py-24 px-6 bg-gradient-to-b from-transparent via-mint/5 to-transparent">
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

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Map */}
          <motion.div
            initial={{ opacity: 0, x: -40 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="glass p-4 border border-mint/20 h-[400px] lg:h-auto"
          >
            <iframe
              src={`https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3039.4!2d${clinicInfo.coordinates.lng}!3d${clinicInfo.coordinates.lat}!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNDDCsDI0JzA3LjAiTiA0OcKwNTAnMjMuMCJF!5e0!3m2!1sen!2s!4v1!5m2!1sen!2s`}
              width="100%"
              height="100%"
              style={{ border: 0, minHeight: '350px' }}
              allowFullScreen
              loading="lazy"
              referrerPolicy="no-referrer-when-downgrade"
              className="rounded-xl"
              title="Briz-L Clinic Location"
            />
          </motion.div>

          {/* Info */}
          <motion.div
            initial={{ opacity: 0, x: 40 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="flex flex-col justify-center"
          >
            <div className="glass p-8 border border-mint/20 space-y-6">
              {/* Address */}
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-mint/10 flex items-center justify-center flex-shrink-0">
                  <MapPin className="w-5 h-5 text-mint" />
                </div>
                <div>
                  <h3 className="font-display font-semibold text-gray-800 mb-1">{t('address')}</h3>
                  <p className="text-gray-500">{clinicInfo.address.full}</p>
                </div>
              </div>

              {/* Hours */}
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-mint/10 flex items-center justify-center flex-shrink-0">
                  <Clock className="w-5 h-5 text-mint" />
                </div>
                <div>
                  <h3 className="font-display font-semibold text-gray-800 mb-1">{t('workingHours')}</h3>
                  <p className="text-gray-500">{t('weekdays')}: {clinicInfo.hours.weekdays}</p>
                  <p className="text-gray-500">{t('weekend')}: {clinicInfo.hours.weekend}</p>
                </div>
              </div>

              {/* Phones */}
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-mint/10 flex items-center justify-center flex-shrink-0">
                  <Phone className="w-5 h-5 text-mint" />
                </div>
                <div>
                  <h3 className="font-display font-semibold text-gray-800 mb-1">{t('phones')}</h3>
                  <p className="text-gray-500">
                    <a href={`tel:${clinicInfo.phone.main}`} className="hover:text-mint transition-colors">
                      {clinicInfo.phone.main}
                    </a>
                  </p>
                  <p className="text-gray-500">
                    <a href={`tel:${clinicInfo.phone.secondary}`} className="hover:text-mint transition-colors">
                      {clinicInfo.phone.secondary}
                    </a>
                  </p>
                </div>
              </div>

              {/* Navigation buttons */}
              <div className="flex flex-wrap gap-3 pt-4 border-t border-mint/10">
                <motion.a
                  href={clinicInfo.maps.google}
                  target="_blank"
                  rel="noopener noreferrer"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="inline-flex items-center gap-2 px-5 py-3 bg-mint text-white rounded-xl font-medium text-sm hover:bg-mint-dark transition-colors"
                >
                  <img 
                    src="/google-maps.svg.png" 
                    alt="Google Maps" 
                    className="w-5 h-5 object-contain brightness-0 invert"
                  />
                  Google Maps
                </motion.a>
                <motion.a
                  href={clinicInfo.maps.waze}
                  target="_blank"
                  rel="noopener noreferrer"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="inline-flex items-center gap-2 px-5 py-3 glass border border-mint/30 text-mint rounded-xl font-medium text-sm hover:border-mint/60 transition-colors"
                >
                  <img 
                    src="/waze.png" 
                    alt="Waze" 
                    className="w-5 h-5 object-contain"
                  />
                  Waze
                </motion.a>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}