from typing import Dict, List, Any, Optional
from .content_retriever import MedicalContentRetriever


class PersonalizationEngine:
    """
    Adapts medical content based on patient context.
    - Knowledge level assessment
    - Emotional state detection (fear → reassurance)
    - Urgency level adaptation
    - Previous question tracking
    """
    
    def __init__(self):
        self.retriever = MedicalContentRetriever()
        
        # Keywords for emotional state detection
        self.fear_keywords = {
            'az': ['qorxuram', 'narahatam', 'təhlükəli', 'ağrılı', 'kor olacam', 'itirəcəm'],
            'ru': ['боюсь', 'переживаю', 'опасно', 'больно', 'ослепну', 'потеряю'],
            'en': ['afraid', 'worried', 'scared', 'dangerous', 'painful', 'blind', 'lose']
        }
        
        # Medical jargon to simplify
        self.jargon_simplifications = {
            'az': {
                'fakoemulsifikasiya': 'ultrasəs ilə lens əridilməsi',
                'intraokulyar': 'göz içi',
                'retinopatiya': 'retina xəstəliyi',
                'qlaukoma': 'göz təzyiqi xəstəliyi',
                'buynuz qişa': 'gözün şəffaf ön qatı'
            }
        }
    
    def detect_knowledge_level(self, user_messages: List[str]) -> str:
        """
        Assess user's medical knowledge level.
        
        Returns:
            'lay' (general public), 'intermediate', or 'advanced'
        """
        
        # Simple heuristic: count medical terms used
        medical_terms = ['lens', 'retina', 'buynuz qişa', 'kornea', 'fakoemulsifikasiya', 
                        'intraokulyar', 'topoqrafiya', 'biometriya']
        
        term_count = 0
        for msg in user_messages:
            msg_lower = msg.lower()
            for term in medical_terms:
                if term in msg_lower:
                    term_count += 1
        
        if term_count >= 3:
            return 'advanced'
        elif term_count >= 1:
            return 'intermediate'
        else:
            return 'lay'
    
    def detect_emotional_state(self, message: str, language: str = 'az') -> str:
        """
        Detect emotional state from message.
        
        Returns:
            'anxious', 'neutral', or 'confident'
        """
        
        keywords = self.fear_keywords.get(language, [])
        message_lower = message.lower()
        
        for keyword in keywords:
            if keyword in message_lower:
                return 'anxious'
        
        return 'neutral'
    
    def assess_urgency(self, symptoms: List[str], language: str = 'az') -> str:
        """
        Assess urgency level based on symptoms mentioned.
        
        Returns:
            'emergency', 'urgent', 'routine'
        """
        
        emergency_keywords = {
            'az': ['ağrı', 'qırmızı', 'birdən', 'kəskin', 'işıq çaxması', 'pərdə'],
            'ru': ['боль', 'красный', 'внезапно', 'резко', 'вспышки', 'завеса'],
            'en': ['pain', 'red', 'sudden', 'sharp', 'flashes', 'curtain']
        }
        
        keywords = emergency_keywords.get(language, [])
        
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            for keyword in keywords:
                if keyword in symptom_lower:
                    return 'emergency'
        
        return 'routine'
    
    def personalize_content(self,
                           content: str,
                           knowledge_level: str = 'lay',
                           emotional_state: str = 'neutral',
                           urgency: str = 'routine',
                           language: str = 'az') -> str:
        """
        Personalize content based on patient context.
        
        Args:
            content: Original content text
            knowledge_level: 'lay', 'intermediate', or 'advanced'
            emotional_state: 'anxious', 'neutral', or 'confident'
            urgency: 'emergency', 'urgent', or 'routine'
            language: User's language
        
        Returns:
            Personalized content
        """
        
        personalized = content
        
        # 1. Simplify medical jargon for lay audience
        if knowledge_level == 'lay':
            simplifications = self.jargon_simplifications.get(language, {})
            for jargon, simple in simplifications.items():
                personalized = personalized.replace(jargon, f"{jargon} ({simple})")
        
        # 2. Add reassurance for anxious patients
        if emotional_state == 'anxious':
            reassurance = {
                'az': "\n\n💙 **Narahat olmayın!** Bu prosedur çox təhlükəsizdir və hər gün minlərlə pasiyentə uğurla edilir.",
                'ru': "\n\n💙 **Не волнуйтесь!** Эта процедура очень безопасна и успешно проводится тысячам пациентов каждый день.",
                'en': "\n\n💙 **Don't worry!** This procedure is very safe and is successfully performed on thousands of patients every day."
            }
            personalized += reassurance.get(language, '')
        
        # 3. Prioritize urgent information
        if urgency == 'emergency':
            warning = {
                'az': "\n\n🚨 **DİQQƏT:** Təcili simptomlar olduğu təqdirdə dərhal həkimə müraciət edin!",
                'ru': "\n\n🚨 **ВНИМАНИЕ:** При наличии срочных симптомов немедленно обратитесь к врачу!",
                'en': "\n\n🚨 **ATTENTION:** If you have urgent symptoms, seek medical attention immediately!"
            }
            personalized = warning.get(language, '') + "\n\n" + personalized
        
        return personalized
    
    def add_follow_up_suggestions(self,
                                  content_type: str,
                                  content_id: str,
                                  current_context: Dict[str, Any],
                                  language: str = 'az') -> List[str]:
        """
        Generate contextual follow-up suggestions.
        
        Returns:
            List of suggested follow-up questions/topics
        """
        
        suggestions = []
        
        # Get related content
        related = self.retriever.get_related_content(content_id)
        if related:
            suggestions.append({
                'az': "Əlaqəli xəstəliklər haqqında məlumat",
                'ru': "Информация о связанных заболеваниях",
                'en': "Information about related conditions"
            }.get(language, ''))
        
        # Suggest treatment info if discussing symptoms
        if current_context.get('discussed_symptoms'):
            suggestions.append({
                'az': "Müalicə variantları haqqında",
                'ru': "О вариантах лечения",
                'en': "About treatment options"
            }.get(language, ''))
        
        # Suggest cost info if discussing treatment
        if current_context.get('discussed_treatment'):
            suggestions.append({
                'az': "Qiymət məlumatı",
                'ru': "Информация о стоимости",
                'en': "Pricing information"
            }.get(language, ''))
        
        # Suggest appointment booking
        suggestions.append({
            'az': "Randevu təyin etmək",
            'ru': "Записаться на прием",
            'en': "Book an appointment"
        }.get(language, ''))
        
        return suggestions
    
    def track_conversation_context(self, 
                                   conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Track what has been discussed to avoid repetition.
        
        Returns:
            Context dictionary with discussed topics
        """
        
        context = {
            'discussed_symptoms': False,
            'discussed_treatment': False,
            'discussed_cost': False,
            'discussed_risks': False,
            'topics_covered': []
        }
        
        for turn in conversation_history:
            message = turn.get('message', '').lower()
            
            if any(word in message for word in ['simptom', 'əlamət', 'symptom']):
                context['discussed_symptoms'] = True
                context['topics_covered'].append('symptoms')
            
            if any(word in message for word in ['müalicə', 'əməliyyat', 'treatment', 'surgery']):
                context['discussed_treatment'] = True
                context['topics_covered'].append('treatment')
            
            if any(word in message for word in ['qiymət', 'nə qədər', 'price', 'cost']):
                context['discussed_cost'] = True
                context['topics_covered'].append('cost')
            
            if any(word in message for word in ['risk', 'komplikasiya', 'complication']):
                context['discussed_risks'] = True
                context['topics_covered'].append('risks')
        
        return context
