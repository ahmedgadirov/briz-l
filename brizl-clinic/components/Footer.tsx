'use client'

import { motion } from 'framer-motion'
import { Phone, Mail, MapPin, Instagram, Facebook, Clock } from 'lucide-react'

const services = [
  { name: 'Katarakta', href: '#services' },
  { name: 'Excimer Laser', href: '#services' },
  { name: 'Qlaukoma', href: '#services' },
]

const socials = [
  { name: 'Instagram', icon: Instagram, url: 'https://instagram.com/brizlclinic' },
  { name: 'Facebook', icon: Facebook, url: 'https://facebook.com/brizlclinic' },
]

export default function Footer() {
  return (
    <footer className="py-16 px-6 border-t border-mint/10">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10 mb-12">
          {/* Brand */}
          <div className="md:col-span-2">
            <motion.a
              href="/"
              className="inline-block font-display text-2xl font-semibold gradient-text mb-4"
              whileHover={{ scale: 1.02 }}
            >
              Briz-L
            </motion.a>
            <p className="text-gray-500 text-sm max-w-sm leading-relaxed">
              Peşəkar göz sağlamlığı xidmətləri. Müasir texnologiyalar və təcrübəli həkimlər.
            </p>
          </div>

          {/* Services */}
          <div>
            <h4 className="font-medium text-gray-700 mb-4 text-sm">Xidmətlər</h4>
            <ul className="space-y-3">
              {services.map((service) => (
                <li key={service.name}>
                  <a
                    href={service.href}
                    className="text-gray-500 hover:text-mint text-sm transition-colors"
                  >
                    {service.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="font-medium text-gray-700 mb-4 text-sm">Əlaqə</h4>
            <ul className="space-y-3">
              <li>
                <a
                  href="tel:+994502222222"
                  className="text-gray-500 hover:text-mint text-sm transition-colors inline-flex items-center gap-2"
                >
                  <Phone className="w-4 h-4" />
                  +994 50 222 22 22
                </a>
              </li>
              <li>
                <a
                  href="mailto:info@brizl.az"
                  className="text-gray-500 hover:text-mint text-sm transition-colors inline-flex items-center gap-2"
                >
                  <Mail className="w-4 h-4" />
                  info@brizl.az
                </a>
              </li>
              <li className="text-gray-500 text-sm inline-flex items-center gap-2">
                <Clock className="w-4 h-4" />
                B.e - Şənbə: 09:00 - 18:00
              </li>
            </ul>
            <div className="flex gap-3 mt-4">
              {socials.map((social) => (
                <motion.a
                  key={social.name}
                  href={social.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                  className="w-10 h-10 rounded-xl bg-mint/10 hover:bg-mint/20 flex items-center justify-center text-mint transition-colors"
                  aria-label={social.name}
                >
                  <social.icon className="w-4 h-4" />
                </motion.a>
              ))}
            </div>
          </div>
        </div>

        {/* Bottom */}
        <div className="flex flex-col md:flex-row items-center justify-between pt-8 border-t border-mint/10 gap-4">
          <p className="text-gray-400 text-xs">
            © {new Date().getFullYear()} Briz-L Göz Klinikası. Bütün hüquqlar qorunur.
          </p>
          <p className="text-gray-400 text-xs inline-flex items-center gap-1">
            <MapPin className="w-3 h-3" />
            Bakı, Azərbaycan
          </p>
        </div>
      </div>
    </footer>
  )
}