import type { Metadata } from 'next'
import { Inter, Space_Grotesk } from 'next/font/google'
import Script from 'next/script'
import './globals.css'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
})

const spaceGrotesk = Space_Grotesk({
  subsets: ['latin'],
  variable: '--font-space-grotesk',
})

export const metadata: Metadata = {
  metadataBase: new URL('https://briz-l.baysart.com'),
  title: {
    default: 'Briz-L Eye Clinic | Professional Eye Care Services in Azerbaijan',
    template: '%s | Briz-L Eye Clinic'
  },
  description: 'Briz-L Eye Clinic - Leading ophthalmology center in Baku, Azerbaijan. Expert eye care services including cataract surgery, Excimer laser vision correction, glaucoma treatment, and more. Modern technologies and experienced doctors.',
  keywords: ['eye clinic', 'ophthalmology', 'cataract surgery', 'excimer laser', 'glaucoma treatment', 'eye surgery', 'Baku eye clinic', 'Azerbaijan ophthalmology', 'LASIK Azerbaijan', 'eye doctor Baku', 'vision correction', 'eye examination', 'pterygium surgery', 'retina treatment', 'keratoconus treatment'],
  authors: [{ name: 'Briz-L Clinic' }],
  creator: 'Briz-L Eye Clinic',
  publisher: 'Briz-L Eye Clinic',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    title: 'Briz-L Eye Clinic | Professional Eye Care Services',
    description: 'Leading ophthalmology center in Baku, Azerbaijan. Modern technologies and experienced doctors for cataract surgery, Excimer laser vision correction, and comprehensive eye care.',
    url: 'https://briz-l.baysart.com',
    siteName: 'Briz-L Eye Clinic',
    images: [
      {
        url: '/brizl.logo.png',
        width: 1200,
        height: 630,
        alt: 'Briz-L Eye Clinic - Professional Eye Care in Baku',
      },
    ],
    locale: 'az_AZ',
    alternateLocale: ['en_US', 'ru_RU'],
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Briz-L Eye Clinic | Professional Eye Care Services',
    description: 'Leading ophthalmology center in Baku, Azerbaijan. Modern technologies and experienced doctors for comprehensive eye care.',
    images: ['/brizl.logo.png'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    google: 'G-EM2ZJEGZPS',
  },
  alternates: {
    canonical: 'https://briz-l.baysart.com',
    languages: {
      'az-AZ': 'https://briz-l.baysart.com/az',
      'en-US': 'https://briz-l.baysart.com/en',
      'ru-RU': 'https://briz-l.baysart.com/ru',
    },
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'MedicalClinic',
    name: 'Briz-L Eye Clinic',
    description: 'Leading ophthalmology center in Baku, Azerbaijan providing professional eye care services including cataract surgery, Excimer laser vision correction, and glaucoma treatment.',
    url: 'https://briz-l.baysart.com',
    logo: 'https://briz-l.baysart.com/brizl.logo.png',
    image: 'https://briz-l.baysart.com/brizl.logo.png',
    telephone: '+994-12-565-28-55',
    email: 'info@brizl.az',
    address: {
      '@type': 'PostalAddress',
      streetAddress: '28 May küç., 20',
      addressLocality: 'Baku',
      addressCountry: 'AZ',
      postalCode: 'AZ1000',
    },
    geo: {
      '@type': 'GeoCoordinates',
      latitude: 40.3695,
      longitude: 49.8350,
    },
    openingHoursSpecification: [
      {
        '@type': 'OpeningHoursSpecification',
        dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        opens: '09:00',
        closes: '18:00',
      },
      {
        '@type': 'OpeningHoursSpecification',
        dayOfWeek: ['Saturday'],
        opens: '09:00',
        closes: '14:00',
      },
    ],
    priceRange: '$$',
    medicalSpecialty: ['Ophthalmology', 'Eye Surgery', 'Vision Correction'],
    availableService: [
      {
        '@type': 'MedicalProcedure',
        name: 'Excimer Laser Vision Correction',
        description: 'LASIK surgery for correction of nearsightedness, farsightedness and astigmatism.',
      },
      {
        '@type': 'MedicalProcedure',
        name: 'Cataract Surgery',
        description: 'Phacoemulsification with artificial lens implantation.',
      },
      {
        '@type': 'MedicalProcedure',
        name: 'Glaucoma Treatment',
        description: 'Diagnosis, laser treatment and surgical intervention for glaucoma.',
      },
      {
        '@type': 'MedicalProcedure',
        name: 'Pterygium Surgery',
        description: 'Microsurgical removal of pterygium tissue.',
      },
      {
        '@type': 'MedicalProcedure',
        name: 'Retina Treatment',
        description: 'Argon laser and injection treatments for retinal conditions.',
      },
    ],
    sameAs: [
      'https://www.facebook.com/brizleyeclinic',
      'https://www.instagram.com/brizleyeclinic',
    ],
  }

  return (
    <html className={`${inter.variable} ${spaceGrotesk.variable}`}>
      <head>
        <link rel="icon" href="/brizl.logo.png" />
        <link rel="apple-touch-icon" href="/brizl.logo.png" />
        <meta name="theme-color" content="#0891b2" />
      </head>
      <body className="antialiased">
        <Script
          src="https://www.googletagmanager.com/gtag/js?id=G-EM2ZJEGZPS"
          strategy="afterInteractive"
        />
        <Script id="google-analytics" strategy="afterInteractive">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'G-EM2ZJEGZPS');
          `}
        </Script>
        <Script
          id="json-ld"
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
        <div className="mesh-gradient" />
        {children}
      </body>
    </html>
  )
}