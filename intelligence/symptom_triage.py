"""
Briz-L Symptom Triage System
Intelligently analyzes symptoms and provides medical guidance
"""

from .knowledge_base import (
    match_symptom_to_conditions, 
    get_urgency_response,
    SURGERIES,
    SYMPTOM_MAPPING
)

class SymptomTriage:
    """Intelligent medical triage system for eye conditions"""
    
    def __init__(self):
        self.triage_history = {}
    
    def analyze_symptoms(self, user_id: str, message: str, knowledge_level: str = "beginner") -> dict:
        """
        Analyze user's symptom description and provide intelligent triage
        
        Args:
            user_id: User identifier
            message: User's symptom description
            knowledge_level: User's medical knowledge level (beginner/intermediate/expert)
        
        Returns:
            dict: {
                'has_symptoms': bool,
                'matched_conditions': list,
                'suggested_surgeries': list,
                'urgency': str,
                'diagnostic_questions': list,
                'recommendation': str,
                'explanation': str (adapted to knowledge level)
            }
        """
        
        # Match symptoms to conditions
        matches = match_symptom_to_conditions(message)
        
        if not matches:
            return {
                'has_symptoms': False,
                'matched_conditions': [],
                'suggested_surgeries': [],
                'urgency': 'routine',
                'diagnostic_questions': [],
                'recommendation': None,
                'explanation': None
            }
        
        # Aggregate results
        all_conditions = []
        all_surgeries = []
        diagnostic_questions = []
        highest_urgency = 'routine'
        
        urgency_priority = {'emergency': 3, 'urgent': 2, 'routine': 1}
        
        for match in matches:
            if 'conditions' in match:
                all_conditions.extend(match.get('conditions', []))
                all_surgeries.extend(match.get('surgeries', []))
                diagnostic_questions.extend(match.get('questions', []))
                
                # Track highest urgency
                match_urgency = match.get('urgency', 'routine')
                if urgency_priority.get(match_urgency, 0) > urgency_priority.get(highest_urgency, 0):
                    highest_urgency = match_urgency
        
        # Remove duplicates
        all_conditions = list(set(all_conditions))
        all_surgeries = list(set(all_surgeries))
        diagnostic_questions = list(set(diagnostic_questions))
        
        # Get urgency response
        urgency_info = get_urgency_response(highest_urgency)
        
        # Generate explanation based on knowledge level
        explanation = self._generate_explanation(
            all_conditions, 
            all_surgeries, 
            knowledge_level,
            highest_urgency
        )
        
        # Generate recommendation
        recommendation = self._generate_recommendation(
            all_surgeries,
            highest_urgency,
            knowledge_level
        )
        
        result = {
            'has_symptoms': True,
            'matched_conditions': all_conditions,
            'suggested_surgeries': all_surgeries,
            'urgency': highest_urgency,
            'urgency_info': urgency_info,
            'diagnostic_questions': diagnostic_questions[:3],  # Limit to 3 questions
            'recommendation': recommendation,
            'explanation': explanation
        }
        
        # Store in history
        if user_id not in self.triage_history:
            self.triage_history[user_id] = []
        self.triage_history[user_id].append(result)
        
        return result
    
    def _generate_explanation(self, conditions: list, surgeries: list, 
                             knowledge_level: str, urgency: str) -> str:
        """Generate explanation adapted to user's knowledge level"""
        
        if not conditions:
            return None
        
        if knowledge_level == "beginner":
            # Simple, clear explanation
            if urgency == "emergency":
                return f"Bu çox təcili vəziyyətdir! Gözünüzlə bağlı ciddi problem ola bilər. Dərhal həkimə müraciət edin!"
            
            condition_text = conditions[0] if len(conditions) == 1 else "bir neçə göz problemi"
            
            if surgeries:
                surgery_names = ", ".join(surgeries[:2])
                return f"Simptomlarınıza görə {condition_text} ola bilər. Müayinə lazımdır. Əgər lazım olarsa, {surgery_names} kimi müalicə variantları mövcuddur."
            else:
                return f"Simptomlarınıza görə {condition_text} ola bilər. Mütləq müayinə olunmalısınız."
        
        elif knowledge_level == "expert":
            # Technical explanation
            condition_list = ", ".join(conditions)
            surgery_list = ", ".join(surgeries) if surgeries else "konsevativ müalicə"
            
            return f"Diferensial diaqnoz: {condition_list}. Müayinə və müvafiq testlər lazımdır. Potensial müalicə: {surgery_list}."
        
        else:  # intermediate
            # Balanced explanation
            condition_text = " və ya ".join(conditions[:2])
            
            if surgeries:
                surgery_names = ", ".join(surgeries)
                return f"Bu simptomlar {condition_text} göstərə bilər. Dəqiq diaqnoz üçün müayinə lazımdır. Əməliyyat lazım olarsa: {surgery_names}."
            else:
                return f"Bu simptomlar {condition_text} əlaməti ola bilər. Müayinə və müalicə planı üçün həkimə müraciət edin."
    
    def _generate_recommendation(self, surgeries: list, urgency: str, 
                                 knowledge_level: str) -> str:
        """Generate actionable recommendation"""
        
        if urgency == "emergency":
            return "⚠️ DƏRHAL klinikamıza gəlin və ya təcili yardım çağırın!\n\nTelefon: +994 12 541 19 00\nWhatsApp: https://wa.me/994555512400"
        
        elif urgency == "urgent":
            if surgeries:
                surgery_text = surgeries[0]
                return f"Tezliklə müayinə olun. Bu problem {surgery_text} tələb edə bilər. 1-3 gün içində klinikamıza gəlməyiniz məsləhətdir."
            else:
                return "Bu problemi tez müayinə etdirmək vacibdir. 1-3 gün içində klinikamıza müraciət edin."
        
        else:  # routine
            if surgeries:
                return f"Müayinə üçün vaxt ayırın. Lazım olarsa, {surgeries[0]} kimi həllər mövcuddur. Müayinəyə yazılmaq üçün bizimlə əlaqə saxlayın."
            else:
                return "Müayinə olunmaq məsləhətdir. Bizə zəng edib vaxt təyin edə bilərsiniz."
    
    def get_diagnostic_questions(self, symptom_context: str) -> list:
        """Get relevant diagnostic questions based on symptom context"""
        
        context_lower = symptom_context.lower()
        questions = []
        
        # Vision-related questions
        if any(word in context_lower for word in ['görmə', 'dumanlı', 'bulanıq', 'görmürəm']):
            questions.extend([
                "Bu problem nə vaxtdan var? (bir neçə gün, ay, il?)",
                "Hər iki gözə aiddir, yoxsa bir gözə?",
                "Tədricən pisləşib, yoxsa qəfil baş verib?"
            ])
        
        # Pain-related questions
        if any(word in context_lower for word in ['ağrı', 'ağrıyır', 'sızıltı']):
            questions.extend([
                "Ağrı nə qədər güclüdür? (10 bal sistemində)",
                "Davamlı ağrıdır, yoxsa gəlib-gedəndir?",
                "İşıqdan narahatlıq var?"
            ])
        
        # Redness questions
        if any(word in context_lower for word in ['qırmızı', 'qızarmış']):
            questions.extend([
                "Axıntı var? (yaşarma, irin və s.)",
                "Qaşınma hiss edirsiniz?",
                "Hər iki göz qırmızıdır?"
            ])
        
        # Default questions if no specific context
        if not questions:
            questions = [
                "Gözlə bağlı əsas problemiz nədir?",
                "Nə vaxtdan bu şikayət var?",
                "Əvvəl göz əməliyyatı olmusunuz?"
            ]
        
        return questions[:3]  # Return max 3 questions
    
    def check_emergency_indicators(self, message: str) -> bool:
        """Check if message contains emergency indicators"""
        
        emergency_keywords = [
            'çox ağrı', 'dəhşətli ağrı', 'görmürəm', 'kor',
            'işıq çaxması', 'qara pərdə', 'qəfil', 'birdən',
            'qan', 'zədə', 'toxundu', 'vurdu'
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in emergency_keywords)
    
    def format_triage_response(self, triage_result: dict, knowledge_level: str) -> str:
        """Format triage results into a coherent response"""
        
        if not triage_result.get('has_symptoms'):
            return None
        
        response_parts = []
        
        # Add urgency alert if needed
        urgency = triage_result.get('urgency')
        if urgency == 'emergency':
            response_parts.append("⚠️ TƏCİLİ VƏZIYYƏT!")
        
        # Add explanation
        if triage_result.get('explanation'):
            response_parts.append(triage_result['explanation'])
        
        # Add diagnostic questions if available
        questions = triage_result.get('diagnostic_questions', [])
        if questions and urgency != 'emergency':
            response_parts.append("\nDaha yaxşı kömək etmək üçün bir neçə sual:")
            for i, q in enumerate(questions, 1):
                response_parts.append(f"{i}. {q}")
        
        # Add recommendation
        if triage_result.get('recommendation'):
            response_parts.append(f"\n{triage_result['recommendation']}")
        
        return "\n\n".join(response_parts)
