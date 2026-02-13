'use client';

import { motion } from 'framer-motion';
import { Award, Users, Scissors, Stethoscope, Cpu, BadgeCheck, Headphones } from 'lucide-react';
import { translations, Locale } from '@/lib/i18n';

interface WhyChooseUsProps {
  locale: Locale;
}

const features = [
  { icon: Award, key: 'experience', value: '10+' },
  { icon: Users, key: 'patients', value: '5000+' },
  { icon: Scissors, key: 'surgeries', value: '1000+' },
  { icon: Stethoscope, key: 'doctors', value: '4' },
];

const benefits = [
  { icon: Cpu, key: 'modern_tech' },
  { icon: BadgeCheck, key: 'certified' },
  { icon: Headphones, key: 'support' },
];

export default function WhyChooseUs({ locale }: WhyChooseUsProps) {
  const t = translations[locale];

  return (
    <section id="about" className="section-padding bg-white">
      <div className="container-custom">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <span className="inline-block px-4 py-2 bg-mint-light text-clinic-primary rounded-full text-sm font-medium mb-4">
            {t.whyUs.title}
          </span>
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            {t.whyUs.title}
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            {t.whyUs.subtitle}
          </p>
        </motion.div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-16"
        >
          {features.map((feature, index) => (
            <motion.div
              key={feature.key}
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="text-center p-6 bg-gradient-to-br from-mint-light to-white rounded-2xl"
            >
              <div className="w-14 h-14 mx-auto bg-clinic-primary/10 rounded-xl flex items-center justify-center mb-4">
                <feature.icon className="w-7 h-7 text-clinic-primary" />
              </div>
              <div className="text-3xl font-bold text-clinic-primary mb-1">
                {feature.value}
              </div>
              <div className="text-sm text-gray-600">
                {t.whyUs[feature.key as keyof typeof t.whyUs]}
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Benefits */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="grid md:grid-cols-3 gap-8"
        >
          {benefits.map((benefit, index) => (
            <motion.div
              key={benefit.key}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="flex items-start gap-4 p-6 bg-gray-50 rounded-2xl"
            >
              <div className="w-12 h-12 bg-clinic-primary rounded-xl flex items-center justify-center flex-shrink-0">
                <benefit.icon className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">
                  {t.whyUs[benefit.key as keyof typeof t.whyUs]}
                </h3>
                <p className="text-sm text-gray-600">
                  {locale === 'az' 
                    ? 'Müasir avadanlıqlar və peşəkar yanaşma ilə xidmətinizdəyik'
                    : locale === 'ru'
                    ? 'Мы служим вам современным оборудованием и профессиональным подходом'
                    : 'We serve you with modern equipment and professional approach'}
                </p>
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}