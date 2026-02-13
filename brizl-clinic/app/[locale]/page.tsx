import Hero from '@/components/Hero'
import Services from '@/components/Services'
import Doctors from '@/components/Doctors'
import WhyChooseUs from '@/components/WhyChooseUs'
import BookingCTA from '@/components/BookingCTA'
import Location from '@/components/Location'
import Footer from '@/components/Footer'

export default function Home() {
  return (
    <main className="min-h-screen">
      <Hero />
      <Services />
      <Doctors />
      <WhyChooseUs />
      <BookingCTA />
      <Location />
      <Footer />
    </main>
  )
}