'use client'

import { motion } from 'framer-motion'
import { Phone, Mail, MapPin, Instagram, Facebook, Clock } from 'lucide-react'
import { clinicInfo } from '@/lib/clinic-data'
import { useTranslations } from 'next-intl'
import { Link } from '@/i18n/navigation'

// Surgery IDs for footer
const footerServiceIds = ['excimer', 'cataract', 'pteregium', 'phacic', 'glaucoma']

const socials = [
  { name: 'Instagram', icon: Instagram, url: clinicInfo.social.instagram },
  { name: 'Facebook', icon: Facebook, url: clinicInfo.social.facebook },
  { name: 'WhatsApp', icon: Phone, url: clinicInfo.social.whatsapp },
]

export default function Footer() {
  const t = useTranslations('footer')
  const tServices = useTranslations('services')
  const tNav = useTranslations('nav')

  return (
    <footer className="py-16 px-6 border-t border-mint/10">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10 mb-12">
          {/* Brand */}
          <div className="md:col-span-2">
            <Link
              href="/"
              className="inline-block font-display text-2xl font-semibold gradient-text mb-4"
            >
              {clinicInfo.name}
            </Link>
            <p className="text-gray-500 text-sm max-w-sm leading-relaxed mb-4">
              {t('description')}
            </p>
            
            {/* Map Links with Logos */}
            <div className="flex gap-3">
              <a
                href={clinicInfo.maps.google}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-4 py-2 glass border border-gray-200 rounded-lg text-sm text-gray-600 hover:border-mint/40 transition-colors"
              >
                <img 
                  src="/google-maps.svg.png" 
                  alt="Google Maps" 
                  className="w-5 h-5 object-contain"
                />
                Google Maps
              </a>
              <a
                href={clinicInfo.maps.waze}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-4 py-2 glass border border-gray-200 rounded-lg text-sm text-gray-600 hover:border-mint/40 transition-colors"
              >
                <img 
                  src="/waze.png" 
                  alt="Waze" 
                  className="w-5 h-5 object-contain"
                />
                Waze
              </a>
            </div>
          </div>

          {/* Services */}
          <div>
            <h4 className="font-medium text-gray-700 mb-4 text-sm">{tNav('services')}</h4>
            <ul className="space-y-3">
              {footerServiceIds.map((id) => (
                <li key={id}>
                  <a
                    href="#services"
                    className="text-gray-500 hover:text-mint text-sm transition-colors"
                  >
                    {tServices(`items.${id}.name`)}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="font-medium text-gray-700 mb-4 text-sm">{t('contact')}</h4>
            <ul className="space-y-3">
              <li>
                <a
                  href={`tel:${clinicInfo.phone.main}`}
                  className="text-gray-500 hover:text-mint text-sm transition-colors inline-flex items-center gap-2"
                >
                  <Phone className="w-4 h-4" />
                  {clinicInfo.phone.main}
                </a>
              </li>
              <li>
                <a
                  href={`tel:${clinicInfo.phone.secondary}`}
                  className="text-gray-500 hover:text-mint text-sm transition-colors inline-flex items-center gap-2"
                >
                  <Phone className="w-4 h-4" />
                  {clinicInfo.phone.secondary}
                </a>
              </li>
              <li>
                <a
                  href={clinicInfo.social.whatsapp}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-500 hover:text-mint text-sm transition-colors inline-flex items-center gap-2"
                >
                  <Phone className="w-4 h-4" />
                  WhatsApp
                </a>
              </li>
              <li>
                <a
                  href={`mailto:${clinicInfo.email}`}
                  className="text-gray-500 hover:text-mint text-sm transition-colors inline-flex items-center gap-2"
                >
                  <Mail className="w-4 h-4" />
                  {clinicInfo.email}
                </a>
              </li>
              <li className="text-gray-500 text-sm inline-flex items-center gap-2">
                <MapPin className="w-4 h-4" />
                {clinicInfo.address.street}
              </li>
              <li className="text-gray-500 text-sm inline-flex items-center gap-2">
                <Clock className="w-4 h-4" />
                {clinicInfo.hours.weekdays}
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
            © {new Date().getFullYear()} {clinicInfo.fullName}. {t('rights')}
          </p>
          <p className="text-gray-400 text-xs inline-flex items-center gap-1">
            <MapPin className="w-3 h-3" />
            {clinicInfo.address.full}
          </p>
        </div>
      </div>
    </footer>
  )
}