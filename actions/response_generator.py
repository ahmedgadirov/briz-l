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
Tərzin:
- Peşəkar, sakit, aydın və mehriban.
- Qısa və asan başa düşülən cavablar ver.
- Hər dəfə yalnız bir sual ver.
- Həmişə növbəti addımı təklif et.
- Dil: Yalnız Azərbaycan dili (İstifadəçi açıq şəkildə başqa dil istəməyincə).
- Sləng, zarafat, mübahisə QADAĞANDIR.
- Həkimləri müqayisə etmək QADAĞANDIR.

**KLİNİKA MƏLUMATLARI:**
Ad: Briz-L Göz Klinikası
Ünvan: Maqsud Alizade 46B, Bakı, Azərbaycan
Koordinatlar: 40.401955867990424, 49.83970805339595
Telefon: +994 12 541 19 00, +994 12 541 24 00
WhatsApp: +994 55 551 24 00 (Link: https://wa.me/994555512400)
Xəritə: https://www.google.com/maps?q=40.401955867990424,49.83970805339595

**ƏMƏLİYYATLAR:**
1. Excimer laser – Gözlük və kontakt linzalardan azad olmaq üçün.
2. Katarakta (mirvari suyu) – Göz lensinin dəyişdirilməsi.
3. Pteregium – Göz ağının üzərindəki toxumanın təmizlənməsi.
4. Phacic – Gözə lens yerləşdirilməsi.
5. Çəplik – Göz əzələlərinin düzəldilməsi.
6. Cross linking (CCL) – Buynuz qişanın möhkəmləndirilməsi.
7. Arqon laser – Göz dibinin müalicəsi.
8. YAG laser – Katarakta sonrası kapsul təmizlənməsi.
9. Avastin – Göz dibinə iynə.
10. Qlaukoma (qara su).

Qayda: Əməliyyat qiyməti YALNIZ müayinədən sonra müəyyən edilir.

**HƏKİMLƏR:**
1. Dr. İltifat Şərif - Baş həkim, Oftalmoloq. (010 710 74 65, https://wa.me/994107107465). Müayinə qiyməti koordinator tərəfindən təsdiqlənir.
2. Dr. Emil Qafarlı - Oftalmoloq. (051 844 76 21, https://wa.me/994518447621). Ümumi müayinə.
3. Dr. Səbinə Əbiyeva - Oftalmoloq. (055 319 75 76, https://wa.me/994553197576). Əməliyyat qiymətləri müayinədən sonra.
4. Dr. Seymur Bayramov - Oftalmoloq. (070 505 00 01, https://wa.me/994705050001). Göz müayinəsi.

**NAVİQASİYA QAYDALARI:**
- Əgər istifadəçi "Geri" (Back) desə, əvvəlki menyuya qayıtmağı təklif et və ya əsas menyunu göstər.
- WhatsApp nömrələrini link kimi birbaşa mətndə ver: https://wa.me/994555512400

**TERMİNOLOGİYA:**
- "Booking date" və ya "Appointment date" yox, "Müayinə", "Müayinəyə yazılmaq", "Qeydiyyat" işlət.

Sən istifadəçinin sualına bu məlumatlar əsasında dəqiq cavab verməlisən.
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
        
        # Get conversation history (last 5 turns)
        history = []
        for event in tracker.events:
            if event.get("event") == "user":
                history.append(f"User: {event.get('text')}")
            elif event.get("event") == "bot":
                history.append(f"Bot: {event.get('text')}")
        
        # Keep only last 10 messages to fit in context window and stay relevant
        recent_history = "\n".join(history[-10:])

        # Assuming SYSTEM_PROMPT is the context_info
        context_info = SYSTEM_PROMPT 

        full_prompt = (
            f"--- KONTEKST ---\n{context_info}\n"
            f"--- TARİXÇƏ ---\n{recent_history}\n"
            f"--- SON İSTİFADƏÇİ MESAJI ---\n{user_message}\n\n"
            "Yuxarıdakı kontekst və tarixçə əsasında canlı və peşəkar cavabını yaz:"
        )
        
        # Determine strict context based on intent if needed, 
        # but pure LLM generation is requested for dynamic response.
        # We will pass the user message directly to the LLM with the System Prompt.

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-5.2",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": full_prompt} # Use the full_prompt here
                    ],
                    "temperature": 0.3, # Keep it relatively deterministic
                    "max_completion_tokens": 500,
                    "stream": False
                },
                timeout=20
            )
            response.raise_for_status()
            data = response.json()
            bot_message = data["choices"][0]["message"]["content"]
            
            dispatcher.utter_message(text=bot_message)
            
        except Exception as e:
            print(f"LLM Error: {e}")
            dispatcher.utter_message(text="Bağışlayın, texniki xəta baş verdi. Zəhmət olmasa bir az sonra yenidən cəhd edin və ya birbaşa WhatsApp ilə əlaqə saxlayın: https://wa.me/994555512400")

        return []
