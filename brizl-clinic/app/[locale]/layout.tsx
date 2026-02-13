import { NextIntlClientProvider } from 'next-intl';
import { getMessages, getTranslations } from 'next-intl/server';
import { notFound } from 'next/navigation';
import { Providers } from '@/components/Providers';
import { routing } from '@/i18n/routing';
import type { Metadata } from 'next';

export async function generateMetadata({
  params
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  
  const titles: Record<string, string> = {
    az: 'Briz-L Göz Klinikası | Peşəkar Göz Sağlamlığı Xidmətləri',
    en: 'Briz-L Eye Clinic | Professional Eye Care Services',
    ru: 'Клиника Глаз Briz-L | Профессиональные Услуги по Уходу за Глазами'
  };
  
  const descriptions: Record<string, string> = {
    az: 'Briz-L Göz Klinikası - Bakıda aparıcı oftalmologiya mərkəzi. Katarakt cərrahiyyəsi, Excimer lazer görmə düzəlişi, qalauktor müalicəsi və daha çox peşəkar göz sağlamlığı xidmətləri.',
    en: 'Briz-L Eye Clinic - Leading ophthalmology center in Baku, Azerbaijan. Expert eye care services including cataract surgery, Excimer laser vision correction, glaucoma treatment, and more.',
    ru: 'Клиника Глаз Briz-L - Ведущий офтальмологический центр в Баку, Азербайджан. Профессиональные услуги по уходу за глазами, включая хирургию катаракты, лазерную коррекцию зрения и лечение глаукомы.'
  };

  return {
    title: {
      default: titles[locale] || titles.en,
      template: `%s | Briz-L Eye Clinic`
    },
    description: descriptions[locale] || descriptions.en,
    alternates: {
      canonical: `https://briz-l.baysart.com/${locale}`,
      languages: {
        'az-AZ': 'https://briz-l.baysart.com/az',
        'en-US': 'https://briz-l.baysart.com/en',
        'ru-RU': 'https://briz-l.baysart.com/ru',
      },
    },
    openGraph: {
      locale: locale === 'az' ? 'az_AZ' : locale === 'ru' ? 'ru_RU' : 'en_US',
      alternateLocale: locale === 'az' ? ['en_US', 'ru_RU'] : locale === 'en' ? ['az_AZ', 'ru_RU'] : ['az_AZ', 'en_US'],
    },
  };
}

export default async function LocaleLayout({
  children,
  params
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  
  if (!routing.locales.includes(locale as any)) {
    notFound();
  }
  
  const messages = await getMessages();

  return (
    <NextIntlClientProvider messages={messages}>
      <Providers>
        {children}
      </Providers>
    </NextIntlClientProvider>
  );
}