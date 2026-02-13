import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Briz-L Göz Klinikası | Peşəkar Göz Sağlamlığı Xidmətləri',
  description: 'Briz-L Göz Klinikası - Müasir texnologiyalar və peşəkar həkimlərlə göz sağlamlığı xidmətləri. Katarakta, Excimer laser, Qlaukoma əməliyyatları.',
  keywords: 'göz klinikası, oftalmologiya, katarakta, excimer laser, qlaukoma, göz əməliyyatı, Bakı, Azərbaycan',
  authors: [{ name: 'Briz-L Clinic' }],
  openGraph: {
    title: 'Briz-L Göz Klinikası',
    description: 'Müasir texnologiyalar və peşəkar həkimlərlə göz sağlamlığı xidmətləri',
    type: 'website',
    locale: 'az_AZ',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="az" className="scroll-smooth">
      <body className="antialiased">{children}</body>
    </html>
  )
}