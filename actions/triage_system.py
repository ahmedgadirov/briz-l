from typing import Dict, Text, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionTriagePatient(Action):
    def name(self) -> Text:
        return "action_triage_patient"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extract symptoms
        symptoms = tracker.get_slot("symptoms") or []
        # Fallback if symptoms is not list but single text from entity
        if isinstance(symptoms, str):
             symptoms = [symptoms]
             
        # Also check patient_concern slot which might hold the symptom text
        concern = tracker.get_slot("patient_concern")
        if concern:
             symptoms = str(symptoms) + " " + concern
        
        duration = tracker.get_slot("symptom_duration")
        severity = tracker.get_slot("symptom_severity") # Corrected slot name from plan to match domain
        
        # EMERGENCY: Immediate attention needed
        emergency_symptoms = [
            "sudden vision loss", "görə bilmirəm",
            "eye injury", "gözə zədə",
            "severe pain", "dözülməz ağrı",
            "flashes of light", "işıq çaxmaları",
            "curtain over vision", "pərdə"
        ]
        
        # URGENT: Within 24 hours
        urgent_symptoms = [
            "red eye", "qırmızı göz", # Relaxed matching "red eye + pain" to just "red eye" or check combination logic if needed
            "floaters", "qaranlıq nöqtələr",
            "double vision", "ikili görmə",
            "post-surgery issue", "əməliyyatdan sonra"
        ]
        
        # SOON: Within 1 week
        soon_symptoms = [
            "blurry vision", "dumanlıq", "zəif görmə",
            "persistent pain", "davam edən ağrı",
            "discharge", "axıntı"
        ]
        
        # Triage decision
        priority = "routine"
        message = ""
        symptoms_str = str(symptoms).lower()
        
        if any(s in symptoms_str for s in emergency_symptoms) or (severity == "severe"):
            priority = "emergency"
            message = """⚠️ BU TƏCİLİ VƏZİYYƏTDİR!

Sizin əlamətləriniz dərhal müayinə tələb edir.

DƏRHAL EDIN:
1. Klinikamıza zəng edin: +994 12 541 19 00
2. WhatsApp yazın: https://wa.me/994555512400
3. Yaxınlıqdakı göz təcili yardımına gedin

⏰ 24 saat ərzində mütləq müayinə olun!"""

        elif any(s in symptoms_str for s in urgent_symptoms) or (severity == "moderate"): 
            priority = "urgent"
            message = """⚡ Sizin vəziyyətiniz tez diqqət tələb edir.

Tövsiyə: 24-48 saat ərzində müayinə.

Bu gün yaxud sabah üçün qeydiyyat edə bilərəm.
Telefon nömrəniz neçədir?"""

        elif any(s in symptoms_str for s in soon_symptoms):
            priority = "soon"
            message = """📋 Sizin əlamətləriniz müayinə tələb edir.

Tövsiyə: 3-7 gün ərzində müayinə.

Bu həftə yaxud gələn həftə üçün uyğun vaxt seçə bilərik.
Hansı günlər sizə əlverişlidir?"""
        
        else:
            priority = "routine"
            message = """✅ Profilaktik müayinə və ya məsləhət üçün qeydiyyat edə bilərəm.

İstədiyiniz vaxtı seçə bilərsiniz.
Hansı tarixlər sizə uyğundur?"""
        
        dispatcher.utter_message(text=message)
        
        return [SlotSet("urgency_level", priority)] # Map triage_priority to urgency_level slot defined in domain
