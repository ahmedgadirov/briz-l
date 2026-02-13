'use client'

import { useLocale } from 'next-intl';
import { usePathname, useRouter } from '@/i18n/navigation';
import { motion } from 'framer-motion';
import { Globe } from 'lucide-react';

const languages = [
  { code: 'az', name: 'AZ', fullName: 'Azərbaycan' },
  { code: 'ru', name: 'RU', fullName: 'Русский' },
  { code: 'en', name: 'EN', fullName: 'English' },
] as const;

export default function LanguageSwitcher() {
  const locale = useLocale();
  const router = useRouter();
  const pathname = usePathname();

  const handleLanguageChange = (newLocale: string) => {
    router.replace(pathname, { locale: newLocale });
  };

  return (
    <div className="flex items-center gap-1">
      <Globe className="w-4 h-4 text-gray-400" />
      {languages.map((lang) => (
        <motion.button
          key={lang.code}
          onClick={() => handleLanguageChange(lang.code)}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className={`px-2 py-1 text-sm font-medium rounded-md transition-all duration-200 ${
            locale === lang.code
              ? 'bg-mint/20 text-mint'
              : 'text-gray-500 hover:text-mint hover:bg-mint/10'
          }`}
        >
          {lang.name}
        </motion.button>
      ))}
    </div>
  );
}