"""
Conversion Optimizer - Detects buying signals and optimizes for conversion
"""

from typing import Dict, List, Any
import re


class ConversionOptimizer:
    """Detects buying signals and determines conversion tactics"""
    
    # Buying signal patterns
    BUYING_SIGNALS = {
        'price_inquiry': {
            'keywords': ['qiymət', 'qiyməti', 'pul', 'nə qədər', 'ödəniş', 'məbləğ', 'dəyər'],
            'weight': 30,
            'urgency': 'high'
        },
        'availability_inquiry': {
            'keywords': ['nə vaxt', 'vaxt', 'gələ bilərəm', 'görüş', 'randevu', 
                        'qəbul', 'açıq', 'boş'],
            'weight': 35,
            'urgency': 'very_high'
        },
        'doctor_inquiry': {
            'keywords': ['hansı həkim', 'həkim', 'doktor', 'seç', 'təklif', 'yaxşı həkim'],
            'weight': 20,
            'urgency': 'medium'
        },
        'booking_intent': {
            'keywords': ['müayinə', 'müayinəyə', 'yazıl', 'qeydiyyat', 'booking', 
                        'appointment', 'təyin et', 'görüş'],
            'weight': 40,
            'urgency': 'very_high'
        },
        'decision_ready': {
            'keywords': ['istəyirəm', 'lazımdır', 'edək', 'razıyam', 'bəli', 
                        'qərar verdim', 'gəlmək'],
            'weight': 35,
            'urgency': 'very_high'
        },
        'surgery_research': {
            'keywords': ['əməliyyat', 'lazer', 'cərrahiyyə', 'operasiya'],
            'weight': 15,
            'urgency': 'medium'
        },
        'comparison_shopping': {
            'keywords': ['fərq', 'müqayisə', 'hansı yaxşı', 'daha yaxşı', 'seçim'],
            'weight': 20,
            'urgency': 'medium'
        }
    }
    
    # Symptoms that require medical attention (from intelligence system)
    SYMPTOM_KEYWORDS = {
        'urgent': ['ağrı', 'qırmızı', 'qəfil', 'tez', 'çox', 'güclü', 'dözülməz'],
        'moderate': ['dumanlı', 'bulanıq', 'görmürəm', 'pis görür', 'azalıb'],
        'mild': ['yorğunluq', 'quruyur', 'sulanır', 'qaşınır']
    }
    
    # Doctor names for detection
    DOCTOR_NAMES = ['iltifat', 'emil', 'səbinə', 'sabina', 'seymur', 'həkim', 'doktor']
    
    # Surgery names for detection (from knowledge base)
    SURGERY_NAMES = [
        'excimer', 'laser', 'katarakta', 'mirvari', 'pteregium', 'phacic',
        'çəplik', 'cesplik', 'cross linking', 'arqon', 'yag', 'avastin', 
        'qlaukoma', 'qara su'
    ]
    
    def __init__(self):
        pass
    
    def analyze_message(self, message: str, conversation_history: List = None) -> Dict[str, Any]:
        """
        Analyze user message for buying signals and conversion opportunities
        
        Args:
            message: User's message text
            conversation_history: Previous messages for context
        
        Returns:
            Dict with detected signals, items, and recommended actions
        """
        message_lower = message.lower()
        
        result = {
            'buying_signals': [],
            'signal_score': 0,
            'urgency_level': 'low',
            'detected_items': {
                'price_inquiry': False,
                'doctor_inquiry': False,
                'surgery_inquiry': False,
                'booking_intent': False,
                'symptoms': [],
                'surgeries': [],
                'doctors': [],
                'urgent_symptoms': False
            },
            'conversion_ready': False,
            'recommended_action': 'educate'
        }
        
        # Detect buying signals
        for signal_name, signal_data in self.BUYING_SIGNALS.items():
            if any(keyword in message_lower for keyword in signal_data['keywords']):
                result['buying_signals'].append(signal_name)
                result['signal_score'] += signal_data['weight']
                
                # Update urgency level
                if signal_data['urgency'] == 'very_high':
                    result['urgency_level'] = 'very_high'
                elif signal_data['urgency'] == 'high' and result['urgency_level'] != 'very_high':
                    result['urgency_level'] = 'high'
                elif signal_data['urgency'] == 'medium' and result['urgency_level'] == 'low':
                    result['urgency_level'] = 'medium'
        
        # Detect specific items
        detected_items = result['detected_items']
        
        # Price inquiry
        if 'price_inquiry' in result['buying_signals']:
            detected_items['price_inquiry'] = True
        
        # Doctor inquiry
        for doctor in self.DOCTOR_NAMES:
            if doctor in message_lower:
                detected_items['doctor_inquiry'] = True
                detected_items['doctors'].append(doctor)
        
        # Surgery inquiry
        for surgery in self.SURGERY_NAMES:
            if surgery in message_lower:
                detected_items['surgery_inquiry'] = True
                if surgery not in detected_items['surgeries']:
                    detected_items['surgeries'].append(surgery)
        
        # Booking intent
        if 'booking_intent' in result['buying_signals'] or 'availability_inquiry' in result['buying_signals']:
            detected_items['booking_intent'] = True
        
        # Symptoms detection
        for urgency, keywords in self.SYMPTOM_KEYWORDS.items():
            for keyword in keywords:
                if keyword in message_lower:
                    detected_items['symptoms'].append(keyword)
                    if urgency == 'urgent':
                        detected_items['urgent_symptoms'] = True
        
        # Determine if conversion ready (score >= 60 or explicit booking intent)
        result['conversion_ready'] = (
            result['signal_score'] >= 60 or 
            'booking_intent' in result['buying_signals'] or
            'decision_ready' in result['buying_signals']
        )
        
        # Recommend action based on analysis
        result['recommended_action'] = self._determine_action(result)
        
        return result
    
    def _determine_action(self, analysis: Dict[str, Any]) -> str:
        """Determine what action bot should take"""
        if analysis['conversion_ready']:
            return 'push_booking_hard'
        elif analysis['signal_score'] >= 40:
            return 'push_booking_soft'
        elif 'comparison_shopping' in analysis['buying_signals']:
            return 'provide_differentiators'
        elif 'surgery_research' in analysis['buying_signals']:
            return 'educate_and_guide'
        elif len(analysis['detected_items']['symptoms']) > 0:
            return 'triage_and_recommend'
        else:
            return 'educate'
    
    def generate_conversion_cta(self, analysis: Dict[str, Any], 
                               lead_score: int = 0) -> str:
        """
        Generate appropriate Call-To-Action based on analysis
        
        Args:
            analysis: Result from analyze_message
            lead_score: Current lead score
        
        Returns:
            String with appropriate CTA
        """
        action = analysis['recommended_action']
        
        if action == 'push_booking_hard':
            return self._get_hard_cta(analysis)
        elif action == 'push_booking_soft':
            return self._get_soft_cta(analysis)
        elif action == 'provide_differentiators':
            return self._get_differentiator_cta()
        elif action == 'triage_and_recommend':
            return self._get_triage_cta(analysis)
        else:
            return self._get_educational_cta()
    
    def _get_hard_cta(self, analysis: Dict[str, Any]) -> str:
        """Hard push for immediate booking"""
        ctas = [
            "\n\n📞 **MÜAYİNƏYƏ YAZILAQ?**\n\nHansı həkim ilə görüş təyin edək?\n🔹 Dr. İltifat Şərif (010 710 74 65)\n🔹 Dr. Səbinə Əbiyeva (055 319 75 76)",
            
            "\n\n📅 **HAZİR TƏYİN EDƏK?**\n\nSizə nömrə verək, birbaşa zəng edib vaxt tutasınız?\n📞 +994 12 541 19 00\n📱 WhatsApp: https://wa.me/994555512400",
            
            "\n\n⏰ **VAXİT İTİRMƏYƏK!**\n\nMüayinə üçün indiki ən yaxın vaxtı sizə ayıraq?\nHansı həkimi seçirsiniz?"
        ]
        
        # Return appropriate CTA based on what was detected
        if 'price_inquiry' in analysis['buying_signals']:
            return "\n\nDəqiq qiymət müayinədən sonra deyilir. Hər vəziyyət fərqlidir.\n\n📞 **Müayinəyə yazılaq?** Birbaşa zəng edin: +994 12 541 19 00"
        elif 'availability_inquiry' in analysis['buying_signals']:
            return ctas[0]
        else:
            return ctas[1]
    
    def _get_soft_cta(self, analysis: Dict[str, Any]) -> str:
        """Softer push with choice"""
        return "\n\n💡 **KÖMƏKLİK EDƏ BİLƏRƏM?**\n\nMüayinə üçün vaxt təyin etmək istərdiniz?\nVə ya başqa suallarınız var?"
    
    def _get_differentiator_cta(self) -> str:
        """Emphasize clinic strengths"""
        return "\n\n✅ **BRİZ-L ÜSTÜNLÜKLƏRI:**\n• 15+ il təcrübə\n• Müasir avadanlıq\n• Peşəkar komanda\n\n📞 Müayinə üçün bizimlə əlaqə saxlayın: +994 12 541 19 00"
    
    def _get_triage_cta(self, analysis: Dict[str, Any]) -> str:
        """CTA for medical triage"""
        if analysis['detected_items']['urgent_symptoms']:
            return "\n\n⚠️ **DİQQƏT!**\n\nBu problem ciddi ola bilər. Mümkün qədər tez müayinə vacibdir!\n\n📞 DƏRHAL ZƏNG EDİN: +994 12 541 19 00"
        else:
            return "\n\n🩺 **MÜAYİNƏ TÖVSİYƏ EDİRİK**\n\nDəqiq diaqnoz üçün həkim müayinəsi lazımdır.\n\n📞 Vaxt təyin edək: +994 12 541 19 00"
    
    def _get_educational_cta(self) -> str:
        """Gentle CTA for information seekers"""
        return "\n\n📚 Başqa sualınız var? Məmnuniyyətlə cavablandırırıq!"
    
    def should_inject_urgency(self, lead_score: int, message_count: int) -> bool:
        """
        Determine if urgency messaging should be added
        
        Args:
            lead_score: Current lead score
            message_count: Number of messages exchanged
        
        Returns:
            Boolean indicating if urgency should be added
        """
        # Add urgency if:
        # - Lead score is warm/hot (50+) and had 3+ messages
        # - Lead score is very hot (80+)
        return (lead_score >= 50 and message_count >= 3) or lead_score >= 80
    
    def get_urgency_message(self) -> str:
        """Get urgency message to inject"""
        messages = [
            "⏰ Qeyd: Həkimlərimizin qrafiki tez dolur. Erkən müayinə tövsiyə edirik.",
            "📅 Məlumat: Bu həftə randevular məhdud sayda qalıb.",
            "💡 Tövsiyə: Göz problemləri erkən müayinə ilə asanlıqla həll olunur."
        ]
        import random
        return messages[random.randint(0, len(messages) - 1)]
    
    def detect_objections(self, message: str) -> Dict[str, Any]:
        """Detect customer objections"""
        message_lower = message.lower()
        
        objections = {
            'price_concern': any(word in message_lower for word in ['bahá', 'qiymət çox', 'ucuz']),
            'time_concern': any(word in message_lower for word in ['vaxt yoxdur', 'məşğul', 'sonra']),
            'fear_concern': any(word in message_lower for word in ['qorxuram', 'təhlükə', 'risk', 'ağrı']),
            'doubt': any(word in message_lower for word in ['əmin deyil', 'bilmirəm', 'düşünürəm']),
            'delay': any(word in message_lower for word in ['sonra', 'gələn həftə', 'bir az'])
        }
        
        return {
            'has_objection': any(objections.values()),
            'objections': [k for k, v in objections.items() if v]
        }
    
    def get_objection_handler(self, objection_type: str) -> str:
        """Get response to handle objection"""
        handlers = {
            'price_concern': "Qiymət müayinədən sonra müəyyən edilir. Amma ən vacib sizin göz sağlamlığınızdır. Erkən müayinə hər zaman daha sərfəlidir.",
            'time_concern': "Müayinə cəmi 30-40 dəqiqə çəkir. Gözünüz üçün bu vaxt ayırmaq vacibdir.",
            'fear_concern': "Narahat olmayın! Müayinə tam ağrısızdır. Həkimlərimiz hər şeyi izah edəcək və rahatlaşdıracaq.",
            'doubt': "Başa düşürük. Məhz buna görə ilk əvvəl müayinə vacibdir - bütün suallarınıza cavab alarsiniz.",
            'delay': "Anladım, amma unutmayın ki göz problemləri tərk edilsə pisləşir. Vaxtı heç olmasa yazaq, sonra dəyişə bilərsiniz."
        }
        return handlers.get(objection_type, "")
