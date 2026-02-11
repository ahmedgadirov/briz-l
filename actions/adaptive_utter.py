from typing import Dict, Text, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionAdaptiveUtter(Action):
    def name(self) -> Text:
        return "action_adaptive_utter"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        language = tracker.get_slot("language") or "az"
        response_name = tracker.get_slot("response_to_utter")
        
        if not response_name:
            return []

        # Get all variations of the response from domain
        # Note: In standard Rasa SDK, 'domain' dict might not contain full response text metadata if not explicitly passed or if using standard utter_ actions. 
        # However, for custom adaptive logic, we usually need to define responses in a way we can access, or use the dispatcher's ability to select if defined with metadata.
        # But Rasa's default dispatcher.utter_message doesn't automatically filter by metadata key unless using specific channels or custom output.
        # A common pattern for multi-lang in Rasa is using response selector or just conditional logic.
        # Here we try to fetch from domain if available, or assume a structure.
        
        # ACTUALLY, a simpler way for this proof-of-concept without complex domain parsing is:
        # Define responses with suffixes like utter_greet_az, utter_greet_en, etc.
        # OR rely on the fact that we can pass the response template name and Rasa 3.x might handle metadata if configured (but that's complex).
        
        # Let's use the suffix approach for reliability in this custom action, 
        # OR better: The plan implies checking `domain.get("responses", ...)`
        
        responses = domain.get("responses", {}).get(response_name, [])
        
        # Filter by language metadata if available
        lang_response = None
        for resp in responses:
            if resp.get("metadata", {}).get("language") == language:
                lang_response = resp
                break
        
        # Fallback to first response if no language match or metadata not found
        if not lang_response and responses:
            lang_response = responses[0]
        
        if lang_response:
            dispatcher.utter_message(text=lang_response.get("text"))
        
        return []
