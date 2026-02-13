'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Menu, X, Phone, Globe } from 'lucide-react';
import { translations, locales, Locale, clinicInfo } from '@/lib/i18n';

interface HeaderProps {
  locale: Locale;
  setLocale: (locale: Locale) => void;
}

export default function Header({ locale, setLocale }: HeaderProps) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isLangOpen, setIsLangOpen] = useState(false);
  const t = translations[locale];

  const navItems = [
    { href: '#about', label: t.nav.about },
    { href: '#services', label: t.nav.services },
    { href: '#doctors', label: t.nav.doctors },
    { href: '#contact', label: t.nav.contact },
  ];

  const langLabels: Record<Locale, string> = {
    az: 'AZ',
    ru: 'RU',
    en: 'EN',
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-md shadow-sm">
      <div className="container-custom">
        <div className="flex items-center justify-between h-16 md:h-20">
          {/* Logo */}
          <a href="#" className="flex items-center gap-2">
            <img 
              src="/brizl.logo.png" 
              alt="Briz-L Clinic" 
              className="h-8 md:h-10 w-auto"
            />
            <span className="text-xl font-bold text-clinic-dark hidden sm:block">
              Briz-L
            </span>
          </a>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-8">
            {navItems.map((item) => (
              <a
                key={item.href}
                href={item.href}
                className="text-gray-600 hover:text-clinic-primary transition-colors font-medium"
              >
                {item.label}
              </a>
            ))}
          </nav>

          {/* Right Side Actions */}
          <div className="flex items-center gap-3">
            {/* Language Switcher */}
            <div className="relative">
              <button
                onClick={() => setIsLangOpen(!isLangOpen)}
                className="flex items-center gap-1 px-3 py-2 text-gray-600 hover:text-clinic-primary transition-colors"
              >
                <Globe className="w-4 h-4" />
                <span className="text-sm font-medium">{langLabels[locale]}</span>
              </button>
              
              <AnimatePresence>
                {isLangOpen && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="absolute right-0 top-full mt-1 bg-white rounded-lg shadow-lg border border-gray-100 overflow-hidden"
                  >
                    {locales.map((lang) => (
                      <button
                        key={lang}
                        onClick={() => {
                          setLocale(lang);
                          setIsLangOpen(false);
                        }}
                        className={`block w-full px-4 py-2 text-left text-sm hover:bg-mint-light transition-colors ${
                          locale === lang ? 'text-clinic-primary font-medium' : 'text-gray-600'
                        }`}
                      >
                        {langLabels[lang]}
                      </button>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* CTA Button */}
            <a
              href={clinicInfo.whatsapp}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-mint hidden sm:flex items-center gap-2 text-sm"
            >
              <Phone className="w-4 h-4" />
              {t.nav.booking}
            </a>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="md:hidden p-2 text-gray-600 hover:text-clinic-primary transition-colors"
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        <AnimatePresence>
          {isMenuOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="md:hidden overflow-hidden"
            >
              <nav className="py-4 space-y-2">
                {navItems.map((item) => (
                  <a
                    key={item.href}
                    href={item.href}
                    onClick={() => setIsMenuOpen(false)}
                    className="block px-4 py-3 text-gray-600 hover:text-clinic-primary hover:bg-mint-light rounded-lg transition-colors font-medium"
                  >
                    {item.label}
                  </a>
                ))}
                <a
                  href={clinicInfo.whatsapp}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block mx-4 mt-4 btn-mint text-center"
                >
                  {t.nav.booking}
                </a>
              </nav>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </header>
  );
}