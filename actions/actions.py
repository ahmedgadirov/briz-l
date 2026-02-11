from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction

class ActionPushMenu(Action):
    def name(self) -> Text:
        return "action_push_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_menu = tracker.get_slot("current_menu")
        menu_stack = tracker.get_slot("menu_stack") or []
        # Ensure it's a list copy
        menu_stack = list(menu_stack)
        
        last_intent = tracker.latest_message.get("intent", {}).get("name")
        target_menu = "main" # default
        
        if last_intent and last_intent.startswith("menu_"):
            target_menu = last_intent.replace("menu_", "")
        
        # Don't push if we are just refreshing the same menu
        if current_menu and current_menu != target_menu:
             menu_stack.append(current_menu)

        return [SlotSet("menu_stack", menu_stack), SlotSet("current_menu", target_menu)]

class ActionBack(Action):
    def name(self) -> Text:
        return "action_back"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        menu_stack = tracker.get_slot("menu_stack") or []
        # Ensure it's a list copy
        menu_stack = list(menu_stack)
        
        if not menu_stack:
            # Stack empty, go to main
            dispatcher.utter_message(response="utter_menu_main")
            return [
                SlotSet("menu_stack", []),
                SlotSet("current_menu", "main")
            ]
            
        # Pop the last menu
        previous_menu = menu_stack.pop()
        
        dispatcher.utter_message(response=f"utter_menu_{previous_menu}")
        
        return [
            SlotSet("menu_stack", menu_stack), 
            SlotSet("current_menu", previous_menu)
        ]

class ActionResetToMain(Action):
    def name(self) -> Text:
        return "action_reset_to_main"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        dispatcher.utter_message(response="utter_menu_main")
        return [
            SlotSet("menu_stack", []),
            SlotSet("current_menu", "main")
        ]

class ActionGuardrailLanguage(Action):
    def name(self) -> Text:
        return "action_guardrail_language"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        # Check if user asked for English
        text = tracker.latest_message.get("text", "").lower()
        if "english" in text:
             dispatcher.utter_message(text="Sorry, I only speak Azerbaijani. (Bağışlayın, mən yalnız Azərbaycan dilində danışıram.)")
             # Optionally set a slot or force Azerbaijani logic here
        
        return []

class ActionFallbackWithCount(Action):
    def name(self) -> Text:
        return "action_fallback_with_count"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        fallback_count = tracker.get_slot("fallback_count") or 0.0
        fallback_count += 1
        
        if fallback_count >= 2:
            dispatcher.utter_message(response="utter_hitl")
            return [SlotSet("fallback_count", 0.0)]
        else:
            dispatcher.utter_message(response="utter_fallback")
            return [SlotSet("fallback_count", fallback_count)]

class ActionAnalyzeSymptoms(Action):
    def name(self) -> Text:
        return "action_analyze_symptoms"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        severity = (tracker.get_slot("symptom_severity") or "").lower()
        duration = (tracker.get_slot("symptom_duration") or "").lower()
        
        urgent_keywords = ["dözülməz", "çox pis", "bərk", "qan", "kor", "görmürəm", "təcili", "ciddi"]
        
        urgency_level = "routine"
        if any(keyword in severity for keyword in urgent_keywords):
            urgency_level = "urgent"
            dispatcher.utter_message(text="⚠️ Bu simptomlar ciddi ola bilər. Zəhmət olmasa təcili müayinəyə yaxınlaşın.")
        elif "gün" in duration and "ay" not in duration:
             # Recent issue
             urgency_level = "soon"
        
        return [SlotSet("urgency_level", urgency_level)]

class ActionRecommendDoctor(Action):
    def name(self) -> Text:
        return "action_recommend_doctor"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        concern = (tracker.get_slot("patient_concern") or "").lower()
        
        doctor_name = "Dr. Emil Qafarlı" # Default
        reason = "ümumi göz müayinəsi üzrə mütəxəssisimizdir"
        
        if any(x in concern for x in ["katarakta", "mirvari", "lens", "yaşlı"]):
            doctor_name = "Dr. İltifat Şərif"
            reason = "baş həkimimiz və katarakta cərrahiyyəsi üzrə ekspertdir"
            
        elif any(x in concern for x in ["lazer", "eynak", "eynək", "glasses", "excimer", "astigmat"]):
            doctor_name = "Dr. Emil Qafarlı"
            reason = "lazer və refraktiv cərrahiyyə üzrə ixtisaslaşıb"
            
        elif any(x in concern for x in ["uşaq", "usaq", "çəplik", "ceplik", "strabismus"]):
            doctor_name = "Dr. Səbinə Əbiyeva"
            reason = "uşaq oftalmologiyası və çəplik üzrə mütəxəssisdir"
            
        elif any(x in concern for x in ["qızartı", "qizarti", "infeksiya", "virus", "buynuz"]):
            doctor_name = "Dr. Seymur Bayramov"
            reason = "göz xəstəliklərinin müalicəsində təcrübəlidir"

        dispatcher.utter_message(text=f"Sizin şikayətinizə əsasən {doctor_name}-i məsləhət görürəm. O, {reason}.")
        
        return [SlotSet("preferred_doctor", doctor_name)]
