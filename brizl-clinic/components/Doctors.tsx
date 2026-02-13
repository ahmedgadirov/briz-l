'use client';

import { motion } from 'framer-motion';
import { User, Phone, MessageCircle, Award } from 'lucide-react';
import { translations, doctors, getDoctorName, getDoctorTitle, Locale } from '@/lib/i18n';

interface DoctorsProps {
  locale: Locale;
}

export default function Doctors({ locale }: DoctorsProps) {
  const t = translations[locale];

  return (
    <section id="doctors" className="section-padding bg-gradient-to-b from-white to-mint-light/30">
      <div className="container-custom">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <span className="inline-block px-4 py-2 bg-mint-light text-clinic-primary rounded-full text-sm font-medium mb-4">
            {t.doctors.title}
          </span>
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            {t.doctors.title}
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            {t.doctors.subtitle}
          </p>
        </motion.div>

        {/* Doctors Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {doctors.map((doctor, index) => (
            <motion.div
              key={doctor.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="group bg-white rounded-2xl shadow-lg overflow-hidden card-hover"
            >
              {/* Doctor Image Placeholder */}
              <div className="relative h-48 bg-gradient-to-br from-mint-light to-white flex items-center justify-center">
                {doctor.isChief && (
                  <div className="absolute top-4 right-4 flex items-center gap-1 px-3 py-1 bg-clinic-primary text-white text-xs font-medium rounded-full">
                    <Award className="w-3 h-3" />
                    {t.doctors.chief_doctor}
                  </div>
                )}
                <div className="w-24 h-24 bg-gradient-to-br from-clinic-primary to-clinic-secondary rounded-full flex items-center justify-center">
                  <User className="w-12 h-12 text-white" />
                </div>
              </div>

              {/* Doctor Info */}
              <div className="p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-1">
                  {getDoctorName(doctor, locale)}
                </h3>
                <p className="text-sm text-clinic-primary font-medium mb-4">
                  {getDoctorTitle(doctor, locale)}
                </p>

                {/* Contact Buttons */}
                <div className="flex gap-2">
                  <a
                    href={`tel:${doctor.phone.replace(/\s/g, '')}`}
                    className="flex-1 flex items-center justify-center gap-2 py-2 px-3 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors text-sm text-gray-700"
                  >
                    <Phone className="w-4 h-4" />
                  </a>
                  <a
                    href={doctor.whatsapp}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex-1 flex items-center justify-center gap-2 py-2 px-3 bg-green-50 hover:bg-green-100 rounded-lg transition-colors text-sm text-green-700"
                  >
                    <MessageCircle className="w-4 h-4" />
                    WhatsApp
                  </a>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Bottom CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-12 text-center"
        >
          <p className="text-gray-600 mb-4">
            {locale === 'az' 
              ? 'Müayinə üçün əvvəlcədən yazılmaq tövsiyə olunur' 
              : locale === 'ru' 
              ? 'Рекомендуется предварительная запись на прием' 
              : 'Prior appointment is recommended'}
          </p>
          <a
            href="#contact"
            className="btn-outline inline-flex items-center gap-2"
          >
            <Phone className="w-5 h-5" />
            {t.doctors.book_appointment}
          </a>
        </motion.div>
      </div>
    </section>
  );
}