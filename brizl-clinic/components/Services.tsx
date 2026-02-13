'use client';

import { motion } from 'framer-motion';
import { Eye, Syringe, ArrowRight } from 'lucide-react';
import { translations, surgeries, getSurgeryName, getSurgeryDescription, Locale } from '@/lib/i18n';

interface ServicesProps {
  locale: Locale;
}

const categoryColors: Record<string, string> = {
  refractive: 'bg-blue-50 border-blue-200',
  cataract: 'bg-purple-50 border-purple-200',
  corneal: 'bg-cyan-50 border-cyan-200',
  retinal: 'bg-orange-50 border-orange-200',
  strabismus: 'bg-pink-50 border-pink-200',
  glaucoma: 'bg-red-50 border-red-200',
};

export default function Services({ locale }: ServicesProps) {
  const t = translations[locale];

  return (
    <section id="services" className="section-padding bg-white">
      <div className="container-custom">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <span className="inline-block px-4 py-2 bg-mint-light text-clinic-primary rounded-full text-sm font-medium mb-4">
            {t.services.title}
          </span>
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            {t.services.title}
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            {t.services.subtitle}
          </p>
        </motion.div>

        {/* Services Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {surgeries.map((surgery, index) => (
            <motion.div
              key={surgery.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className={`group relative bg-white border-2 rounded-2xl p-6 card-hover ${categoryColors[surgery.category] || 'bg-gray-50 border-gray-200'}`}
            >
              {/* Icon */}
              <div className="w-14 h-14 bg-white rounded-xl shadow-sm flex items-center justify-center mb-4">
                {surgery.icon === 'Syringe' ? (
                  <Syringe className="w-7 h-7 text-clinic-primary" />
                ) : (
                  <Eye className="w-7 h-7 text-clinic-primary" />
                )}
              </div>

              {/* Content */}
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {getSurgeryName(surgery, locale)}
              </h3>
              <p className="text-gray-600 text-sm mb-4">
                {getSurgeryDescription(surgery, locale)}
              </p>

              {/* Category Badge */}
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium px-3 py-1 bg-white rounded-full text-gray-500">
                  {t.services.categories[surgery.category as keyof typeof t.services.categories]}
                </span>
                <a
                  href="#contact"
                  className="flex items-center gap-1 text-clinic-primary text-sm font-medium opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  {t.services.learn_more}
                  <ArrowRight className="w-4 h-4" />
                </a>
              </div>
            </motion.div>
          ))}
        </div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mt-12"
        >
          <p className="text-gray-600 mb-4">
            {locale === 'az' 
              ? 'Qiymətlər haqqında məlumat üçün bizimlə əlaqə saxlayın' 
              : locale === 'ru' 
              ? 'Свяжитесь с нами для получения информации о ценах' 
              : 'Contact us for pricing information'}
          </p>
          <a
            href="#contact"
            className="btn-mint inline-flex items-center gap-2"
          >
            {locale === 'az' ? 'Əlaqə Saxlayın' : locale === 'ru' ? 'Связаться' : 'Contact Us'}
            <ArrowRight className="w-5 h-5" />
          </a>
        </motion.div>
      </div>
    </section>
  );
}