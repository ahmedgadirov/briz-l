import { MetadataRoute } from 'next'

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://briz-l.baysart.com'
  const locales = ['az', 'en', 'ru']
  
  const routes = [
    '',
  ]
  
  const sitemapEntries: MetadataRoute.Sitemap = []
  
  // Add localized routes
  locales.forEach((locale) => {
    routes.forEach((route) => {
      sitemapEntries.push({
        url: `${baseUrl}/${locale}${route}`,
        lastModified: new Date(),
        changeFrequency: 'weekly',
        priority: route === '' ? 1 : 0.8,
        alternates: {
          languages: {
            az: `${baseUrl}/az${route}`,
            en: `${baseUrl}/en${route}`,
            ru: `${baseUrl}/ru${route}`,
          },
        },
      })
    })
  })
  
  return sitemapEntries
}