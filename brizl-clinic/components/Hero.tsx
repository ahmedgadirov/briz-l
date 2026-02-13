'use client';

import { motion } from 'framer-motion';
import { Phone, ArrowRight, Eye, Shield, Heart, Sparkles } from 'lucide-react';
import { translations, clinicInfo, Locale } from '@/lib/i18n';

interface HeroProps {
  locale: Locale;
}

export default function Hero({ locale }: HeroProps) {
  const t = translations[locale];

  return (
    <section className="relative min-h-[90vh] flex items-center pt-24 pb-16 overflow-hidden mint-gradient-mesh">
      {/* Dynamic Background Elements */}
      <div className="absolute top-[-10%] right-[-10%] w-[500px] h-[500px] bg-mint-400/10 rounded-full blur-[120px] animate-pulse-soft" />
      <div className="absolute bottom-[-10%] left-[-10%] w-[400px] h-[400px] bg-clinic-primary/10 rounded-full blur-[100px] animate-pulse-soft" style={{ animationDelay: '1s' }} />

      {/* Decorative Floating Icons */}
      <motion.div
        animate={{ y: [-20, 20, -20], rotate: [0, 10, 0] }}
        transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
        className="absolute top-40 right-[15%] hidden lg:block z-20"
      >
        <div className="glass-premium p-4 rounded-2xl">
          <Eye className="w-8 h-8 text-clinic-primary" />
        </div>
      </motion.div>

      <motion.div
        animate={{ y: [15, -15, 15], rotate: [0, -10, 0] }}
        transition={{ duration: 7, repeat: Infinity, ease: "easeInOut" }}
        className="absolute bottom-32 left-[10%] hidden lg:block z-20"
      >
        <div className="glass-premium p-4 rounded-2xl">
          <Shield className="w-7 h-7 text-clinic-primary" />
        </div>
      </motion.div>

      <div className="container-custom relative z-10">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          {/* Left Content */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 1, ease: [0.16, 1, 0.3, 1] }}
          >
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="inline-flex items-center gap-2 px-4 py-2 bg-white/50 backdrop-blur-md border border-mint-200 rounded-full text-clinic-primary text-sm font-semibold mb-8 shadow-sm"
            >
              <Sparkles className="w-4 h-4" />
              <span className="tracking-wide uppercase">
                {locale === 'az' ? 'Peşəkar Göz Sağlamlığı' : locale === 'ru' ? 'Профессиональное Здоровье Глаз' : 'Professional Eye Health'}
              </span>
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="text-5xl md:text-6xl lg:text-7xl font-extrabold text-clinic-accent leading-[1.1] mb-8"
            >
              <span className="text-gradient">{t.hero.title.split(' ').slice(0, -1).join(' ')}</span>
              <br />
              {t.hero.title.split(' ').slice(-1)}
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="text-xl text-gray-600 mb-10 max-w-xl leading-relaxed"
            >
              {t.hero.subtitle}
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="flex flex-col sm:flex-row gap-5"
            >
              <a
                href={clinicInfo.whatsapp}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-premium flex items-center justify-center gap-3 text-lg group"
              >
                <Phone className="w-5 h-5 group-hover:rotate-12 transition-transform" />
                {t.hero.cta_booking}
              </a>
              <a
                href="#services"
                className="btn-ghost flex items-center justify-center gap-3 text-lg group"
              >
                {t.hero.cta_services}
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </a>
            </motion.div>

            {/* Stats Section */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="grid grid-cols-3 gap-8 mt-16 pt-10 border-t border-mint-100"
            >
              <div className="space-y-1">
                <div className="text-4xl font-black text-clinic-primary tracking-tight">10+</div>
                <div className="text-xs uppercase font-bold text-gray-400 tracking-wider font-display">{t.whyUs.experience}</div>
              </div>
              <div className="space-y-1">
                <div className="text-4xl font-black text-clinic-primary tracking-tight">5K+</div>
                <div className="text-xs uppercase font-bold text-gray-400 tracking-wider font-display">{t.whyUs.patients}</div>
              </div>
              <div className="space-y-1">
                <div className="text-4xl font-black text-clinic-primary tracking-tight">4</div>
                <div className="text-xs uppercase font-bold text-gray-400 tracking-wider font-display">{t.whyUs.doctors}</div>
              </div>
            </motion.div>
          </motion.div>

          {/* Right Content - Modern Abstract Card */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9, rotate: 2 }}
            animate={{ opacity: 1, scale: 1, rotate: 0 }}
            transition={{ duration: 1.2, ease: [0.16, 1, 0.3, 1] }}
            className="relative hidden lg:block"
          >
            <div className="relative z-10">
              <div className="glass-premium rounded-[40px] p-10 shadow-2xl overflow-hidden relative group">
                {/* Decorative mesh inside card */}
                <div className="absolute inset-0 bg-gradient-to-br from-mint-100/50 to-white/30 -z-10 group-hover:scale-110 transition-transform duration-700" />

                <div className="flex flex-col items-center text-center">
                  <motion.div
                    animate={{ scale: [1, 1.05, 1] }}
                    transition={{ duration: 4, repeat: Infinity }}
                    className="w-40 h-40 bg-gradient-to-br from-clinic-primary to-clinic-secondary rounded-full flex items-center justify-center mb-8 shadow-2xl shadow-mint-500/30"
                  >
                    <Eye className="w-20 h-20 text-white" />
                  </motion.div>

                  <h3 className="text-3xl font-black text-clinic-accent mb-4 leading-tight">
                    {locale === 'az' ? 'Briz-L Göz Klinikası' : locale === 'ru' ? 'Клиника Briz-L' : 'Briz-L Eye Clinic'}
                  </h3>

                  <p className="text-gray-500 text-lg font-medium mb-8">
                    {locale === 'az' ? 'Müasir oftalmologiya' : locale === 'ru' ? 'Современная офтальмология' : 'Modern Ophthalmology'}
                  </p>

                  <div className="flex items-center gap-3 px-5 py-3 bg-mint-50 rounded-2xl border border-mint-100">
                    <Heart className="w-5 h-5 text-clinic-primary fill-clinic-primary" />
                    <span className="text-clinic-primary font-bold">Health & Trust</span>
                  </div>
                </div>
              </div>

              {/* Abstract decorative floating rings */}
              <div className="absolute -top-10 -left-10 w-32 h-32 border-2 border-mint-300/30 rounded-full animate-float" style={{ animationDelay: '0.5s' }} />
              <div className="absolute -bottom-10 -right-10 w-48 h-48 border-[3px] border-mint-500/10 rounded-full animate-float" />
            </div>

            {/* Background Blur Patterns */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[120%] h-[120%] bg-mint-500/5 blur-[100px] -z-10" />
          </motion.div>
        </div>
      </div>

      {/* Modern Scroll Indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5 }}
        className="absolute bottom-10 left-1/2 -translate-x-1/2 hidden md:block"
      >
        <div className="flex flex-col items-center gap-3">
          <span className="text-[10px] uppercase font-bold tracking-widest text-gray-400 font-display">Explore</span>
          <motion.div
            animate={{ y: [0, 8, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="w-1 h-12 bg-gradient-to-b from-clinic-primary to-transparent rounded-full"
          />
        </div>
      </motion.div>
    </section>
  );
}