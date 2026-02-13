'use client';

import { motion } from 'framer-motion';
import { Eye, Phone, Mail, MapPin, Instagram, Facebook, Send } from 'lucide-react';
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
    <footer className="bg-clinic-dark text-white">
      <div className="container-custom py-16">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-10">
          {/* Brand */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <div className="flex items-center gap-2 mb-4">
              <div className="w-10 h-10 bg-clinic-primary rounded-lg flex items-center justify-center">
                <Eye className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold">Briz-L</span>
            </div>
            <p className="text-gray-400 text-sm mb-4">
              {t.footer.tagline}
            </p>
            <div className="flex gap-3">
              <a
                href="https://www.instagram.com/brizl_clinic/"
                target="_blank"
                rel="noopener noreferrer"
                className="w-10 h-10 bg-white/10 hover:bg-clinic-primary rounded-lg flex items-center justify-center transition-colors"
              >
                <Instagram className="w-5 h-5" />
              </a>
              <a
                href="#"
                className="w-10 h-10 bg-white/10 hover:bg-clinic-primary rounded-lg flex items-center justify-center transition-colors"
              >
                <Facebook className="w-5 h-5" />
              </a>
              <a
                href={clinicInfo.whatsapp}
                target="_blank"
                rel="noopener noreferrer"
                className="w-10 h-10 bg-white/10 hover:bg-green-500 rounded-lg flex items-center justify-center transition-colors"
              >
                <Send className="w-5 h-5" />
              </a>
            </div>
          </motion.div>

          {/* Quick Links */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
          >
            <h3 className="text-lg font-semibold mb-4">{t.footer.quick_links}</h3>
            <ul className="space-y-2">
              {quickLinks.map((link) => (
                <li key={link.href}>
                  <a
                    href={link.href}
                    className="text-gray-400 hover:text-clinic-primary transition-colors text-sm"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </motion.div>

          {/* Services */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
          >
            <h3 className="text-lg font-semibold mb-4">{t.nav.services}</h3>
            <ul className="space-y-2">
              <li>
                <a href="#services" className="text-gray-400 hover:text-clinic-primary transition-colors text-sm">
                  {locale === 'az' ? 'Excimer laser' : locale === 'ru' ? 'Эксимер-лазер' : 'Excimer Laser'}
                </a>
              </li>
              <li>
                <a href="#services" className="text-gray-400 hover:text-clinic-primary transition-colors text-sm">
                  {locale === 'az' ? 'Katarakta əməliyyatı' : locale === 'ru' ? 'Операция катаракты' : 'Cataract Surgery'}
                </a>
              </li>
              <li>
                <a href="#services" className="text-gray-400 hover:text-clinic-primary transition-colors text-sm">
                  {locale === 'az' ? 'Qlaukoma müalicəsi' : locale === 'ru' ? 'Лечение глаукомы' : 'Glaucoma Treatment'}
                </a>
              </li>
              <li>
                <a href="#services" className="text-gray-400 hover:text-clinic-primary transition-colors text-sm">
                  {locale === 'az' ? 'Retina əməliyyatları' : locale === 'ru' ? 'Операции на сетчатке' : 'Retinal Surgeries'}
                </a>
              </li>
            </ul>
          </motion.div>

          {/* Contact */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.3 }}
          >
            <h3 className="text-lg font-semibold mb-4">{t.footer.contact_us}</h3>
            <ul className="space-y-3">
              <li className="flex items-start gap-3">
                <MapPin className="w-5 h-5 text-clinic-primary flex-shrink-0 mt-0.5" />
                <span className="text-gray-400 text-sm">{getClinicAddress(locale)}</span>
              </li>
              <li>
                <a href={`tel:${clinicInfo.phones[0].replace(/\s/g, '')}`} className="flex items-center gap-3 text-gray-400 hover:text-clinic-primary transition-colors text-sm">
                  <Phone className="w-5 h-5 text-clinic-primary" />
                  {clinicInfo.phones[0]}
                </a>
              </li>
              <li>
                <a href={`mailto:${clinicInfo.email}`} className="flex items-center gap-3 text-gray-400 hover:text-clinic-primary transition-colors text-sm">
                  <Mail className="w-5 h-5 text-clinic-primary" />
                  {clinicInfo.email}
                </a>
              </li>
            </ul>
          </motion.div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-white/10">
        <div className="container-custom py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-gray-400 text-sm text-center md:text-left">
              © {currentYear} {getClinicName(locale)}. {t.footer.rights}
            </p>
            <p className="text-gray-500 text-xs">
              {locale === 'az' ? 'Dizayn və inkişaf' : locale === 'ru' ? 'Дизайн и разработка' : 'Design & Development'}: Baysart
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}