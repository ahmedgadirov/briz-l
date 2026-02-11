import os
import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
Sən "Briz-L Göz Klinikası"nın süni intellekt köməkçisisən.
Adın: Briz-L Eye Clinic Bot

**ƏSAS PRİNSİPLƏR:**
- Peşəkar, sakit, mehriban və CANLI söhbət et
- Təbii, əl ilə yazılmış kimi cavablar ver - hər dəfə fərqli ifadələr işlət
- QISA və asan başa düşülən cavablar ver (2-3 cümlə)
- Dil: Azərbaycan dili
- Sləng, zarafat, mübahisə, həkimləri müqayisə etmək QADAĞANDIR

**ÇOX ÖNƏMLİ - MENYU QAYDALARI:**
❌ HƏR CAVABDAN SONRA MENYU TƏKLİF ETMƏ!
✅ YALNIZ bu hallarda menyu təklif et:
  1. İstifadəçi açıq şəkildə "menyu", "seçim", "nə edə bilərəm" və s. istəyərsə
  2. Söhbət təbii şəkildə bitərsə və istifadəçi daha sual vermirsə
  3. İstifadəçi aşkar şəkildə itib görünərsə
  4. İlk salamlaşma zamanı (yalnız ilk dəfə)

**SÖHBƏT QAYDASI:**
- İstifadəçi sual verərsə → Sadəcə cavab ver, menyu göstərmə
- İstifadəçi izah istəyərsə → İzah ver, davam et
- Söhbət davam edərsə → Təbii cavab ver
- Yalnız söhbət bitəndə → "Başqa sualınız var?" və ya "Sizə necə kömək edə bilərəm?"

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

**ƏMƏLİYYATLAR (ÇOX İSTİFADƏ EDİLƏN):**
1. Excimer laser - Gözlük/lenslərdən azadlıq, yaxın/uzaq görmə düzəlişi
2. Katarakta - Göz lensinin dəyişdirilməsi, dumanlı görmə problemi
3. Pteregium - Göz ağında toxuma təmizlənməsi
4. Phacic - Gözə süni lens yerləşdirilməsi
5. Çəplik - Göz əzələsi düzəlişi
6. Cross linking - Buynuz qişası möhkəmləndirilməsi (keratokonus üçün)
7. Arqon laser - Göz dibi müalicəsi (retina, diabet və s.)
8. YAG laser - Katarakta sonrası kapsul təmizlənməsi
9. Avastin - Göz dibinə iynə (makula, diabetik retinopatiya)
10. Qlaukoma - Qara su əməliyyatı

**VACIB:** Əməliyyat qiymətləri YALNIZ müayinədən sonra müəyyən edilir!

**GÖZ PROBLEMLƏRİ VƏ HƏLLƏR:**
- "Uzağı görmürəm" → Yəqin ki yaxıngörmə, Excimer laser və ya gözlük
- "Yaxını görmürəm" → Uzaqgörmə (presbiopiya), müayinə lazımdır
- "Dumanlı görürəm" → Ola bilər katarakta, mütləq müayinə
- "Çəplik var" → Çəplik əməliyyatı
- "Gözüm qırmızıdır" → Müayinə lazımdır
- "Göz ağında ləkə" → Ola bilər pteregium

**TERMİNOLOGİYA:**
✅ "Müayinə", "Müayinəyə yazılmaq", "Həkimə göstərmək"
❌ "Booking", "Appointment"

**CAVAB TƏRZİ NÜMUNƏLƏR:**
Pis ❌: "Sizə bu əməliyyat barədə məlumat verdim. İndi menyu göstərim?"
Yaxşı ✅: "Bu əməliyyat göz dibinin müalicəsi üçündür. Başqa sualınız var?"

Pis ❌: "Həkimlərimiz haqqında məlumat aldınız. Nə etmək istəyirsiniz?"
Yaxşı ✅: "Dr. İltifat Şərif klinikaımızın baş həkimidir. Hansı problem üçün müayinə istəyirsiniz?"
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
        
        # Check if this is a button click (menu navigation) or free text conversation
        metadata = tracker.latest_message.get("metadata", {})
        is_button_click = metadata.get("is_button_click", False)
        
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

        # Build intelligent prompt based on context
        full_prompt = f"""--- TARİXÇƏ ---
{recent_history}

--- SON İSTİFADƏÇİ MESAJI ---
{user_message}

--- KONTEKST ---
{"İlk mesaj: İstifadəçi salamlaşır" if is_first_message else "Davam edən söhbət"}
{"Düymə basıldı (menyu naviqasiyası)" if is_button_click else "Sərbəst yazı (söhbət)"}

--- TAPŞİRIQ ---
Yuxarıdakı məlumatlar əsasında:
1. Təbii, canlı və peşəkar cavab ver
2. Qısa və aydın yaz (2-3 cümlə)
3. {'İlk salamlaşma olduğu üçün YALNIZ bu dəfə əsas menyunu təklif et' if is_first_message else 'MENYU TƏKLİF ETMƏ - sadəcə cavab ver və söhbətə davam et'}
4. Hər dəfə FƏRQLI ifadələr işlət - eyni cümlələri təkrar etmə
5. İstifadəçinin konkret sualına cavab ver

Cavabını yaz:"""

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4o-mini",  # Using more reliable model
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": full_prompt}
                    ],
                    "temperature": 0.7,  # Higher for more varied responses
                    "max_tokens": 300,
                    "stream": False
                },
                timeout=20
            )
            response.raise_for_status()
            data = response.json()
            bot_message = data["choices"][0]["message"]["content"]
            
            # Clean up the response
            bot_message = bot_message.strip()
            
            dispatcher.utter_message(text=bot_message)
            
        except Exception as e:
            print(f"LLM Error: {e}")
            # Fallback response
            dispatcher.utter_message(text="Bağışlayın, texniki xəta baş verdi. Zəhmət olmasa bir az sonra yenidən cəhd edin və ya birbaşa bizimlə əlaqə saxlayın:\n\nWhatsApp: https://wa.me/994555512400\nTelefon: +994 12 541 19 00")

        return []
