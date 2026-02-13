export const defaultLocale = 'az';

export const locales = ['az', 'ru', 'en'] as const;

export type Locale = (typeof locales)[number];

export const translations: Record<Locale, {
  nav: {
    about: string;
    services: string;
    doctors: string;
    contact: string;
    booking: string;
  };
  hero: {
    title: string;
    subtitle: string;
    cta_booking: string;
    cta_services: string;
  };
  services: {
    title: string;
    subtitle: string;
    learn_more: string;
    categories: {
      refractive: string;
      cataract: string;
      corneal: string;
      retinal: string;
      strabismus: string;
      glaucoma: string;
    };
  };
  doctors: {
    title: string;
    subtitle: string;
    book_appointment: string;
    chief_doctor: string;
  };
  whyUs: {
    title: string;
    subtitle: string;
    experience: string;
    patients: string;
    surgeries: string;
    doctors: string;
    modern_tech: string;
    certified: string;
    support: string;
  };
  contact: {
    title: string;
    subtitle: string;
    address: string;
    phone: string;
    working_hours: string;
    get_directions: string;
  };
  footer: {
    tagline: string;
    quick_links: string;
    contact_us: string;
    rights: string;
  };
}> = {
  az: {
    nav: {
      about: 'Haqqımızda',
      services: 'Xidmətlər',
      doctors: 'Həkimlər',
      contact: 'Əlaqə',
      booking: 'Randevu Al',
    },
    hero: {
      title: 'Göz sağlamlığınız bizim üçün önəmlidir',
      subtitle: 'Müasir texnologiyalar və peşəkar həkimlərlə göz xidmətləri',
      cta_booking: 'Randevu Al',
      cta_services: 'Xidmətlər',
    },
    services: {
      title: 'Xidmətlərimiz',
      subtitle: 'Briz-L Göz Klinikasında aparılan əməliyyatlar',
      learn_more: 'Ətraflı',
      categories: {
        refractive: 'Refraktiv',
        cataract: 'Katarakta',
        corneal: 'Buynuz qişa',
        retinal: 'Retina',
        strabismus: 'Çəplik',
        glaucoma: 'Qlaukoma',
      },
    },
    doctors: {
      title: 'Həkimlərimiz',
      subtitle: 'Peşəkar və təcrübəli oftalmoloq komandamız',
      book_appointment: 'Randevu Al',
      chief_doctor: 'Baş həkim',
    },
    whyUs: {
      title: 'Niyə Bizi Seçməlisiniz?',
      subtitle: 'Göz sağlamlığınız üçün ən yaxşı xidmət',
      experience: 'İl təcrübə',
      patients: 'Xəstə',
      surgeries: 'Əməliyyat',
      doctors: 'Həkim',
      modern_tech: 'Müasir Avadanlıqlar',
      certified: 'Sertifikatlı Mütəxəssislər',
      support: '7/7 Dəstək',
    },
    contact: {
      title: 'Əlaqə',
      subtitle: 'Bizimlə əlaqə saxlayın',
      address: 'Ünvan',
      phone: 'Telefon',
      working_hours: 'İş saatları',
      get_directions: 'Yol tarifi',
    },
    footer: {
      tagline: 'Göz sağlamlığınız bizim etimadımızdır',
      quick_links: 'Sürətli keçidlər',
      contact_us: 'Bizimlə əlaqə',
      rights: 'Bütün hüquqlar qorunur.',
    },
  },
  ru: {
    nav: {
      about: 'О нас',
      services: 'Услуги',
      doctors: 'Врачи',
      contact: 'Контакты',
      booking: 'Записаться',
    },
    hero: {
      title: 'Здоровье ваших глаз важно для нас',
      subtitle: 'Современные технологии и профессиональные врачи для ваших глаз',
      cta_booking: 'Записаться',
      cta_services: 'Услуги',
    },
    services: {
      title: 'Наши услуги',
      subtitle: 'Операции, проводимые в клинике Briz-L',
      learn_more: 'Подробнее',
      categories: {
        refractive: 'Рефрактивная',
        cataract: 'Катаракта',
        corneal: 'Роговица',
        retinal: 'Сетчатка',
        strabismus: 'Косоглазие',
        glaucoma: 'Глаукома',
      },
    },
    doctors: {
      title: 'Наши врачи',
      subtitle: 'Профессиональная и опытная команда офтальмологов',
      book_appointment: 'Записаться',
      chief_doctor: 'Главный врач',
    },
    whyUs: {
      title: 'Почему Выбирают Нас?',
      subtitle: 'Лучший сервис для здоровья ваших глаз',
      experience: 'Лет опыта',
      patients: 'Пациентов',
      surgeries: 'Операций',
      doctors: 'Врачей',
      modern_tech: 'Современное Оборудование',
      certified: 'Сертифицированные Специалисты',
      support: 'Поддержка 7/7',
    },
    contact: {
      title: 'Контакты',
      subtitle: 'Свяжитесь с нами',
      address: 'Адрес',
      phone: 'Телефон',
      working_hours: 'Часы работы',
      get_directions: 'Проложить маршрут',
    },
    footer: {
      tagline: 'Здоровье ваших глаз — наше доверие',
      quick_links: 'Быстрые ссылки',
      contact_us: 'Связаться с нами',
      rights: 'Все права защищены.',
    },
  },
  en: {
    nav: {
      about: 'About Us',
      services: 'Services',
      doctors: 'Doctors',
      contact: 'Contact',
      booking: 'Book Now',
    },
    hero: {
      title: 'Your Eye Health is Our Priority',
      subtitle: 'Modern technology and professional doctors for your eyes',
      cta_booking: 'Book Appointment',
      cta_services: 'Our Services',
    },
    services: {
      title: 'Our Services',
      subtitle: 'Surgeries performed at Briz-L Eye Clinic',
      learn_more: 'Learn More',
      categories: {
        refractive: 'Refractive',
        cataract: 'Cataract',
        corneal: 'Corneal',
        retinal: 'Retinal',
        strabismus: 'Strabismus',
        glaucoma: 'Glaucoma',
      },
    },
    doctors: {
      title: 'Our Doctors',
      subtitle: 'Professional and experienced ophthalmologist team',
      book_appointment: 'Book Appointment',
      chief_doctor: 'Chief Doctor',
    },
    whyUs: {
      title: 'Why Choose Us?',
      subtitle: 'The best service for your eye health',
      experience: 'Years Experience',
      patients: 'Patients',
      surgeries: 'Surgeries',
      doctors: 'Doctors',
      modern_tech: 'Modern Equipment',
      certified: 'Certified Specialists',
      support: '7/7 Support',
    },
    contact: {
      title: 'Contact Us',
      subtitle: 'Get in touch with us',
      address: 'Address',
      phone: 'Phone',
      working_hours: 'Working Hours',
      get_directions: 'Get Directions',
    },
    footer: {
      tagline: 'Your eye health is our trust',
      quick_links: 'Quick Links',
      contact_us: 'Contact Us',
      rights: 'All rights reserved.',
    },
  },
};

export const doctors = [
  {
    id: 1,
    name: 'Dr. İltifat Şərif',
    name_ru: 'Др. Ильтифат Шериф',
    name_en: 'Dr. İltifat Şərif',
    title: 'Baş həkim, Oftalmoloq',
    title_ru: 'Главный врач, Офтальмолог',
    title_en: 'Chief Doctor, Ophthalmologist',
    phone: '010 710 74 65',
    whatsapp: 'https://wa.me/994107107465',
    note: 'Müayinə qiyməti və qəbul saatları koordinator tərəfindən təsdiqlənir',
    isChief: true,
  },
  {
    id: 2,
    name: 'Dr. Emil Qafarlı',
    name_ru: 'Др. Эмиль Гафарлы',
    name_en: 'Dr. Emil Qafarlı',
    title: 'Oftalmoloq',
    title_ru: 'Офтальмолог',
    title_en: 'Ophthalmologist',
    phone: '051 844 76 21',
    whatsapp: 'https://wa.me/994518447621',
    note: 'Ümumi göz müayinəsi və konsultasiya',
    isChief: false,
  },
  {
    id: 3,
    name: 'Dr. Səbinə Əbiyeva',
    name_ru: 'Др. Сабина Абиевa',
    name_en: 'Dr. Səbinə Əbiyeva',
    title: 'Oftalmoloq',
    title_ru: 'Офтальмолог',
    title_en: 'Ophthalmologist',
    phone: '055 319 75 76',
    whatsapp: 'https://wa.me/994553197576',
    note: 'Əməliyyat qiymətləri yalnız müayinədən sonra təsdiqlənir',
    isChief: false,
  },
  {
    id: 4,
    name: 'Dr. Seymur Bayramov',
    name_ru: 'Др. Сеймуp Байрамов',
    name_en: 'Dr. Seymur Bayramov',
    title: 'Oftalmoloq',
    title_ru: 'Офтальмолог',
    title_en: 'Ophthalmologist',
    phone: '070 505 00 01',
    whatsapp: 'https://wa.me/994705050001',
    note: 'Göz müayinəsi və konsultasiya',
    isChief: false,
  },
];

export const surgeries = [
  {
    id: 1,
    name: 'Excimer laser',
    name_ru: 'Эксимер-лазер',
    name_en: 'Excimer Laser',
    description: 'Gözlük və kontakt linzalardan azad olmaq üçün lazer əməliyyatı',
    description_ru: 'Лазерная операция для освобождения от очков и контактных линз',
    description_en: 'Laser surgery to get rid of glasses and contact lenses',
    details: 'Yaxıngörmə, uzaqgörmə və astiqmatizmin korreksiyası',
    details_ru: 'Коррекция близорукости, дальнозоркости и астигматизма',
    details_en: 'Correction of myopia, hyperopia and astigmatism',
    category: 'refractive',
    icon: 'Eye',
  },
  {
    id: 2,
    name: 'Katarakta',
    name_ru: 'Катаракта',
    name_en: 'Cataract',
    description: 'Göz lensinin dəyişdirilməsi',
    description_ru: 'Замена хрусталика глаза',
    description_en: 'Eye lens replacement',
    details: 'Katarakta zamanı göz lensi dumanlı olur və görmə zəifləyir',
    details_ru: 'При катаракте хрусталик становится мутным и зрение ухудшается',
    details_en: 'In cataract, the lens becomes cloudy and vision deteriorates',
    category: 'cataract',
    icon: 'Eye',
  },
  {
    id: 3,
    name: 'Pteregium',
    name_ru: 'Птеригиум',
    name_en: 'Pterygium',
    description: 'Göz ağının üzərində əmələ gələn toxumanın təmizlənməsi',
    description_ru: 'Удаление ткани, образующейся на белке глаза',
    description_en: 'Removal of tissue forming on the white of the eye',
    details: 'Gözün ağ hissəsində və buynuz qişada əmələ gələn artıq toxuma',
    details_ru: 'Избыточная ткань на белке глаза и роговице',
    details_en: 'Excess tissue on the white of the eye and cornea',
    category: 'corneal',
    icon: 'Eye',
  },
  {
    id: 4,
    name: 'Phacic',
    name_ru: 'Факичные линзы',
    name_en: 'Phacic IOL',
    description: 'Gözə lens yerləşdirilməsi',
    description_ru: 'Установка линзы в глаз',
    description_en: 'Lens implantation in the eye',
    details: 'Yüksək dərəcəli görmə qüsurlarında süni lens',
    details_ru: 'Искусственная линза при высоких степенях нарушений зрения',
    details_en: 'Artificial lens for high-degree vision problems',
    category: 'refractive',
    icon: 'Eye',
  },
  {
    id: 5,
    name: 'Çəplik',
    name_ru: 'Косоглазие',
    name_en: 'Strabismus',
    description: 'Göz əzələlərinin düzəldilməsi',
    description_ru: 'Исправление мышц глаза',
    description_en: 'Eye muscle correction',
    details: 'Gözlərin düz baxmaması probleminin həlli',
    details_ru: 'Решение проблемы неправильного положения глаз',
    details_en: 'Solution for misaligned eyes',
    category: 'strabismus',
    icon: 'Eye',
  },
  {
    id: 6,
    name: 'Cross linking',
    name_ru: 'Кросс-линкинг',
    name_en: 'Cross Linking',
    description: 'Buynuz qişanın möhkəmləndirilməsi',
    description_ru: 'Укрепление роговицы',
    description_en: 'Corneal strengthening',
    details: 'Keratokonus xəstəliyində buynuz qişanı möhkəmləndirmək',
    details_ru: 'Укрепление роговицы при кератоконусе',
    details_en: 'Strengthening cornea in keratoconus',
    category: 'corneal',
    icon: 'Eye',
  },
  {
    id: 7,
    name: 'Arqon laser',
    name_ru: 'Аргоновый лазер',
    name_en: 'Argon Laser',
    description: 'Göz dibinin lazer müalicəsi',
    description_ru: 'Лазерное лечение глазного дна',
    description_en: 'Laser treatment of the fundus',
    details: 'Retina problemlərində, şəkərli diabet, yırtıq hallarda',
    details_ru: 'При проблемах сетчатки, диабете, разрывах',
    details_en: 'For retinal problems, diabetes, tears',
    category: 'retinal',
    icon: 'Eye',
  },
  {
    id: 8,
    name: 'YAG laser',
    name_ru: 'YAG лазер',
    name_en: 'YAG Laser',
    description: 'Katarakta sonrası kapsul təmizlənməsi',
    description_ru: 'Очистка капсулы после катаракты',
    description_en: 'Capsule cleaning after cataract',
    details: 'Katarakta əməliyyatından sonra kapsul dumanlanarsa',
    details_ru: 'Если капсула помутнела после операции катаракты',
    details_en: 'If capsule becomes cloudy after cataract surgery',
    category: 'cataract',
    icon: 'Eye',
  },
  {
    id: 9,
    name: 'Avastin',
    name_ru: 'Авастин',
    name_en: 'Avastin',
    description: 'Göz dibinə vurulan iynə müalicəsi',
    description_ru: 'Инъекция в глазное дно',
    description_en: 'Injection treatment to the fundus',
    details: 'Makula degenerasiyası, diabetik retinopatiya',
    details_ru: 'Макулярная дегенерация, диабетическая ретинопатия',
    details_en: 'Macular degeneration, diabetic retinopathy',
    category: 'retinal',
    icon: 'Syringe',
  },
  {
    id: 10,
    name: 'Qlaukoma',
    name_ru: 'Глаукома',
    name_en: 'Glaucoma',
    description: 'Qlaukoma müalicəsi üçün əməliyyat',
    description_ru: 'Операция для лечения глаукомы',
    description_en: 'Surgery for glaucoma treatment',
    details: 'Göz daxili təzyiqin azaldılması',
    details_ru: 'Снижение внутриглазного давления',
    details_en: 'Reducing intraocular pressure',
    category: 'glaucoma',
    icon: 'Eye',
  },
];

export const clinicInfo = {
  name: 'Briz-L Göz Klinikası',
  name_ru: 'Клиника Глаз Briz-L',
  name_en: 'Briz-L Eye Clinic',
  address: 'Maqsud Alizade 46B, Bakı, Azərbaycan',
  address_ru: 'Максуд Ализаде 46B, Баку, Азербайджан',
  address_en: 'Maqsud Alizade 46B, Baku, Azerbaijan',
  phones: ['+994 12 541 19 00', '+994 12 541 24 00'],
  whatsapp: 'https://wa.me/994555512400',
  email: 'info@briz-l.az',
  mapsUrl: 'https://www.google.com/maps?q=40.401955867990424,49.83970805339595',
  wazeUrl: 'https://waze.com/ul?ll=40.401955867990424,49.83970805339595&navigate=yes',
  workingHours: {
    az: 'Həftə içi: 09:00 - 18:00, Şənbə: 09:00 - 14:00',
    ru: 'Будни: 09:00 - 18:00, Суббота: 09:00 - 14:00',
    en: 'Weekdays: 09:00 - 18:00, Saturday: 09:00 - 14:00',
  },
};

export function getTranslation(locale: Locale) {
  return translations[locale] || translations[defaultLocale];
}

export function getDoctorName(doctor: typeof doctors[0], locale: Locale) {
  switch (locale) {
    case 'ru':
      return doctor.name_ru;
    case 'en':
      return doctor.name_en;
    default:
      return doctor.name;
  }
}

export function getDoctorTitle(doctor: typeof doctors[0], locale: Locale) {
  switch (locale) {
    case 'ru':
      return doctor.title_ru;
    case 'en':
      return doctor.title_en;
    default:
      return doctor.title;
  }
}

export function getSurgeryName(surgery: typeof surgeries[0], locale: Locale) {
  switch (locale) {
    case 'ru':
      return surgery.name_ru;
    case 'en':
      return surgery.name_en;
    default:
      return surgery.name;
  }
}

export function getSurgeryDescription(surgery: typeof surgeries[0], locale: Locale) {
  switch (locale) {
    case 'ru':
      return surgery.description_ru;
    case 'en':
      return surgery.description_en;
    default:
      return surgery.description;
  }
}

export function getSurgeryDetails(surgery: typeof surgeries[0], locale: Locale) {
  switch (locale) {
    case 'ru':
      return surgery.details_ru;
    case 'en':
      return surgery.details_en;
    default:
      return surgery.details;
  }
}

export function getClinicName(locale: Locale) {
  switch (locale) {
    case 'ru':
      return clinicInfo.name_ru;
    case 'en':
      return clinicInfo.name_en;
    default:
      return clinicInfo.name;
  }
}

export function getClinicAddress(locale: Locale) {
  switch (locale) {
    case 'ru':
      return clinicInfo.address_ru;
    case 'en':
      return clinicInfo.address_en;
    default:
      return clinicInfo.address;
  }
}

export function getWorkingHours(locale: Locale) {
  return clinicInfo.workingHours[locale] || clinicInfo.workingHours.az;
}