"""
Medical Education Action for Rasa.
Provides intelligent, personalized medical information to patients.
"""

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import sys
from pathlib import Path

# Add medical_education to path
medical_education_path = Path(__file__).parent.parent
sys.path.insert(0, str(medical_education_path))

from core.content_retriever import MedicalContentRetriever
from core.progressive_disclosure import ProgressiveDisclosure
from core.personalization_engine import PersonalizationEngine
from core.semantic_search import SemanticSearch


class ActionEducate(Action):
    """
    Main education action.
    Handles queries about medical conditions and procedures.
    """
    
    def __init__(self):
        super().__init__()
        self.retriever = MedicalContentRetriever()
        self.progressive = ProgressiveDisclosure()
        self.personalizer = PersonalizationEngine()
        self.search = SemanticSearch()
    
    def name(self) -> Text:
        return "action_educate"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get language from slot (set by language detection)
        language = tracker.get_slot("detected_language") or "az"
        
        # Get user's message
        user_message = tracker.latest_message.get('text', '')
        
        # Try to extract medical condition/procedure from entities
        entities = tracker.latest_message.get('entities', [])
        condition = None
        procedure = None
        
        for entity in entities:
            if entity.get('entity') == 'medical_condition':
                condition = entity.get('value')
            elif entity.get('entity') == 'medical_procedure':
                procedure = entity.get('value')
        
        # If no entity, use semantic search
        if not condition and not procedure:
            search_results = self.search.search(user_message, language, limit=1)
            if search_results:
                result = search_results[0]
                if result['type'] == 'condition':
                    condition = result['id']
                else:
                    procedure = result['id']
        
        # Determine content type and ID
        if condition:
            content_type = 'condition'
            content_id = condition
        elif procedure:
            content_type = 'procedure'
            content_id = procedure
        else:
            # No match found
            dispatcher.utter_message(text=self._get_no_match_message(language))
            return []
        
        # Get current education depth
        current_depth = tracker.get_slot("education_depth") or 0
        
        # Check if user wants more details
        if self._is_more_request(user_message, language):
            current_depth += 1
        else:
            # New topic, reset depth
            current_depth = 0
        
        # Get layer content
        layer_data = self.progressive.get_next_layer(
            content_type,
            content_id,
            current_depth,
            language
        )
        
        # Format content
        content = self.progressive.format_for_chat(layer_data, language)
        
        # Personalize content
        # Get conversation history for context
        events = tracker.events
        user_messages = [e.get('text', '') for e in events if e.get('event') == 'user']
        
        # Detect personalization parameters
        knowledge_level = self.personalizer.detect_knowledge_level(user_messages[-5:])
        emotional_state = self.personalizer.detect_emotional_state(user_message, language)
        
        # Personalize
        personalized_content = self.personalizer.personalize_content(
            content,
            knowledge_level=knowledge_level,
            emotional_state=emotional_state,
            urgency='routine',  # Could extract from triage system
            language=language
        )
        
        # Send message
        dispatcher.utter_message(text=personalized_content)
        
        # Return updated slots
        return [
            SlotSet("education_topic", content_id),
            SlotSet("education_type", content_type),
            SlotSet("education_depth", current_depth),
            SlotSet("education_layer", layer_data['layer_name'])
        ]
    
    def _is_more_request(self, message: str, language: str) -> bool:
        """Check if user is requesting more information."""
        
        more_keywords = {
            'az': ['daha', 'ətraflı', 'bəli', 'hə', 'istəyirəm', 'davam'],
            'ru': ['больше', 'подробнее', 'да', 'хочу', 'продолжить'],
            'en': ['more', 'details', 'yes', 'continue', 'next']
        }
        
        keywords = more_keywords.get(language, [])
        message_lower = message.lower()
        
        return any(keyword in message_lower for keyword in keywords)
    
    def _get_no_match_message(self, language: str) -> str:
        """Return message when no content match found."""
        
        messages = {
            'az': "Üzr istəyirəm, bu mövzu haqqında məlumat tapa bilmədim. Başqa sualınız var?",
            'ru': "Извините, я не нашел информацию по этой теме. Есть другие вопросы?",
            'en': "Sorry, I couldn't find information on this topic. Any other questions?"
        }
        
        return messages.get(language, messages['az'])


class ActionSearchEducation(Action):
    """
    Search action for finding medical content.
    """
    
    def __init__(self):
        super().__init__()
        self.search = SemanticSearch()
    
    def name(self) -> Text:
        return "action_search_education"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        language = tracker.get_slot("detected_language") or "az"
        user_message = tracker.latest_message.get('text', '')
        
        # Search
        results = self.search.search(user_message, language, limit=5)
        
        if not results:
            dispatcher.utter_message(text=self._get_no_results_message(language))
            return []
        
        # Format results
        response = self._format_results(results, language)
        dispatcher.utter_message(text=response)
        
        return []
    
    def _format_results(self, results: List[Dict], language: str) -> str:
        """Format search results for display."""
        
        header = {
            'az': "Tapılan nəticələr:\n\n",
            'ru': "Найденные результаты:\n\n",
            'en': "Search results:\n\n"
        }
        
        message = header.get(language, header['az'])
        
        for i, result in enumerate(results, 1):
            content_type_label = {
                'az': '(Xəstəlik)' if result['type'] == 'condition' else '(Prosedur)',
                'ru': '(Заболевание)' if result['type'] == 'condition' else '(Процедура)',
                'en': '(Condition)' if result['type'] == 'condition' else '(Procedure)'
            }
            
            label = content_type_label.get(language, content_type_label['az'])
            message += f"{i}. {result['name']} {label}\n"
        
        message += "\n" + {
            'az': "Hansı haqqında məlumat istəyirsiniz?",
            'ru': "О каком хотите узнать?",
            'en': "Which one would you like to know about?"
        }.get(language, "Hansı haqqında məlumat istəyirsiniz?")
        
        return message
    
    def _get_no_results_message(self, language: str) -> str:
        """Message when no search results."""
        
        messages = {
            'az': "Heç nə tapa bilmədim. Başqa cür sual edə bilərsiniz?",
            'ru': "Ничего не найдено. Можете задать вопрос иначе?",
            'en': "No results found. Can you rephrase your question?"
        }
        
        return messages.get(language, messages['az'])


class ActionListConditions(Action):
    """List all available conditions."""
    
    def __init__(self):
        super().__init__()
        self.retriever = MedicalContentRetriever()
    
    def name(self) -> Text:
        return "action_list_conditions"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        language = tracker.get_slot("detected_language") or "az"
        
        conditions = self.retriever.list_all_conditions(language)
        
        header = {
            'az': "Haqqında məlumat verə biləcəyim göz xəstəlikləri:\n\n",
            'ru': "Глазные заболевания, о которых я могу рассказать:\n\n",
            'en': "Eye conditions I can tell you about:\n\n"
        }
        
        message = header.get(language, header['az'])
        
        for condition in conditions:
            message += f"• {condition['name']}\n"
        
        dispatcher.utter_message(text=message)
        
        return []
