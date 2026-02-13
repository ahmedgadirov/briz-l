'use client';

import { motion } from 'framer-motion';
import { Eye, Syringe, ArrowRight, Activity } from 'lucide-react';
import { translations, surgeries, getSurgeryName, getSurgeryDescription, Locale } from '@/lib/i18n';

interface ServicesProps {
  locale: Locale;
}

const categoryStyles: Record<string, string> = {
  refractive: 'from-blue-50 to-indigo-50 text-blue-600 border-blue-100',
  cataract: 'from-purple-50 to-fuchsia-50 text-purple-600 border-purple-100',
  corneal: 'from-cyan-50 to-teal-50 text-cyan-600 border-cyan-100',
  retinal: 'from-orange-50 to-amber-50 text-orange-600 border-orange-100',
  strabismus: 'from-pink-50 to-rose-50 text-pink-600 border-pink-100',
  glaucoma: 'from-red-50 to-orange-50 text-red-600 border-red-100',
};

export default function Services({ locale }: ServicesProps) {
  const t = translations[locale];

  return (
    <section id="services" className="section-spacing bg-white relative overflow-hidden">
      {/* Decorative background blur */}
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-mint-50/50 rounded-full blur-[120px] -z-10" />

      <div className="container-custom">
        {/* Header */}
        <div className="text-center mb-20">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="inline-flex items-center gap-2 px-4 py-2 bg-mint-50 rounded-full text-clinic-primary text-sm font-bold mb-6 border border-mint-100 shadow-sm"
          >
            <Activity className="w-4 h-4" />
            <span className="tracking-widest uppercase">{t.services.title}</span>
          </motion.div>

          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-4xl md:text-5xl font-black text-clinic-accent mb-6"
          >
            <span className="text-gradient">{t.services.title}</span>
          </motion.h2>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-xl text-gray-500 max-w-2xl mx-auto leading-relaxed"
          >
            {t.services.subtitle}
          </motion.p>
        </div>

        {/* Services Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {surgeries.map((surgery, index) => (
            <motion.div
              key={surgery.id}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.05 }}
              className="group"
            >
              <div className="card-premium h-full flex flex-col relative overflow-hidden">
                {/* Visual Category Accent */}
                <div className={`absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r ${categoryStyles[surgery.category] || 'from-mint-400 to-mint-600'}`} />

                {/* Icon Container */}
                <div className="flex justify-between items-start mb-8">
                  <div className="w-16 h-16 glass-premium rounded-2xl flex items-center justify-center shadow-md group-hover:scale-110 transition-transform duration-500">
                    {surgery.icon === 'Syringe' ? (
                      <Syringe className="w-8 h-8 text-clinic-primary" />
                    ) : (
                      <Eye className="w-8 h-8 text-clinic-primary" />
                    )}
                  </div>
                  <span className={`text-[10px] font-black uppercase tracking-widest px-3 py-1.5 rounded-lg border ${categoryStyles[surgery.category] || 'bg-mint-50 border-mint-100 text-clinic-primary'}`}>
                    {t.services.categories[surgery.category as keyof typeof t.services.categories]}
                  </span>
                </div>

                {/* Content */}
                <h3 className="text-2xl font-black text-clinic-accent mb-4 group-hover:text-clinic-primary transition-colors">
                  {getSurgeryName(surgery, locale)}
                </h3>
                <p className="text-gray-500 leading-relaxed mb-8 flex-grow">
                  {getSurgeryDescription(surgery, locale)}
                </p>

                {/* Bottom Action */}
                <div className="pt-6 border-t border-gray-50 mt-auto flex items-center justify-between">
                  <a
                    href="#contact"
                    className="inline-flex items-center gap-2 text-clinic-primary font-bold text-sm tracking-tight group/link"
                  >
                    {t.services.learn_more}
                    <ArrowRight className="w-4 h-4 group-hover/link:translate-x-1 transition-transform" />
                  </a>
                  <div className="w-8 h-8 rounded-full bg-mint-50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                    <Activity className="w-4 h-4 text-clinic-primary animate-pulse" />
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Dynamic Bottom CTA */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-24"
        >
          <div className="glass-premium rounded-[40px] p-10 md:p-16 relative overflow-hidden text-center">
            <div className="absolute inset-0 bg-gradient-to-br from-mint-50 to-white -z-10" />

            <h3 className="text-3xl md:text-4xl font-black text-clinic-accent mb-6 leading-tight">
              {locale === 'az'
                ? 'Gözlərinizi Bizə Etibar Edin'
                : locale === 'ru'
                  ? 'Доверьте свои глаза нам'
                  : 'Trust Your Eyes to Us'}
            </h3>
            <p className="text-lg text-gray-500 mb-10 max-w-2xl mx-auto">
              {locale === 'az'
                ? 'Ən son texnologiya ilə peşəkar müayinə və müalicə.'
                : locale === 'ru'
                  ? 'Профессиональное обследование и лечение с использованием новейших технологий.'
                  : 'Professional examination and treatment with the latest technology.'}
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-5">
              <a
                href="#contact"
                className="btn-premium flex items-center gap-3 text-lg px-10"
              >
                {locale === 'az' ? 'Əlaqə Saxlayın' : locale === 'ru' ? 'Связаться' : 'Contact Us'}
                <ArrowRight className="w-5 h-5" />
              </a>
              <span className="text-sm font-bold text-gray-400 uppercase tracking-widest">{t.footer.rights}</span>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}