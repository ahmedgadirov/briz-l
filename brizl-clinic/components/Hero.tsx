'use client';

import { motion } from 'framer-motion';
import { Phone, ArrowRight, Eye, Shield, Heart } from 'lucide-react';
import { translations, clinicInfo, Locale } from '@/lib/i18n';

interface HeroProps {
  locale: Locale;
}

export default function Hero({ locale }: HeroProps) {
  const t = translations[locale];

  return (
    <section className="relative min-h-screen flex items-center pt-20 overflow-hidden">
      {/* Background decorations */}
      <div className="absolute inset-0 mint-gradient-hero" />
      <div className="absolute top-20 right-0 w-96 h-96 bg-mint-500/10 rounded-full blur-3xl" />
      <div className="absolute bottom-0 left-0 w-80 h-80 bg-mint-500/5 rounded-full blur-3xl" />
      
      {/* Floating elements */}
      <motion.div
        animate={{ y: [-10, 10, -10] }}
        transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
        className="absolute top-32 right-20 hidden lg:block"
      >
        <div className="w-20 h-20 bg-mint-500/20 rounded-full flex items-center justify-center">
          <Eye className="w-10 h-10 text-clinic-primary" />
        </div>
      </motion.div>
      
      <motion.div
        animate={{ y: [10, -10, 10] }}
        transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
        className="absolute bottom-40 right-40 hidden lg:block"
      >
        <div className="w-16 h-16 bg-mint-500/15 rounded-full flex items-center justify-center">
          <Shield className="w-8 h-8 text-clinic-primary" />
        </div>
      </motion.div>
      
      <motion.div
        animate={{ y: [-5, 15, -5] }}
        transition={{ duration: 7, repeat: Infinity, ease: "easeInOut" }}
        className="absolute top-60 left-20 hidden lg:block"
      >
        <div className="w-14 h-14 bg-mint-500/10 rounded-full flex items-center justify-center">
          <Heart className="w-7 h-7 text-clinic-primary" />
        </div>
      </motion.div>

      <div className="container-custom relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
          >
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="inline-flex items-center gap-2 px-4 py-2 bg-mint-light rounded-full text-clinic-primary text-sm font-medium mb-6"
            >
              <Eye className="w-4 h-4" />
              {locale === 'az' ? 'Peşəkar Göz Sağlamlığı' : locale === 'ru' ? 'Профессиональное Здоровье Глаз' : 'Professional Eye Health'}
            </motion.div>
            
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 leading-tight mb-6"
            >
              {t.hero.title}
            </motion.h1>
            
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="text-lg md:text-xl text-gray-600 mb-8 max-w-xl"
            >
              {t.hero.subtitle}
            </motion.p>
            
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="flex flex-col sm:flex-row gap-4"
            >
              <a
                href={clinicInfo.whatsapp}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-mint flex items-center justify-center gap-2 text-lg"
              >
                <Phone className="w-5 h-5" />
                {t.hero.cta_booking}
              </a>
              <a
                href="#services"
                className="btn-outline flex items-center justify-center gap-2 text-lg"
              >
                {t.hero.cta_services}
                <ArrowRight className="w-5 h-5" />
              </a>
            </motion.div>

            {/* Stats */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="grid grid-cols-3 gap-6 mt-12 pt-8 border-t border-gray-200"
            >
              <div>
                <div className="text-3xl font-bold text-clinic-primary">10+</div>
                <div className="text-sm text-gray-500">{t.whyUs.experience}</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-clinic-primary">5000+</div>
                <div className="text-sm text-gray-500">{t.whyUs.patients}</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-clinic-primary">4</div>
                <div className="text-sm text-gray-500">{t.whyUs.doctors}</div>
              </div>
            </motion.div>
          </motion.div>

          {/* Right Content - Hero Image */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            className="relative hidden lg:block"
          >
            <div className="relative">
              {/* Main card */}
              <div className="bg-white rounded-3xl shadow-2xl p-8 relative z-10">
                <div className="aspect-square bg-gradient-to-br from-mint-light to-white rounded-2xl flex items-center justify-center">
                  <div className="text-center">
                    <div className="w-32 h-32 mx-auto bg-gradient-to-br from-clinic-primary to-clinic-secondary rounded-full flex items-center justify-center mb-6">
                      <Eye className="w-16 h-16 text-white" />
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900 mb-2">
                      {locale === 'az' ? 'Briz-L Göz Klinikası' : locale === 'ru' ? 'Клиника Briz-L' : 'Briz-L Eye Clinic'}
                    </h3>
                    <p className="text-gray-500">
                      {locale === 'az' ? 'Müasir oftalmologiya' : locale === 'ru' ? 'Современная офтальмология' : 'Modern Ophthalmology'}
                    </p>
                  </div>
                </div>
              </div>
              
              {/* Decorative elements */}
              <div className="absolute -bottom-4 -right-4 w-full h-full bg-clinic-primary/20 rounded-3xl -z-10" />
              <div className="absolute -bottom-8 -right-8 w-full h-full bg-clinic-primary/10 rounded-3xl -z-20" />
            </div>
          </motion.div>
        </div>
      </div>

      {/* Scroll indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1 }}
        className="absolute bottom-8 left-1/2 -translate-x-1/2"
      >
        <motion.div
          animate={{ y: [0, 10, 0] }}
          transition={{ duration: 2, repeat: Infinity }}
          className="w-6 h-10 border-2 border-clinic-primary rounded-full flex justify-center pt-2"
        >
          <div className="w-1.5 h-3 bg-clinic-primary rounded-full" />
        </motion.div>
      </motion.div>
    </section>
  );
}