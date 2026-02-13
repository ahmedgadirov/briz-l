'use client';

import { motion } from 'framer-motion';
import { Eye, Phone, Mail, MapPin, Instagram, Facebook, Send, ExternalLink, Heart } from 'lucide-react';
import { translations, clinicInfo, getClinicName, getClinicAddress, Locale } from '@/lib/i18n';

interface FooterProps {
  locale: Locale;
}

export default function Footer({ locale }: FooterProps) {
  const t = translations[locale];
  const currentYear = new Date().getFullYear();

  const quickLinks = [
    { href: '#about', label: t.nav.about },
    { href: '#services', label: t.nav.services },
    { href: '#doctors', label: t.nav.doctors },
    { href: '#contact', label: t.nav.contact },
  ];

  return (
    <footer className="bg-clinic-accent text-white relative overflow-hidden">
      {/* Decorative background glass circles */}
      <div className="absolute top-[-20%] left-[-10%] w-[600px] h-[600px] bg-mint-500/5 rounded-full blur-[120px]" />
      <div className="absolute bottom-[-10%] right-[-5%] w-[400px] h-[400px] bg-clinic-primary/10 rounded-full blur-[100px]" />

      <div className="container-custom relative z-10 pt-24 pb-12">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-16 mb-20">
          {/* Brand & Mission */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="space-y-8"
          >
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-clinic-primary to-clinic-secondary rounded-2xl flex items-center justify-center shadow-lg shadow-mint-500/20">
                <Eye className="w-7 h-7 text-white" />
              </div>
              <span className="text-3xl font-black font-display tracking-tightest">Briz-L</span>
            </div>

            <p className="text-gray-400 text-lg leading-relaxed font-medium italic">
              "{t.footer.tagline}"
            </p>

            <div className="flex gap-4">
              {[
                { icon: Instagram, href: 'https://www.instagram.com/brizl_clinic/' },
                { icon: Facebook, href: '#' },
                { icon: Send, href: clinicInfo.whatsapp }
              ].map((social, i) => (
                <a
                  key={i}
                  href={social.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-12 h-12 glass-dark rounded-xl flex items-center justify-center hover:bg-clinic-primary hover:text-white transition-all duration-300 hover:-translate-y-1"
                >
                  <social.icon className="w-5 h-5" />
                </a>
              ))}
            </div>
          </motion.div>

          {/* Navigation Sections */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="space-y-8"
          >
            <h3 className="text-xs font-black uppercase tracking-[0.2em] text-mint-400">{t.footer.quick_links}</h3>
            <ul className="space-y-4">
              {quickLinks.map((link) => (
                <li key={link.href}>
                  <a
                    href={link.href}
                    className="text-gray-400 hover:text-white transition-colors text-base font-bold tracking-tight inline-flex items-center gap-2 group"
                  >
                    <span className="w-1.5 h-1.5 rounded-full bg-mint-500 scale-0 group-hover:scale-100 transition-transform" />
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="space-y-8"
          >
            <h3 className="text-xs font-black uppercase tracking-[0.2em] text-mint-400">{t.nav.services}</h3>
            <ul className="space-y-4">
              {[
                { az: 'Excimer laser', ru: 'Эксимер-лазер', en: 'Excimer Laser' },
                { az: 'Katarakta əməliyyatı', ru: 'Операция катаракты', en: 'Cataract Surgery' },
                { az: 'Qlaukoma müalicəsi', ru: 'Лечение глаукомы', en: 'Glaucoma Treatment' },
                { az: 'Retina əməliyyatları', ru: 'Операции на сетчатке', en: 'Retinal Surgeries' }
              ].map((service, i) => (
                <li key={i}>
                  <a href="#services" className="text-gray-400 hover:text-white transition-colors text-base font-bold tracking-tight inline-flex items-center gap-2 group">
                    <span className="w-1.5 h-1.5 rounded-full bg-mint-500 scale-0 group-hover:scale-100 transition-transform" />
                    {service[locale as keyof typeof service] || service.en}
                  </a>
                </li>
              ))}
            </ul>
          </motion.div>

          {/* Contact Details */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.3 }}
            className="space-y-8"
          >
            <h3 className="text-xs font-black uppercase tracking-[0.2em] text-mint-400">{t.footer.contact_us}</h3>
            <ul className="space-y-6">
              <li className="flex items-start gap-4 group">
                <div className="w-10 h-10 glass-dark rounded-xl flex items-center justify-center group-hover:bg-mint-500/20 transition-colors">
                  <MapPin className="w-5 h-5 text-clinic-primary" />
                </div>
                <div className="space-y-1">
                  <span className="block text-xs font-black uppercase tracking-widest text-gray-500">Address</span>
                  <span className="text-gray-300 text-sm font-bold leading-relaxed">{getClinicAddress(locale)}</span>
                </div>
              </li>
              <li className="flex items-start gap-4 group">
                <div className="w-10 h-10 glass-dark rounded-xl flex items-center justify-center group-hover:bg-mint-500/20 transition-colors">
                  <Phone className="w-5 h-5 text-clinic-primary" />
                </div>
                <div className="space-y-1">
                  <span className="block text-xs font-black uppercase tracking-widest text-gray-500">Phone</span>
                  <a href={`tel:${clinicInfo.phones[0].replace(/\s/g, '')}`} className="text-gray-300 hover:text-white transition-colors text-sm font-bold">
                    {clinicInfo.phones[0]}
                  </a>
                </div>
              </li>
              <li className="flex items-start gap-4 group">
                <div className="w-10 h-10 glass-dark rounded-xl flex items-center justify-center group-hover:bg-mint-500/20 transition-colors">
                  <Mail className="w-5 h-5 text-clinic-primary" />
                </div>
                <div className="space-y-1">
                  <span className="block text-xs font-black uppercase tracking-widest text-gray-500">Email</span>
                  <a href={`mailto:${clinicInfo.email}`} className="text-gray-300 hover:text-white transition-colors text-sm font-bold">
                    {clinicInfo.email}
                  </a>
                </div>
              </li>
            </ul>
          </motion.div>
        </div>

        {/* Bottom Attribution Bar */}
        <div className="pt-12 border-t border-white/5 flex flex-col md:flex-row items-center justify-between gap-8">
          <div className="flex flex-col md:flex-row items-center gap-8">
            <p className="text-gray-500 text-xs font-black uppercase tracking-widest">
              © {currentYear} {getClinicName(locale)}
            </p>
            <div className="flex items-center gap-4 text-xs font-black uppercase tracking-widest text-gray-600">
              <a href="#" className="hover:text-mint-400 transition-colors">Privacy Policy</a>
              <span className="w-1 h-1 bg-gray-800 rounded-full" />
              <a href="#" className="hover:text-mint-400 transition-colors">Terms of Service</a>
            </div>
          </div>

          <div className="flex items-center gap-2 px-4 py-2 glass-dark rounded-full">
            <Heart className="w-3 h-3 text-red-500 fill-red-500 animate-pulse" />
            <span className="text-[10px] font-black uppercase tracking-widest text-gray-400">
              Handcrafted by <span className="text-white hover:text-clinic-primary cursor-pointer transition-colors">Baysart</span>
            </span>
            <ExternalLink className="w-2 h-2 text-gray-600" />
          </div>
        </div>
      </div>
    </footer>
  );
}