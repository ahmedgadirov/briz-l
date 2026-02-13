'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Menu, X, Phone, Globe, ChevronDown } from 'lucide-react';
import { translations, locales, Locale, clinicInfo } from '@/lib/i18n';

interface HeaderProps {
  locale: Locale;
  setLocale: (locale: Locale) => void;
}

export default function Header({ locale, setLocale }: HeaderProps) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isLangOpen, setIsLangOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const t = translations[locale];

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

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
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${scrolled ? 'py-3' : 'py-6'
        }`}
    >
      <div className="container-custom">
        <div className={`transition-all duration-500 rounded-[24px] ${scrolled ? 'glass-premium px-6 shadow-xl' : 'bg-transparent px-2'
          }`}>
          <div className="flex items-center justify-between h-16 md:h-20">
            {/* Logo */}
            <a href="#" className="flex items-center gap-3 group">
              <div className="relative">
                <div className="absolute inset-0 bg-mint-400/20 blur-lg rounded-full group-hover:bg-mint-400/40 transition-colors" />
                <img
                  src="/brizl.logo.png"
                  alt="Briz-L Clinic"
                  className="h-10 md:h-12 w-auto relative z-10 drop-shadow-sm group-hover:scale-110 transition-transform duration-300"
                />
              </div>
              <span className="text-2xl font-black text-clinic-accent hidden sm:block font-display tracking-tight">
                Briz-L
              </span>
            </a>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center gap-10">
              {navItems.map((item) => (
                <a
                  key={item.href}
                  href={item.href}
                  className="text-gray-600 hover:text-clinic-primary transition-all font-bold text-sm uppercase tracking-widest relative group"
                >
                  {item.label}
                  <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-clinic-primary transition-all group-hover:w-full" />
                </a>
              ))}
            </nav>

            {/* Right Side Actions */}
            <div className="flex items-center gap-4">
              {/* Language Switcher */}
              <div className="relative">
                <button
                  onClick={() => setIsLangOpen(!isLangOpen)}
                  className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gray-50 hover:bg-mint-50 text-gray-700 hover:text-clinic-primary transition-all border border-transparent hover:border-mint-100"
                >
                  <Globe className="w-4 h-4" />
                  <span className="text-xs font-black uppercase tracking-tighter">{langLabels[locale]}</span>
                  <ChevronDown className={`w-3 h-3 transition-transform ${isLangOpen ? 'rotate-180' : ''}`} />
                </button>

                <AnimatePresence>
                  {isLangOpen && (
                    <motion.div
                      initial={{ opacity: 0, y: 10, scale: 0.95 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={{ opacity: 0, y: 10, scale: 0.95 }}
                      className="absolute right-0 top-full mt-2 w-32 glass-premium rounded-2xl shadow-2xl overflow-hidden p-1"
                    >
                      {locales.map((lang) => (
                        <button
                          key={lang}
                          onClick={() => {
                            setLocale(lang);
                            setIsLangOpen(false);
                          }}
                          className={`block w-full px-4 py-3 text-left text-xs font-bold tracking-widest rounded-xl transition-all ${locale === lang ? 'bg-mint-500 text-white shadow-lg shadow-mint-500/30' : 'text-gray-600 hover:bg-mint-50'
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
                className="btn-premium hidden sm:flex items-center gap-3 text-xs tracking-widest uppercase hover:scale-105"
              >
                <Phone className="w-4 h-4 animate-pulse" />
                {t.nav.booking}
              </a>

              {/* Mobile Menu Button */}
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="md:hidden p-3 bg-gray-50 rounded-xl text-gray-600 hover:text-clinic-primary transition-all"
              >
                {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Menu */}
        <AnimatePresence>
          {isMenuOpen && (
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="md:hidden mt-4"
            >
              <div className="glass-premium rounded-3xl p-6 shadow-2xl">
                <nav className="space-y-3">
                  {navItems.map((item) => (
                    <a
                      key={item.href}
                      href={item.href}
                      onClick={() => setIsMenuOpen(false)}
                      className="block px-4 py-4 text-gray-700 hover:text-white hover:bg-clinic-primary rounded-2xl transition-all font-bold uppercase tracking-widest text-sm"
                    >
                      {item.label}
                    </a>
                  ))}
                  <div className="pt-4 mt-4 border-t border-gray-100">
                    <a
                      href={clinicInfo.whatsapp}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn-premium flex items-center justify-center gap-3 uppercase tracking-widest text-sm"
                    >
                      <Phone className="w-5 h-5" />
                      {t.nav.booking}
                    </a>
                  </div>
                </nav>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </header>
  );
}