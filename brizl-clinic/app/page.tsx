'use client';

import { useState } from 'react';
import Header from '@/components/Header';
import Hero from '@/components/Hero';
import WhyChooseUs from '@/components/WhyChooseUs';
import Services from '@/components/Services';
import Doctors from '@/components/Doctors';
import Contact from '@/components/Contact';
import Footer from '@/components/Footer';
import { Locale } from '@/lib/i18n';

export default function Home() {
  const [locale, setLocale] = useState<Locale>('az');

  return (
    <>
      <Header locale={locale} setLocale={setLocale} />
      <main>
        <Hero locale={locale} />
        <WhyChooseUs locale={locale} />
        <Services locale={locale} />
        <Doctors locale={locale} />
        <Contact locale={locale} />
      </main>
      <Footer locale={locale} />
    </>
  );
}