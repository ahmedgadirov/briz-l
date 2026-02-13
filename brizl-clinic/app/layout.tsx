import type { Metadata } from 'next'
import { Inter, Space_Grotesk } from 'next/font/google'
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
  title: 'Briz-L Göz Klinikası | Peşəkar Göz Sağlamlığı Xidmətləri',
  description: 'Briz-L Göz Klinikası - Müasir texnologiyalar və peşəkar həkimlərlə göz sağlamlığı xidmətləri. Katarakta, Excimer laser, Qlaukoma əməliyyatları.',
  keywords: ['göz klinikası', 'oftalmologiya', 'katarakta', 'excimer laser', 'qlaukoma', 'göz əməliyyatı', 'Bakı', 'Azərbaycan'],
  authors: [{ name: 'Briz-L Clinic' }],
  openGraph: {
    title: 'Briz-L Göz Klinikası',
    description: 'Müasir texnologiyalar və peşəkar həkimlərlə göz sağlamlığı xidmətləri',
    url: 'https://brizl.az',
    siteName: 'Briz-L Clinic',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="az" className={`${inter.variable} ${spaceGrotesk.variable}`}>
      <body className="antialiased">
        <div className="mesh-gradient" />
        {children}
      </body>
    </html>
  )
}