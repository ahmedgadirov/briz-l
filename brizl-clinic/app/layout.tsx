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
  title: 'Briz-L Eye Clinic | Professional Eye Care Services',
  description: 'Briz-L Eye Clinic - Modern technologies and professional doctors for eye health services. Cataract, Excimer laser, Glaucoma surgeries.',
  keywords: ['eye clinic', 'ophthalmology', 'cataract', 'excimer laser', 'glaucoma', 'eye surgery', 'Baku', 'Azerbaijan'],
  authors: [{ name: 'Briz-L Clinic' }],
  openGraph: {
    title: 'Briz-L Eye Clinic',
    description: 'Modern technologies and professional doctors for eye health services',
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
    <html className={`${inter.variable} ${spaceGrotesk.variable}`}>
      <body className="antialiased">
        <div className="mesh-gradient" />
        {children}
      </body>
    </html>
  )
}