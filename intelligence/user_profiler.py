"""
Briz-L User Profiler
Analyzes user messages to detect knowledge level and conversation intent
"""

from .knowledge_base import detect_knowledge_level, TERMINOLOGY_LEVELS

class UserProfiler:
    """Profiles users based on their messages and conversation history"""
    
    def __init__(self):
        self.user_profiles = {}
    
    def analyze_user(self, user_id: str, message: str, conversation_history: list) -> dict:
        """
        Analyze user and create/update profile
        
        Returns:
            dict: {
                'knowledge_level': str,  # beginner/intermediate/expert
                'intent': str,  # symptom_inquiry/surgery_info/booking/general
                'confidence_level': str,  # lost/uncertain/confident
                'conversation_stage': str  # greeting/questioning/deciding/ready_to_book
            }
        """
        
        # Detect knowledge level
        knowledge_level = detect_knowledge_level(message)
        
        # Detect intent
        intent = self._detect_intent(message)
        
        # Detect confidence level
        confidence = self._detect_confidence(message)
        
        # Detect conversation stage
        stage = self._detect_conversation_stage(message, conversation_history)
        
        profile = {
            'user_id': user_id,
            'knowledge_level': knowledge_level,
            'intent': intent,
            'confidence_level': confidence,
            'conversation_stage': stage,
            'needs_guidance': confidence in ['lost', 'uncertain']
        }
        
        # Store profile
        self.user_profiles[user_id] = profile
        
        return profile
    
    def _detect_intent(self, message: str) -> str:
        """Detect what the user is trying to accomplish"""
        message_lower = message.lower()
        
        # Symptom inquiry
        symptom_keywords = [
            'görmürəm', 'ağrıyır', 'dumanlı', 'qırmızı', 'göz ağrısı',
            'görmə problem', 'görmə azalması', 'göz əti', 'çəp',
            'problem var', 'ağrı', 'işıq çaxması'
        ]
        if any(keyword in message_lower for keyword in symptom_keywords):
            return 'symptom_inquiry'
        
        # Surgery information
        surgery_keywords = [
            'əməliyyat', 'lazer', 'katarakta', 'excimer', 'çəplik',
            'operasiya', 'cərrahiyyə', 'nə qədər çəkir', 'qiymət'
        ]
        if any(keyword in message_lower for keyword in surgery_keywords):
            return 'surgery_info'
        
        # Booking intent
        booking_keywords = [
            'müayinə', 'qeydiyyat', 'yazılmaq', 'randevu', 'gəlmək istəyirəm',
            'vaxt', 'həkim', 'görüş', 'appointment'
        ]
        if any(keyword in message_lower for keyword in booking_keywords):
            return 'booking'
        
        # Pricing inquiry
        price_keywords = ['qiymət', 'pul', 'nə qədər', 'ödəniş', 'məbləğ']
        if any(keyword in message_lower for keyword in price_keywords):
            return 'pricing'
        
        # General inquiry
        return 'general'
    
    def _detect_confidence(self, message: str) -> str:
        """Detect user's confidence level about their needs"""
        message_lower = message.lower()
        
        # Lost/confused indicators
        lost_indicators = [
            'bilmirəm', 'nə edim', 'başa düşmürəm', 'kömək',
            'nə etməli', 'qarışıq', 'anlamıram', 'çaşqınam'
        ]
        if any(indicator in message_lower for indicator in lost_indicators):
            return 'lost'
        
        # Uncertain indicators
        uncertain_indicators = [
            'ola bilər', 'düşünürəm', 'yəqin', 'görünür',
            'deyəsən', 'bəlkə', 'şübhə', 'əmin deyil'
        ]
        if any(indicator in message_lower for indicator in uncertain_indicators):
            return 'uncertain'
        
        # Confident indicators
        confident_indicators = [
            'istəyirəm', 'lazımdır', 'bilirəm', 'əminəm',
            'mütləq', 'vaxt', 'həkim seç', 'əməliyyat et'
        ]
        if any(indicator in message_lower for indicator in confident_indicators):
            return 'confident'
        
        # Default to uncertain
        return 'uncertain'
    
    def _detect_conversation_stage(self, message: str, history: list) -> str:
        """Detect what stage of conversation flow user is in"""
        message_lower = message.lower()
        
        # Greeting stage
        greeting_keywords = ['salam', 'hello', 'hi', 'privet', 'sabah', 'axşam']
        if any(keyword in message_lower for keyword in greeting_keywords):
            return 'greeting'
        
        # Questioning stage (asking about symptoms/options)
        if len(history) <= 3:
            return 'questioning'
        
        # Deciding stage (comparing options, asking details)
        deciding_keywords = [
            'fərq', 'hansı yaxşı', 'seçim', 'müqayisə',
            'daha yaxşı', 'tövsiyə', 'məsləhət'
        ]
        if any(keyword in message_lower for keyword in deciding_keywords):
            return 'deciding'
        
        # Ready to book (wants to schedule)
        ready_keywords = [
            'müayinə', 'yazıl', 'qeydiyyat', 'vaxt',
            'gəlmək', 'görüş', 'randevu'
        ]
        if any(keyword in message_lower for keyword in ready_keywords):
            return 'ready_to_book'
        
        # Extended conversation
        if len(history) > 8:
            return 'extended_conversation'
        
        return 'questioning'
    
    def get_profile(self, user_id: str) -> dict:
        """Get stored user profile"""
        return self.user_profiles.get(user_id, {})
    
    def should_ask_diagnostic_questions(self, profile: dict) -> bool:
        """Determine if bot should ask diagnostic questions"""
        return (
            profile.get('intent') == 'symptom_inquiry' and
            profile.get('conversation_stage') in ['questioning', 'greeting']
        )
    
    def should_provide_education(self, profile: dict) -> bool:
        """Determine if bot should provide educational content"""
        return (
            profile.get('knowledge_level') == 'beginner' and
            profile.get('confidence_level') in ['lost', 'uncertain']
        )
    
    def should_recommend_booking(self, profile: dict) -> bool:
        """Determine if bot should recommend scheduling appointment"""
        return (
            profile.get('conversation_stage') in ['deciding', 'ready_to_book'] or
            profile.get('intent') == 'booking'
        )


def generate_adaptive_prompt(profile: dict, symptom_analysis: dict = None) -> str:
    """
    Generate an adaptive system prompt based on user profile
    
    Args:
        profile: User profile from UserProfiler
        symptom_analysis: Optional symptom triage results
    
    Returns:
        str: Customized prompt instructions for LLM
    """
    prompt_parts = []
    
    # Knowledge level adaptation
    if profile.get('knowledge_level') == 'beginner':
        prompt_parts.append("""
**İSTİFADƏÇİ SEVİYYƏSİ: Başlanğıc**
- ÇOX SADƏ dillə danış
- Tibbi terminlərdən qaçın və ya izah edin
- Hər şeyi addım-addım izah et
- Nümunələr və təşbehlər istifadə et
        """)
    elif profile.get('knowledge_level') == 'expert':
        prompt_parts.append("""
**İSTİFADƏÇİ SEVİYYƏSİ: Mütəxəssis**
- Tibbi terminologiya istifadə edə bilərsən
- Texniki detallar ver
- Müqayisəli analizlər təqdim et
        """)
    else:
        prompt_parts.append("""
**İSTİFADƏÇİ SEVİYYƏSİ: Orta**
- Balanslaşdırılmış dil istifadə et
- Bəzi tibbi terminlər uyğundur
- Aydın və dəqiq cavablar ver
        """)
    
    # Intent-based guidance
    if profile.get('intent') == 'symptom_inquiry':
        prompt_parts.append("""
**İSTİFADƏÇİ NİYYƏTİ: Simptom soruşur**
- DİAQNOSTİK suallar ver (nə vaxt başladı? hər iki göz? ağrı var?)
- Mümkün səbəbləri qeyd et
- TƏCİLİ olub-olmadığını qiymətləndir
- Müvafiq həkim və ya əməliyyat tövsiyə et
        """)
    
    if profile.get('confidence_level') == 'lost':
        prompt_parts.append("""
**İSTİFADƏÇİ HALATI: İtirib, köməyə ehtiyacı var**
- ÇOX MEHRIBAN və dəstəkləyici ol
- Addım-addım bələdçilik et
- Seçimləri sadələşdir
- "Narahat olmayın, sizə kömək edəcəyəm" tonunu saxla
        """)
    
    # Add symptom analysis if available
    if symptom_analysis:
        urgency = symptom_analysis.get('urgency', 'routine')
        if urgency == 'emergency':
            prompt_parts.append("""
**⚠️ TƏCİLİ VƏZIYYƏT AŞKAR EDİLDİ**
- DƏRHAL klinikamıza gəlməli olduğunu vurğula
- Təcili əlaqə məlumatları ver
- Sakit amma qətiyyətli ol
            """)
        elif urgency == 'urgent':
            prompt_parts.append("""
**ÖNƏMLİ: Tezliklə müayinə lazımdır**
- Bu problemin tez həll edilməli olduğunu izah et
- 1-3 gün içində müayinə tövsiyə et
            """)
    
    return "\n".join(prompt_parts)
