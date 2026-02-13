// Clinic data from domain.yml
// Briz-L Göz Klinikasi

export const clinicInfo = {
  name: 'Briz-L',
  fullName: 'Briz-L Göz Klinikası',
  phone: {
    main: '+994 12 541 19 00',
    secondary: '+994 12 541 24 00',
    whatsapp: '+994 55 551 24 00',
  },
  email: 'info@brizl.az',
  address: {
    street: 'Maqsud Alizade 46B',
    city: 'Bakı',
    country: 'Azərbaycan',
    full: 'Maqsud Alizade 46B, Bakı, Azərbaycan',
  },
  coordinates: {
    lat: 40.401955867990424,
    lng: 49.83970805339595,
  },
  maps: {
    google: 'https://www.google.com/maps?q=40.401955867990424,49.83970805339595',
    waze: 'https://waze.com/ul?ll=40.401955867990424,49.83970805339595&navigate=yes',
  },
  social: {
    instagram: 'https://instagram.com/brizlclinic',
    facebook: 'https://facebook.com/brizlclinic',
    whatsapp: 'https://wa.me/994555512400',
  },
  hours: {
    weekdays: '09:00 - 18:00',
    weekend: 'Qeyri-iş günü',
  },
}

export const doctors = [
  {
    id: 'iltifat',
    name: 'Dr. İltifat Şərif',
    title: 'Baş həkim, Oftalmoloq',
    phone: '010 710 74 65',
    whatsapp: 'https://wa.me/994107107465',
    description: 'Baş həkim, oftalmoqrafiya sahəsində ekspert',
  },
  {
    id: 'emil',
    name: 'Dr. Emil Qafarlı',
    title: 'Oftalmoloq',
    phone: '051 844 76 21',
    whatsapp: 'https://wa.me/994518447621',
    description: 'Ümumi göz müayinəsi və konsultasiya',
  },
  {
    id: 'sabina',
    name: 'Dr. Səbinə Əbiyeva',
    title: 'Oftalmoloq',
    phone: '055 319 75 76',
    whatsapp: 'https://wa.me/994553197576',
    description: 'Əməliyyat qiymətləri yalnız müayinədən sonra təsdiqlənir',
  },
  {
    id: 'seymur',
    name: 'Dr. Seymur Bayramov',
    title: 'Oftalmoloq',
    phone: '070 505 00 01',
    whatsapp: 'https://wa.me/994705050001',
    description: 'Göz müayinəsi və konsultasiya',
  },
]

export const surgeries = [
  {
    id: 'excimer',
    name: 'Excimer Laser',
    description: 'Gözlük və kontakt linzalardan azad olmaq üçün lazer əməliyyatı. Yaxıngörmə, uzaqgörmə və astiqmatizmin korreksiyası üçün istifadə olunur.',
    features: ['LASIK üsulu', 'Həssas korreksiya', 'Sürətli bərpa'],
  },
  {
    id: 'cataract',
    name: 'Katarakta (mirvari suyu)',
    description: 'Göz lensinin dəyişdirilməsi. Katarakta zamanı göz lensi dumanlı olur və görmə zəifləyir. Əməliyyat zamanı köhnə lens çıxarılır və yenisi yerləşdirilir.',
    features: ['Fako əməliyyat üsulu', 'Süni lens implantasiyası', 'Qısa bərpa dövrü'],
  },
  {
    id: 'pteregium',
    name: 'Pteregium',
    description: 'Göz ağının üzərində əmələ gələn toxumanın təmizlənməsi. Bu əməliyyat gözün ağ hissəsində və buynuz qişada əmələ gələn artıq toxumanın çıxarılması üçündür.',
    features: ['Mikrocərrahi üsul', 'Buynuz qişa qorunması', 'Minimal bərpa vaxtı'],
  },
  {
    id: 'phacic',
    name: 'Phacic Lens',
    description: 'Yüksək dərəcəli görmə qüsurlarında gözə süni lens yerləşdirmək üçün istifadə olunur.',
    features: ['Yüksək dioptriya', 'Reversiv prosedura', 'Qısa bərpa dövrü'],
  },
  {
    id: 'cesplik',
    name: 'Çəplik əməliyyatı',
    description: 'Göz əzələlərinin düzəldilməsi. Gözlərin düz baxmaması probleminin həlli üçündür.',
    features: ['Mikrocərrahi düzəliş', 'Fərdi yanaşma', 'Estetik nəticə'],
  },
  {
    id: 'cross_linking',
    name: 'Cross Linking (CCL)',
    description: 'Buynuz qişanın möhkəmləndirilməsi. Keratokonus xəstəliyində buynuz qişanı möhkəmləndirmək üçün istifadə olunur.',
    features: ['Keratokonus müalicəsi', 'Buynuz qişa möhkəmləndirmə', 'Proqressiv xəstəliklər'],
  },
  {
    id: 'argon',
    name: 'Arqon Laser (Green Laser)',
    description: 'Göz dibinin lazer müalicəsi. Retina problemlərində, şəkərli diabet, yırtıq və s. hallarda istifadə olunur.',
    features: ['Retina müalicəsi', 'Diabetik retinopatiya', 'Tez bərpa'],
  },
  {
    id: 'yag',
    name: 'YAG Laser',
    description: 'Katarakta əməliyyatından sonra kapsul təmizlənməsi. Katarakta əməliyyatından sonra kapsul dumanlanarsa, YAG lazer ilə təmizlənir.',
    features: ['Kapsulotomiya', 'Ağrısız prosedura', 'Tez nəticə'],
  },
  {
    id: 'avastin',
    name: 'Avastin',
    description: 'Göz dibinə vurulan iynə müalicəsi. Göz dibində yaş tipli makula degenerasiyası, diabetik retinopatiya və s. xəstəliklərdə istifadə olunur.',
    features: ['Anti-VEGF terapiya', 'Makula degenerasiyası', 'Diabetik retinopatiya'],
  },
  {
    id: 'glaucoma',
    name: 'Qlaukoma (qara su)',
    description: 'Qlaukoma diaqnostikası və müalicəsi. Gözdaxili təzyiqin normallaşdırılması.',
    features: ['Erkən diaqnostika', 'Lazer müalicəsi', 'Cərrahi müdaxilə'],
  },
]

export const whyChooseUs = [
  {
    title: 'Təcrübəli Həkimlər',
    description: 'Peşəkar və təcrübəli həkim heyəti',
    stat: '10+ il',
    statLabel: 'təcrübə',
  },
  {
    title: 'Müasir Texnologiyalar',
    description: 'Son texnologiya avadanlıqlar',
    stat: '5+',
    statLabel: 'lazer cihazı',
  },
  {
    title: 'Minlərlə Əməliyyat',
    description: 'Uğurla həyata keçirilmiş əməliyyatlar',
    stat: '5000+',
    statLabel: 'əməliyyat',
  },
  {
    title: 'Keyfiyyətli Xidmət',
    description: 'Fərdi yanaşma və qulluq',
    stat: '98%',
    statLabel: 'məmnuniyyət',
  },
]
