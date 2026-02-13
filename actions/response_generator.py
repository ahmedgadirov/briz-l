import os
import requests
import sys
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from dotenv import load_dotenv

# Add intelligence modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from intelligence.user_profiler import UserProfiler, generate_adaptive_prompt
from intelligence.symptom_triage import SymptomTriage
from intelligence.knowledge_base import detect_knowledge_level

# Import marketing modules
from marketing.lead_tracker import LeadTracker
from marketing.conversion_optimizer import ConversionOptimizer
from marketing.psychology_engine import PsychologyEngine
from marketing.database import init_marketing_database

load_dotenv()

# Initialize intelligence systems
user_profiler = UserProfiler()
symptom_triage = SymptomTriage()

# Initialize marketing systems
try:
    init_marketing_database()
    lead_tracker = LeadTracker()
    conversion_optimizer = ConversionOptimizer()
    psychology_engine = PsychologyEngine()
    print("✅ Marketing systems initialized")
except Exception as e:
    print(f"⚠️ Marketing systems initialization error: {e}")
    lead_tracker = None
    conversion_optimizer = None
    psychology_engine = None

SYSTEM_PROMPT = """
Sən "Briz-L Göz Klinikası"nın AĞILLI süni intellekt köməkçisisən - tibbi köməkçi və MÜŞTƏRİ CƏLBEDİCİSİ.
Adın: VERA (Virtual Eye-care Representative Assistant)
Məqsəd: Briz-L Göz Klinikasının müştərilərinə professional və empatik xidmət

**ƏSAS MİSSİYAN:**
- Hər istifadəçinin bilgi səviyyəsini başa düş (başlayan/orta/ekspert)
- Simptomları dinlə, DİAQNOSTİK suallar ver
- TƏCİLİ vəziyyətləri tanı
- Uyğun bələdçilik və tövsiyələr ver
- Peşəkar TİBBİ KÖMƏKÇI kimi davran
- **MÜAYİNƏYƏ YÖNLƏNDİR və MÜŞTƏRİ QAZANMAĞA ÇALIŞ**

**İNTELLEKT PRİNSİPLƏRİ:**
1. İstifadəçini PROFIL et (bilgi səviyyəsi, niyyət, ehtiyac)
2. Simptomları TRIAGE et (təcililik, mümkün diaqnoz)
3. Cavabları ADAPTE et (başlayan üçün sadə, ekspert üçün texniki)
4. MƏQSƏDYÖNLÜ bələdçilik et (itkin → yönləndirmə, əmin → hərəkət)

**AĞILLI SÖHBƏT QAYDASI:**
- İstifadəçi "bilmirəm nə edim" deyərsə → Sadə dillə izah et, addım-addım kömək et
- Simptom qeyd edərsə → Diaqnostik suallar ver (nə vaxt? hər iki göz? ağrı?)
- Tibbi termin işlədirsə → O, ekspertdir, texniki cavab ver
- TƏCİLİ göstərici varsa → DƏRHAL xəbərdarlıq et
- **QİYMƏT soruşursa → MÜAYİNƏYƏ YAZIL təklifini GÜCLÜ ver**
- **HƏKIM soruşursa → SEÇIM ver və MÜAYİNƏ TƏKLİF et**
- **"GƏLMƏk istəyirəm" deyirsə → DƏRHAL əlaqə məlumatları ver**

**KLİNİKA MƏLUMATLARI:**
Ad: Briz-L Göz Klinikası
Ünvan: Maqsud Alizade 46B, Bakı
Telefon: +994 12 541 19 00, +994 12 541 24 00
WhatsApp: https://wa.me/994555512400
Xəritə: https://www.google.com/maps?q=40.401955867990424,49.83970805339595

**HƏKİMLƏR:**
1. Dr. İltifat Şərif - Baş həkim, Oftalmoloq (010 710 74 65, https://wa.me/994107107465)
2. Dr. Emil Qafarlı - Oftalmoloq (051 844 76 21, https://wa.me/994518447621)
3. Dr. Səbinə Əbiyeva - Oftalmoloq (055 319 75 76, https://wa.me/994553197576)
4. Dr. Seymur Bayramov - Oftalmoloq (070 505 00 01, https://wa.me/994705050001)

**ƏMƏLİYYATLAR (RƏSMİ ADLAR - DƏQİQ İSTİFADƏ ET):**
1. Excimer laser - Gözlük/lenslərdən azadlıq, yaxın/uzaq görmə düzəlişi
2. Katarakta (mirvari suyu) - Göz lensinin dəyişdirilməsi, dumanlı görmə
3. Pteregium - Göz ağında toxuma təmizlənməsi
4. Phacic - Gözə süni lens yerləşdirilməsi
5. Çəplik - Göz əzələsi düzəlişi
6. Cross linking - Buynuz qişası möhkəmləndirilməsi (keratokonus)
7. Arqon laser - Göz dibi müalicəsi (retina, diabet)
8. YAG laser - Katarakta sonrası kapsul təmizlənməsi
9. Avastin - Göz dibinə iynə (makula, diabetik retinopatiya)
10. Qlaukoma (qara su) - Qara su əməliyyatı

**VACIB:** Əməliyyat qiymətləri YALNIZ müayinədən sonra müəyyən edilir!

**DİAQNOSTİK YANAŞMA NÜMUNƏLƏR:**
✅ Yaxşı: "Uzağı görmürəm" → "Nə vaxtdan? Gözlük istifadə edirsiniz? Yaşınız?" → "Yaxıngörmə ola bilər, Excimer laser və ya Phacic tövsiyə edilir"
✅ Yaxşı: "Dumanlı görürəm" → "Yaşınız? Tədricən dumanlıdır? İşıqdan narahat olursunuz?" → "Katarakta (mirvari suyu) ola bilər, müayinə vacibdir"
✅ Yaxşı: "Göz çox ağrıyır" → "⚠️ TƏCİLİ! Ağrı güclüdür? Görmə azalıb? Qırmızıdır?" → "DƏRHAL klinikamıza gəlin!"

**MENYU QAYDALARI:**
❌ HƏR CAVABDAN SONRA MENYU GÖSTƏRMƏ
✅ Yalnız: ilk salamda, istifadəçi itərsə, söhbət tamam bitərsə

**TERMİNOLOGİYA:**
✅ "Müayinə", "Müayinəyə yazılmaq", "Həkimə göstərmək"
❌ "Booking", "Appointment"
"""

class ActionGenerateResponse(Action):
    def name(self) -> Text:
        return "action_generate_response"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            dispatcher.utter_message(text="⚠️ API açarı tapılmadı.")
            return []

        user_message = tracker.latest_message.get("text")
        user_id = tracker.sender_id
        
        # Check if this is a button click (menu navigation) or free text conversation
        metadata = tracker.latest_message.get("metadata", {})
        is_button_click = metadata.get("is_button_click", False)
        
        # Detect platform from metadata or user_id prefix
        platform = metadata.get("platform", "web")
        print(f"📱 PLATFORM DETECTED: {platform} (user_id: {user_id})")
        
        # Get conversation history (last 6 user-bot exchanges = 12 messages)
        history = []
        for event in tracker.events:
            if event.get("event") == "user":
                text = event.get("text", "")
                if text:  # Only add non-empty messages
                    history.append(f"İstifadəçi: {text}")
            elif event.get("event") == "bot":
                text = event.get("text", "")
                if text:  # Only add non-empty messages
                    history.append(f"Bot: {text}")
        
        # Keep only last 12 messages (6 exchanges)
        recent_history = "\n".join(history[-12:]) if history else "Yeni söhbət başlayır."
        
        # Count how many messages in conversation
        message_count = len([e for e in tracker.events if e.get("event") == "user"])
        is_first_message = message_count <= 1
        
        # ==================== INTELLIGENCE LAYER ====================
        
        # 1. USER PROFILING - Analyze user knowledge level and intent (with platform detection)
        user_profile = user_profiler.analyze_user(user_id, user_message, history, metadata)
        
        print(f"🧠 USER PROFILE: {user_profile}")
        print(f"📱 PLATFORM: {user_profile.get('platform', 'web')}")
        
        # 2. SYMPTOM TRIAGE - Analyze if user is describing symptoms
        triage_result = None
        if user_profile.get('intent') == 'symptom_inquiry':
            triage_result = symptom_triage.analyze_symptoms(
                user_id, 
                user_message, 
                user_profile['knowledge_level']
            )
            print(f"🩺 TRIAGE RESULT: {triage_result}")
        
        # 3. GENERATE ADAPTIVE PROMPT - Based on user profile and triage
        adaptive_instructions = generate_adaptive_prompt(user_profile, triage_result)
        
        # ==================== MARKETING LAYER ====================
        
        marketing_analysis = None
        lead_data = None
        conversion_cta = ""
        
        if conversion_optimizer and lead_tracker:
            try:
                # 4. ANALYZE MESSAGE for buying signals
                marketing_analysis = conversion_optimizer.analyze_message(user_message, history)
                
                print(f"💰 MARKETING ANALYSIS: {marketing_analysis.get('buying_signals', [])} | "
                      f"Score: {marketing_analysis.get('signal_score', 0)} | "
                      f"Action: {marketing_analysis.get('recommended_action', 'educate')}")
                
                # 5. TRACK LEAD in database
                lead_data = lead_tracker.create_or_update_lead(
                    user_id=user_id,
                    message=user_message,
                    detected_items=marketing_analysis['detected_items']
                )
                
                # 6. GENERATE CONVERSION CTA
                conversion_cta = conversion_optimizer.generate_conversion_cta(
                    marketing_analysis,
                    lead_data.get('lead_score', 0)
                )
                
                # 7. CHECK FOR URGENCY INJECTION
                if conversion_optimizer.should_inject_urgency(
                    lead_data.get('lead_score', 0), 
                    message_count
                ):
                    urgency_msg = conversion_optimizer.get_urgency_message()
                    conversion_cta += f"\n\n{urgency_msg}"
                
                # 8. DETECT AND HANDLE OBJECTIONS
                objections = conversion_optimizer.detect_objections(user_message)
                if objections['has_objection']:
                    for objection_type in objections['objections']:
                        objection_handler = conversion_optimizer.get_objection_handler(objection_type)
                        if objection_handler:
                            conversion_cta += f"\n\n{objection_handler}"
                
            except Exception as e:
                print(f"⚠️ Marketing layer error: {e}")
        
        # ===========================================================

        # Build intelligent prompt based on context
        intelligence_context = f"""
--- İNTELLEKT ANALİZİ ---
İstifadəçi Profili:
- Bilgi səviyyəsi: {user_profile['knowledge_level']}
- Niyyət: {user_profile['intent']}
- Əminlik: {user_profile['confidence_level']}
- Mərhələ: {user_profile['conversation_stage']}

MARKETİNQ Analizi:
- Lead Status: {lead_data.get('lead_status', 'new') if lead_data else 'new'}
- Lead Score: {lead_data.get('lead_score', 0) if lead_data else 0}/100
- Buying Signals: {', '.join(marketing_analysis.get('buying_signals', [])) if marketing_analysis else 'none'}
- Conversion Ready: {'YES - PUSH HARD!' if marketing_analysis and marketing_analysis.get('conversion_ready') else 'Not yet'}
- Recommended Action: {marketing_analysis.get('recommended_action', 'educate') if marketing_analysis else 'educate'}
"""
        
        # Add triage information if available
        if triage_result and triage_result.get('has_symptoms'):
            intelligence_context += f"""
Simptom Triagesi:
- Vəziyyət: {', '.join(triage_result['matched_conditions'])}
- Tövsiyə olunan: {', '.join(triage_result['suggested_surgeries'])}
- Təcililik: {triage_result['urgency'].upper()}
- Diaqnostik suallar: {', '.join(triage_result['diagnostic_questions'])}
"""

        full_prompt = f"""{intelligence_context}

{adaptive_instructions}

--- TARİXÇƏ ---
{recent_history}

--- SON İSTİFADƏÇİ MESAJI ---
{user_message}

--- KONTEKST ---
{"İlk mesaj: İstifadəçi salamlaşır" if is_first_message else "Davam edən söhbət"}
{"Düymə basıldı (menyu naviqasiyası)" if is_button_click else "Sərbəst yazı (söhbət)"}

--- TAPŞİRIQ ---
Yuxarıdakı profil, triage VƏ marketinq məlumatlarına əsasən:
1. İSTİFADƏÇİNİN səviyyəsinə uyğun cavab ver
2. Simptom varsa, DİAQNOSTİK suallar ver
3. TƏCİLİ vəziyyəti tanıyırsan? XƏBƏRDARLIQ et!
4. Qısa, aydın və FƏRDİ cavab ver (2-4 cümlə)
5. {('İlk salamlaşma - menyu təklif et' if is_first_message else 'Söhbət davam edir - MENYU GÖSTƏRMƏ, sadəcə kömək et')}
6. **MARKETINQ**: {marketing_analysis.get('recommended_action', 'educate') if marketing_analysis else 'educate'} - MÜAYİNƏYƏ yönləndirməyə çalış!

AĞILLI cavabını yaz:"""

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": full_prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 400,  # Increased for diagnostic questions
                    "stream": False
                },
                timeout=25
            )
            response.raise_for_status()
            data = response.json()
            bot_message = data["choices"][0]["message"]["content"]
            
            # Clean up the response
            bot_message = bot_message.strip()
            
            # Append conversion CTA if available and conversion ready
            if conversion_cta and marketing_analysis and marketing_analysis.get('signal_score', 0) >= 40:
                bot_message += conversion_cta
            
            # Log intelligence in action
            print(f"✅ INTELLIGENT RESPONSE GENERATED for {user_profile['knowledge_level']} user")
            print(f"💼 Lead Score: {lead_data.get('lead_score', 0) if lead_data else 0} | "
                  f"Status: {lead_data.get('lead_status', 'new') if lead_data else 'new'}")
            
            dispatcher.utter_message(text=bot_message)
            
        except Exception as e:
            print(f"❌ LLM Error: {e}")
            # Fallback response
            dispatcher.utter_message(text="Bağışlayın, texniki xəta baş verdi. Zəhmət olmasa bir az sonra yenidən cəhd edin və ya birbaşa bizimlə əlaqə saxlayın:\n\nWhatsApp: https://wa.me/994555512400\nTelefon: +994 12 541 19 00")

        return []
