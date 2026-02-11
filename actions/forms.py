from typing import Dict, Text, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict

class ValidateSymptomQualifierForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_symptom_qualifier_form"
    
    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Text]:
        return ["symptom_type", "symptom_duration", "symptom_severity", "affects_daily_life"]
    
    async def extract_symptom_type(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> Dict[Text, Any]:
        # Extract from entities or text
        # If symptom entity is present, use it. Else use full text if it's the start of form
        symptom = next(tracker.get_latest_entity_values("patient_concern"), None)
        if symptom:
             return {"symptom_type": symptom}
        
        return {"symptom_type": tracker.latest_message.get("text")}
    
    def validate_symptom_severity(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        # Natural language to severity mapping
        text = str(slot_value).lower()
        
        if any(word in text for word in ["dözülməz", "çox pis", "ölürəm", "güclü"]):
            return {"symptom_severity": "severe"}
        elif any(word in text for word in ["orta", "bəzən", "arada"]):
            return {"symptom_severity": "moderate"}
        elif any(word in text for word in ["yüngül", "az", "xeyli", "bir az"]):
            return {"symptom_severity": "mild"}
        
        # Ask for clarification
        dispatcher.utter_message(text="Ağrı 1-dən 10-a qədər neçədir? (1=az, 10=dözülməz)")
        return {"symptom_severity": None}
