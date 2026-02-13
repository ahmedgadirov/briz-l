'use client';

import { motion } from 'framer-motion';
import { User, Phone, MessageCircle, Award, Star, ArrowRight } from 'lucide-react';
import { translations, doctors, getDoctorName, getDoctorTitle, Locale } from '@/lib/i18n';

interface DoctorsProps {
  locale: Locale;
}

export default function Doctors({ locale }: DoctorsProps) {
  const t = translations[locale];

  return (
    <section id="doctors" className="section-spacing bg-white relative overflow-hidden">
      {/* Decorative background grid/mesh */}
      <div className="absolute inset-0 bg-[radial-gradient(#3EB489_0.5px,transparent_0.5px)] [background-size:24px_24px] opacity-[0.03]" />

      <div className="container-custom relative z-10">
        {/* Header */}
        <div className="text-center mb-20">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="inline-flex items-center gap-2 px-4 py-2 bg-mint-50 rounded-full text-clinic-primary text-sm font-bold mb-6 border border-mint-100 shadow-sm"
          >
            <Star className="w-4 h-4 fill-clinic-primary" />
            <span className="tracking-widest uppercase">{t.doctors.title}</span>
          </motion.div>

          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-4xl md:text-5xl font-black text-clinic-accent mb-6"
          >
            <span className="text-gradient">{t.doctors.title}</span>
          </motion.h2>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-xl text-gray-500 max-w-2xl mx-auto leading-relaxed"
          >
            {t.doctors.subtitle}
          </motion.p>
        </div>

        {/* Doctors Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {doctors.map((doctor, index) => (
            <motion.div
              key={doctor.id}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="group"
            >
              <div className="card-premium h-full flex flex-col p-6">
                {/* Doctor Avatar Placeholder */}
                <div className="relative mb-8 pt-4">
                  <div className="relative w-32 h-32 mx-auto">
                    {/* Ring animation */}
                    <div className="absolute inset-0 border-2 border-mint-200 border-dashed rounded-full animate-[spin_20s_linear_infinite]" />
                    <div className="absolute inset-2 bg-gradient-to-br from-clinic-primary to-clinic-secondary rounded-full flex items-center justify-center shadow-2xl shadow-mint-500/40 relative z-10">
                      <User className="w-16 h-16 text-white" />
                    </div>
                  </div>

                  {doctor.isChief && (
                    <motion.div
                      initial={{ scale: 0 }}
                      whileInView={{ scale: 1 }}
                      className="absolute top-2 right-1/2 translate-x-12 z-20 flex items-center gap-1.5 px-3 py-1.5 bg-clinic-accent text-white text-[10px] font-black uppercase tracking-widest rounded-full shadow-lg"
                    >
                      <Award className="w-3 h-3 text-mint-400" />
                      {t.doctors.chief_doctor}
                    </motion.div>
                  )}
                </div>

                {/* Doctor Info */}
                <div className="text-center flex-grow">
                  <h3 className="text-xl font-black text-clinic-accent mb-2 group-hover:text-clinic-primary transition-colors duration-300">
                    {getDoctorName(doctor, locale)}
                  </h3>
                  <p className="text-sm font-bold text-mint-600 uppercase tracking-widest mb-6">
                    {getDoctorTitle(doctor, locale)}
                  </p>

                  {/* Rating/Trust mock badge */}
                  <div className="flex justify-center items-center gap-1 mb-6">
                    {[1, 2, 3, 4, 5].map((i) => (
                      <Star key={i} className="w-3 h-3 fill-mint-500 text-mint-500" />
                    ))}
                  </div>
                </div>

                {/* Contact Actions */}
                <div className="grid grid-cols-2 gap-3 pt-6 border-t border-gray-50">
                  <a
                    href={`tel:${doctor.phone.replace(/\s/g, '')}`}
                    className="flex items-center justify-center p-3 glass-premium !bg-gray-50/50 hover:!bg-clinic-primary group/icon transition-all duration-300 rounded-2xl"
                    title={t.contact.phone}
                  >
                    <Phone className="w-5 h-5 text-gray-500 group-hover/icon:text-white transition-colors" />
                  </a>
                  <a
                    href={doctor.whatsapp}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center justify-center gap-2 p-3 bg-mint-50 hover:bg-mint-500 group/wa transition-all duration-300 rounded-2xl"
                  >
                    <MessageCircle className="w-5 h-5 text-clinic-primary group-hover/wa:text-white transition-colors" />
                    <span className="text-[10px] font-black uppercase tracking-tighter text-clinic-primary group-hover/wa:text-white transition-colors">WhatsApp</span>
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
          className="mt-20 text-center"
        >
          <div className="inline-block p-1 rounded-[20px] bg-gradient-to-r from-mint-100 via-white to-mint-100 border border-mint-50">
            <a
              href="#contact"
              className="btn-premium flex items-center justify-center gap-3 px-10"
            >
              <Star className="w-5 h-5" />
              {t.doctors.book_appointment}
              <ArrowRight className="w-5 h-5" />
            </a>
          </div>
          <p className="mt-6 text-sm font-bold text-gray-400 uppercase tracking-widest">
            {locale === 'az'
              ? 'Təcrübəli Heyətimiz Sizi Gözləyir'
              : locale === 'ru'
                ? 'Наш Опытный Персонал Ждет Вас'
                : 'Our Experienced Staff is Waiting for You'}
          </p>
        </motion.div>
      </div>
    </section>
  );
}