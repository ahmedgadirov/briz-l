"""
Briz-L Medical Knowledge Base
Comprehensive eye condition and surgery information
"""

# Official Surgery Names (as per clinic standards)
SURGERIES = {
    "excimer_laser": {
        "name": "Excimer laser",
        "description": "Gözlük və kontakt linzalardan azad olmaq üçün lazer əməliyyatı",
        "treats": ["yaxıngörmə", "uzaqgörmə", "astiqmatizm"],
        "keywords": ["lazer", "excimer", "eksimer", "gözlük", "lens", "yaxın görməmək", "uzaq görməmək"],
        "simple_explanation": "Bu əməliyyat gözünüzün buynuz qişasını düzəldir və siz gözlüksüz görə bilərsiniz.",
        "expert_explanation": "Excimer laser ilə buynuz qişanın refraksiya gücü dəyişdirilir. LASIK və PRK metodları mövcuddur."
    },
    "katarakta": {
        "name": "Katarakta (mirvari suyu)",
        "description": "Göz lensinin dəyişdirilməsi əməliyyatı",
        "treats": ["dumanlı görmə", "katarakta", "lens dumanlığı"],
        "keywords": ["dumanlı", "duman", "katarakta", "mirvari", "lens", "ağ göz", "köhnəlik"],
        "simple_explanation": "Gözünüzdə lens var, o dumanlıdır. Biz köhnə lensi çıxarıb yeni şəffaf lens qoyuruq.",
        "expert_explanation": "Fakoemulsifikasiya ilə IOL implantasiyası. Monofocal, multifocal və ya toric IOL seçimi mövcuddur."
    },
    "pteregium": {
        "name": "Pteregium",
        "description": "Göz ağının üzərində əmələ gələn toxumanın təmizlənməsi",
        "treats": ["göz ağında ət", "göz ağında ləkə", "pteregium"],
        "keywords": ["ət", "göz əti", "göz ağında", "ləkə", "toxuma", "pteregium", "pterigy"],
        "simple_explanation": "Gözünüzün ağ hissəsində artıq toxuma əmələ gəlib, biz onu təmizləyirik.",
        "expert_explanation": "Konjonktival pteregium ekssizyası və müvafiq rekonstruksiya."
    },
    "phacic": {
        "name": "Phacic",
        "description": "Gözə süni lens yerləşdirilməsi",
        "treats": ["yüksək miop", "yüksək refraktiv xəta"],
        "keywords": ["phacic", "fakik", "ICL", "lens implant", "yüksək yaxıngörmə"],
        "simple_explanation": "Təbii lensinizi saxlayaraq, əlavə bir lens gözünüzə yerləşdiririk.",
        "expert_explanation": "Fakik IOL implantasiyası - təbii lens saxlanılır, anterior və ya posterior kameraya implant yerləşdirilir."
    },
    "ceplik": {
        "name": "Çəplik",
        "description": "Göz əzələlərinin düzəldilməsi",
        "treats": ["çəplik", "strabismus", "göz əyri baxır"],
        "keywords": ["çəp", "cep", "əyri göz", "çəp baxmaq", "strabizm", "strabismus"],
        "simple_explanation": "Gözünüz düz baxmır, biz göz əzələlərini düzəldirik ki düz baxsın.",
        "expert_explanation": "Strabismus cərrahiyyəsi - ekstraokulyar əzələlərin reseksiya və ya sessiya əməliyyatı."
    },
    "cross_linking": {
        "name": "Cross linking",
        "description": "Buynuz qişanın möhkəmləndirilməsi",
        "treats": ["keratokonus", "buynuz qişa zəifliyi", "nazik buynuz qişa"],
        "keywords": ["cross", "linking", "ccl", "keratokon", "keratokonus", "konusa", "buynuz qişa"],
        "simple_explanation": "Gözünüzün şəffaf pərdəsi (buynuz qişa) zəifdir, biz onu möhkəmləndiririk.",
        "expert_explanation": "Korneal kollagen cross-linking (CXL) - riboflavin və UVA işığı ilə korneal kollagenin möhkəmləndirilməsi."
    },
    "argon_laser": {
        "name": "Arqon laser",
        "description": "Göz dibinin lazer müalicəsi",
        "treats": ["retina problemi", "diabetik retinopatiya", "retina yırtığı"],
        "keywords": ["arqon", "argon", "green laser", "yaşıl lazer", "göz dibi", "retina", "diabet", "şəkər"],
        "simple_explanation": "Gözünüzün arxasında (göz dibi) problem var, lazer ilə müalicə edirik.",
        "expert_explanation": "Arqon laser fotokoaqulyasiya - retinal yırtıq, diabetik retinopatiya, venoz okkluziya müalicəsi."
    },
    "yag_laser": {
        "name": "YAG laser",
        "description": "Katarakta əməliyyatından sonra kapsul təmizlənməsi",
        "treats": ["posterior kapsul opasifikasiyası", "PCO", "katarakta sonrası dumanlıq"],
        "keywords": ["yag", "yaq", "kapsul", "katarakta sonra", "yenə dumanlı"],
        "simple_explanation": "Katarakta əməliyyatından sonra yenə dumanlıq olarsa, onu lazer ilə təmizləyirik.",
        "expert_explanation": "Nd:YAG laser posterior kapsulotomiya - PCO müalicəsi."
    },
    "avastin": {
        "name": "Avastin",
        "description": "Göz dibinə vurulan iynə müalicəsi",
        "treats": ["makula degenerasiyası", "diabetik retinopatiya", "venoz okkluziya"],
        "keywords": ["avastin", "iynə", "göz dibi iynə", "intravitreal", "makula", "diabet göz"],
        "simple_explanation": "Göz dibində damarlar problem yaradır, dərmanlı iynə vuraraq müalicə edirik.",
        "expert_explanation": "İntravitreal anti-VEGF iynə (bevacizumab) - neovaskulyar AMD, DME, RVO müalicəsi."
    },
    "qlaukoma": {
        "name": "Qlaukoma (qara su)",
        "description": "Göz təzyiqinin azaldılması əməliyyatı",
        "treats": ["qlaukoma", "göz təzyiqi", "qara su"],
        "keywords": ["qlaukoma", "glaukoma", "qara su", "təzyiq", "göz təzyiqi", "göz ağrısı"],
        "simple_explanation": "Gözünüzdə təzyiq yüksəkdir, əməliyyatla təzyiqi azaldırıq.",
        "expert_explanation": "Trabekulektomiya, şunt implantasiyası və ya minimal invaziv qlaukoma cərrahiyyəsi (MIGS)."
    }
}

# Symptom to Surgery/Condition Mapping
SYMPTOM_MAPPING = {
    # Vision problems - Distance
    "uzağı görmürəm": {
        "conditions": ["yaxıngörmə (myopia)"],
        "surgeries": ["Excimer laser", "Phacic"],
        "questions": ["Nə vaxtdan?", "Yaşınız neçədir?", "Gözlük istifadə edirsiniz?"],
        "urgency": "routine"
    },
    "uzaq görməmək": {
        "conditions": ["yaxıngörmə (myopia)"],
        "surgeries": ["Excimer laser", "Phacic"],
        "questions": ["Dərəcəsi nə qədərdir?", "Gözlük və ya lens istifadə edirsiniz?"],
        "urgency": "routine"
    },
    
    # Vision problems - Near
    "yaxını görmürəm": {
        "conditions": ["uzaqgörmə", "presbiopiya"],
        "surgeries": ["Excimer laser"],
        "questions": ["Yaşınız?", "Uzağı yaxşı görürsünüz?"],
        "urgency": "routine"
    },
    
    # Cloudy/blurry vision
    "dumanlı görürəm": {
        "conditions": ["Katarakta", "buynuz qişa problemi"],
        "surgeries": ["Katarakta (mirvari suyu)", "Cross linking"],
        "questions": ["Yaşınız?", "Tədricənmi dumanlıdır?", "İşıqdan narahatmısınız?"],
        "urgency": "urgent"
    },
    "bulanıq": {
        "conditions": ["Katarakta", "refraktiv xəta"],
        "surgeries": ["Katarakta (mirvari suyu)", "Excimer laser"],
        "questions": ["Səbəh və ya axşam daha pisdir?"],
        "urgency": "routine"
    },
    
    # Red eye
    "qırmızı göz": {
        "conditions": ["konjonktivit", "uveitis", "qlaukoma hücumu"],
        "surgeries": [],
        "questions": ["Ağrı var?", "İşıqdan qorxursunuz?", "Axıntı var?"],
        "urgency": "urgent"
    },
    
    # Eye pain
    "göz ağrısı": {
        "conditions": ["qlaukoma hücumu", "uveitis", "keratit"],
        "surgeries": ["Qlaukoma (qara su)"],
        "questions": ["TƏCİLİ! Ağrı nə qədər güclüdür?", "Görmə azalıb?", "Göz qırmızıdır?"],
        "urgency": "emergency"
    },
    
    # Growth on eye
    "göz ağında ət": {
        "conditions": ["Pteregium", "pinguekula"],
        "surgeries": ["Pteregium"],
        "questions": ["Böyüyür?", "Görmə problem yaradır?", "Qırmızılaşma var?"],
        "urgency": "routine"
    },
    
    # Strabismus
    "çəp göz": {
        "conditions": ["strabismus"],
        "surgeries": ["Çəplik"],
        "questions": ["Uşaqlıqdan?", "Hər zaman çəpdir?", "İkiqat görmə var?"],
        "urgency": "routine"
    },
    
    # Diabetes-related
    "şəkərli diabetim var": {
        "conditions": ["diabetik retinopatiya"],
        "surgeries": ["Arqon laser", "Avastin"],
        "questions": ["Görmə zəifləməsi var?", "Neçə ildir diabet xəstəsisiz?"],
        "urgency": "urgent"
    },
    
    # Flashes and floaters
    "işıq çaxması": {
        "conditions": ["retina yırtığı", "posterior vitreoz detaçman"],
        "surgeries": ["Arqon laser"],
        "questions": ["TƏCİLİ! Nə vaxt başladı?", "Kor nöqtə var?", "Görmə azalması var?"],
        "urgency": "emergency"
    },
    
    # High eye pressure
    "göz təzyiqi": {
        "conditions": ["qlaukoma"],
        "surgeries": ["Qlaukoma (qara su)"],
        "questions": ["Təzyiq nə qədərdir?", "Ağrı var?", "Ailədə qlaukoma var?"],
        "urgency": "urgent"
    }
}

# Medical terminology detection - knowledge level assessment
TERMINOLOGY_LEVELS = {
    "beginner": [
        "görmürəm", "ağrıyır", "dumanlı", "qırmızı", "ət", "çəp",
        "pis", "problem", "nə edim", "bilmirəm", "köməək"
    ],
    "intermediate": [
        "katarakta", "lazer", "əməliyyat", "müayinə", "nömrə",
        "diabet", "təzyiq", "gözlük", "lens"
    ],
    "expert": [
        "IOL", "fakoemulsifikasiya", "retinopatiya", "makula",
        "keratokonus", "astiqmatizm", "refraktiv", "intravitreal",
        "kornea", "vitreoz", "okkluziya", "PCO"
    ]
}

# Urgency classification
URGENCY_LEVELS = {
    "emergency": {
        "response": "⚠️ TƏCİLİ VƏZIYYƏT! Dərhal klinikamıza gəlməlisiniz!",
        "action": "immediate_contact",
        "timeframe": "Dərhal - 1 saat içində"
    },
    "urgent": {
        "response": "Bu problemi tez həll etmək lazımdır. Ən qısa zamanda müayinə olun.",
        "action": "schedule_soon",
        "timeframe": "1-3 gün içində"
    },
    "routine": {
        "response": "Müayinə olunmaq məsləhətdir. Vaxt ayırıb klinikamıza gələ bilərsiniz.",
        "action": "schedule_appointment",
        "timeframe": "1-2 həftə içində"
    }
}

def get_surgery_info(surgery_key: str, knowledge_level: str = "beginner") -> dict:
    """Get surgery information adapted to user's knowledge level"""
    if surgery_key not in SURGERIES:
        return None
    
    surgery = SURGERIES[surgery_key]
    explanation_key = "simple_explanation" if knowledge_level == "beginner" else "expert_explanation"
    
    return {
        "name": surgery["name"],
        "description": surgery["description"],
        "explanation": surgery.get(explanation_key, surgery["simple_explanation"])
    }

def match_symptom_to_conditions(user_message: str) -> dict:
    """Match user symptoms to potential conditions and surgeries"""
    user_message_lower = user_message.lower()
    matches = []
    
    for symptom, info in SYMPTOM_MAPPING.items():
        if any(word in user_message_lower for word in symptom.split()):
            matches.append({
                "symptom": symptom,
                "conditions": info["conditions"],
                "surgeries": info["surgeries"],
                "questions": info["questions"],
                "urgency": info["urgency"]
            })
    
    # Also check surgery keywords
    for surgery_key, surgery_info in SURGERIES.items():
        for keyword in surgery_info["keywords"]:
            if keyword in user_message_lower:
                matches.append({
                    "matched_surgery": surgery_info["name"],
                    "surgery_key": surgery_key
                })
                break
    
    return matches if matches else None

def detect_knowledge_level(message: str) -> str:
    """Detect user's medical knowledge level from their message"""
    message_lower = message.lower()
    
    # Check for expert terminology
    expert_count = sum(1 for term in TERMINOLOGY_LEVELS["expert"] if term in message_lower)
    if expert_count >= 1:
        return "expert"
    
    # Check for intermediate terminology
    intermediate_count = sum(1 for term in TERMINOLOGY_LEVELS["intermediate"] if term in message_lower)
    if intermediate_count >= 2:
        return "intermediate"
    
    return "beginner"

def get_urgency_response(urgency_level: str) -> dict:
    """Get appropriate response based on urgency"""
    return URGENCY_LEVELS.get(urgency_level, URGENCY_LEVELS["routine"])
