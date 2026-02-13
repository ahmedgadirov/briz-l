'use client';

import { motion } from 'framer-motion';
import { MapPin, Phone, Clock, MessageCircle, ExternalLink } from 'lucide-react';
import { translations, clinicInfo, getClinicAddress, getWorkingHours, Locale } from '@/lib/i18n';

interface ContactProps {
  locale: Locale;
}

export default function Contact({ locale }: ContactProps) {
  const t = translations[locale];

  return (
    <section id="contact" className="section-padding bg-gradient-to-b from-mint-light/30 to-white">
      <div className="container-custom">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <span className="inline-block px-4 py-2 bg-mint-light text-clinic-primary rounded-full text-sm font-medium mb-4">
            {t.contact.title}
          </span>
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            {t.contact.title}
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            {t.contact.subtitle}
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-12">
          {/* Contact Info */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="space-y-6"
          >
            {/* Address Card */}
            <div className="bg-white rounded-2xl shadow-lg p-6 flex items-start gap-4">
              <div className="w-12 h-12 bg-clinic-primary/10 rounded-xl flex items-center justify-center flex-shrink-0">
                <MapPin className="w-6 h-6 text-clinic-primary" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">{t.contact.address}</h3>
                <p className="text-gray-600">{getClinicAddress(locale)}</p>
                <div className="flex gap-3 mt-3">
                  <a
                    href={clinicInfo.mapsUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-sm text-clinic-primary hover:underline"
                  >
                    Google Maps
                    <ExternalLink className="w-3 h-3" />
                  </a>
                  <a
                    href={clinicInfo.wazeUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-sm text-clinic-primary hover:underline"
                  >
                    Waze
                    <ExternalLink className="w-3 h-3" />
                  </a>
                </div>
              </div>
            </div>

            {/* Phone Card */}
            <div className="bg-white rounded-2xl shadow-lg p-6 flex items-start gap-4">
              <div className="w-12 h-12 bg-clinic-primary/10 rounded-xl flex items-center justify-center flex-shrink-0">
                <Phone className="w-6 h-6 text-clinic-primary" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">{t.contact.phone}</h3>
                <div className="space-y-1">
                  {clinicInfo.phones.map((phone) => (
                    <a
                      key={phone}
                      href={`tel:${phone.replace(/\s/g, '')}`}
                      className="block text-gray-600 hover:text-clinic-primary transition-colors"
                    >
                      {phone}
                    </a>
                  ))}
                </div>
              </div>
            </div>

            {/* Working Hours Card */}
            <div className="bg-white rounded-2xl shadow-lg p-6 flex items-start gap-4">
              <div className="w-12 h-12 bg-clinic-primary/10 rounded-xl flex items-center justify-center flex-shrink-0">
                <Clock className="w-6 h-6 text-clinic-primary" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">{t.contact.working_hours}</h3>
                <p className="text-gray-600">{getWorkingHours(locale)}</p>
              </div>
            </div>

            {/* WhatsApp CTA */}
            <a
              href={clinicInfo.whatsapp}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-center gap-3 w-full py-4 bg-green-500 hover:bg-green-600 text-white rounded-2xl transition-colors font-semibold text-lg"
            >
              <MessageCircle className="w-6 h-6" />
              WhatsApp
            </a>
          </motion.div>

          {/* Map */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="h-[400px] lg:h-full min-h-[400px] rounded-2xl overflow-hidden shadow-lg"
          >
            <iframe
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3039.4!2d49.83970805339595!3d40.401955867990424!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNDDCsDI0JzA3LjAiTiA0OcKwNTAnMjMuMCJF!5e0!3m2!1sen!2s!4v1"
              width="100%"
              height="100%"
              style={{ border: 0 }}
              allowFullScreen
              loading="lazy"
              referrerPolicy="no-referrer-when-downgrade"
              title="Briz-L Clinic Location"
              className="grayscale-[30%] hover:grayscale-0 transition-all duration-300"
            />
          </motion.div>
        </div>
      </div>
    </section>
  );
}