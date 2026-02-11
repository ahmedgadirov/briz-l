"""
Psychology Engine - Persuasion tactics and psychological techniques
"""

from typing import Dict, List, Any
import random


class PsychologyEngine:
    """Applies psychological persuasion techniques to marketing messages"""
    
    def __init__(self):
        pass
    
    def apply_choice_architecture(self, options: List[str]) -> str:
        """
        Choice architecture - Present options instead of yes/no
        
        Args:
            options: List of choices to present
        
        Returns:
            Formatted choice message
        """
        if len(options) == 2:
            return f"Hansını seçirsiniz:\n🔹 {options[0]}\n🔹 {options[1]}"
        elif len(options) >= 3:
            formatted = "\n".join([f"🔹 {opt}" for opt in options])
            return f"Seçim edin:\n{formatted}"
        else:
            return options[0] if options else ""
    
    def apply_loss_aversion(self, context: str = 'general') -> str:
        """
        Loss aversion - Emphasize what they'll lose by not acting
        
        Args:
            context: Context for loss aversion message
        
        Returns:
            Loss aversion message
        """
        messages = {
            'general': [
                "Gözləmək göz sağlamlığınıza zərər verə bilər.",
                "Hər gün gecikmə problemi daha da çətinləşdirir.",
                "Erkən müdaxilə həmişə daha effektivdir və asandır."
            ],
            'symptom': [
                "Bu simptomları nəzərə almamaq vəziyyəti pisləşdirə bilər.",
                "Göz problemləri tərk edilərsə qaytarılmaz zərər yarada bilər.",
                "Tez müayinə problemin böyüməsinin qarşısını alır."
            ],
            'surgery': [
                "Əməliyyatı gecikdirmək nəticələri pisləşdirə bilər.",
                "Optimal nəticə üçün düzgün vaxt seçmək vacibdir.",
                "Erkən müdaxilə sağalmanı asanlaşdırır."
            ]
        }
        
        context_messages = messages.get(context, messages['general'])
        return random.choice(context_messages)
    
    def apply_social_proof(self, context: str = 'general') -> str:
        """
        Social proof - Show that others trust and use the service
        
        Args:
            context: Context for social proof
        
        Returns:
            Social proof message
        """
        proofs = {
            'general': [
                "15+ il təcrübə ilə minlərlə xəstəyə xidmət göstərmişik.",
                "Xəstələrimiz bizimlə göz sağlamlığını etibar edirlər.",
                "Professional komandamız hər gün insanlara görməyə kömək edir."
            ],
            'surgery': [
                "Bu əməliyyat bizim ən çox apardığımız prosedurlardan biridir.",
                "Həkimlərimiz bu sahədə geniş təcrübəyə malikdir.",
                "Yüksək texnologiyalı avadanlıqla əməliyyatlar aparılır."
            ],
            'doctor': [
                "Həkimlərimiz Avropa standartlarında təlim keçiblər.",
                "Komandamız 15+ il birgə işləyir və yüksək təcrübəyə malikdir.",
                "Peşəkar oftalmoloqlarımız sizə ən yaxşı xidməti göstərəcək."
            ]
        }
        
        context_proofs = proofs.get(context, proofs['general'])
        return random.choice(context_proofs)
    
    def apply_scarcity(self, scarcity_type: str = 'time') -> str:
        """
        Scarcity - Create sense of limited availability
        
        Args:
            scarcity_type: Type of scarcity (time, availability, seasonal)
        
        Returns:
            Scarcity message
        """
        messages = {
            'time': [
                "⏰ Həkimlərimizin qrafiki tez dolur.",
                "⏰ Tezliklə yazılmaq daha çox seçim imkanı verir.",
                "⏰ Bu həftə hələ açıq vaxtlar var."
            ],
            'availability': [
                "📅 Randevular məhdud sayda qalıb.",
                "📅 Tez qərar vermək vaxt seçimi üçün yaxşıdır.",
                "📅 Ən yaxşı vaxtlar tez dolur."
            ],
            'seasonal': [
                "🌤️ Yay aylarında sağalma prosesi daha rahatdır.",
                "🌤️ İndi ən uyğun mövsümdür.",
                "🌤️ Bu dövr əməliyyat üçün idealdır."
            ]
        }
        
        scarcity_messages = messages.get(scarcity_type, messages['time'])
        return random.choice(scarcity_messages)
    
    def apply_authority(self, context: str = 'general') -> str:
        """
        Authority - Emphasize expertise and credentials
        
        Args:
            context: Context for authority message
        
        Returns:
            Authority message
        """
        authorities = {
            'general': [
                "✅ 15+ il peşəkar təcrübə",
                "✅ Avropa standartlarında xidmət",
                "✅ Sertifikatlı oftalmoloq komanda"
            ],
            'doctor': [
                "✅ Dr. İltifat - 5000+ uğurlu əməliyyat təcrübəsi",
                "✅ Beynəlxalq sertifikatlı həkimlər",
                "✅ Mütəmadi olaraq xaricdə təlim keçən komanda"
            ],
            'technology': [
                "✅ Ən müasir göz əməliyyat avadanlıqları",
                "✅ Avropa texnologiyaları ilə təchiz olunmuş",
                "✅ Yüksək keyfiyyətli tibbi materiallar"
            ]
        }
        
        context_authorities = authorities.get(context, authorities['general'])
        return random.choice(context_authorities)
    
    def apply_reciprocity(self, value_given: str) -> str:
        """
        Reciprocity - Give value first, then ask
        
        Args:
            value_given: Description of value provided
        
        Returns:
            Reciprocity message
        """
        return f"Sizə {value_given} təqdim etdik. İndi sizə necə kömək edə bilərik?"
    
    def apply_commitment_consistency(self, previous_action: str) -> str:
        """
        Commitment & Consistency - Reference previous commitment
        
        Args:
            previous_action: Previous action user took
        
        Returns:
            Commitment message
        """
        messages = [
            f"Daha əvvəl {previous_action} maraq göstərmisiniz. Davam edək?",
            f"{previous_action} barədə daha ətraflı danışaq?",
            f"Gördüyüm kimi {previous_action} sizin üçün vacibdir. Addım ataq?"
        ]
        return random.choice(messages)
    
    def create_value_stack(self, items: List[str]) -> str:
        """
        Value stacking - Stack multiple benefits together
        
        Args:
            items: List of value items
        
        Returns:
            Formatted value stack
        """
        if not items:
            return ""
        
        header = "✅ **SİZİN ÜÇÜN:**\n"
        stacked = "\n".join([f"• {item}" for item in items])
        return f"{header}{stacked}"
    
    def apply_anchoring(self, high_value: str, actual_value: str) -> str:
        """
        Anchoring - Set high anchor first
        
        Args:
            high_value: High anchor value
            actual_value: Actual value to present
        
        Returns:
            Anchoring message
        """
        return f"Bəzi klinikalarda {high_value}, amma bizdə {actual_value}."
    
    def handle_fear_then_relief(self, fear: str, relief: str) -> str:
        """
        Fear then relief - Present concern, then solution
        
        Args:
            fear: Fear/concern to present
            relief: Relief/solution to provide
        
        Returns:
            Fear-relief message
        """
        return f"⚠️ {fear}\n\n✅ Amma narahat olmayın: {relief}"
    
    def create_assumptive_close(self, assumed_action: str) -> str:
        """
        Assumptive close - Assume they've decided
        
        Args:
            assumed_action: Action assumed they'll take
        
        Returns:
            Assumptive close message
        """
        closes = [
            f"{assumed_action} üçün hansı vaxt sizə uyğundur?",
            f"Yaxşı! {assumed_action}. Hansı həkimi seçirsiniz?",
            f"Əla! {assumed_action} başlayaq. Sizə nömrə verim?"
        ]
        return random.choice(closes)
    
    def apply_pain_amplification(self, problem: str) -> str:
        """
        Pain amplification - Emphasize problem severity
        
        Args:
            problem: Problem to amplify
        
        Returns:
            Pain amplification message
        """
        amplifiers = [
            f"{problem} - bu sadəcə başlanğıc ola bilər. Daha pisə getməməsi üçün tez hərəkət lazımdır.",
            f"{problem} köhnəldikcə həll etmək çətinləşir. Erkən müdaxilə vacibdir.",
            f"{problem} həyat keyfiyyətinizə təsir edir. Bunu düzəltmək sizin əlinizdədir."
        ]
        return random.choice(amplifiers)
    
    def create_contrast_effect(self, bad_option: str, good_option: str) -> str:
        """
        Contrast effect - Show bad vs good option
        
        Args:
            bad_option: Less desirable option
            good_option: More desirable option
        
        Returns:
            Contrast message
        """
        return f"❌ {bad_option}\n\n✅ {good_option}\n\nSeçim sizindir."
    
    def apply_foot_in_door(self, small_ask: str) -> str:
        """
        Foot in door - Start with small request
        
        Args:
            small_ask: Small request to make
        
        Returns:
            Foot in door message
        """
        messages = [
            f"İlk öncə {small_ask}, sonra qərara gələ bilərsiniz.",
            f"Sadəcə {small_ask} - heç bir öhdəlik yoxdur.",
            f"{small_ask} etmək sizə daha aydın mənzərə verəcək."
        ]
        return random.choice(messages)
    
    def get_urgency_builder(self, context: str = 'health') -> str:
        """
        Build urgency message
        
        Args:
            context: Context for urgency
        
        Returns:
            Urgency message
        """
        builders = {
            'health': [
                "Göz sağlamlığı gözləməni sevmir. Tez hərəkət vacibdir.",
                "Hər gün əhəmiyyətlidir. Problemi erkən tutmaq daha yaxşı nəticə verir.",
                "Vaxt amili çox vacibdir. Gec qalmaq risklidir."
            ],
            'availability': [
                "Həkimlərin qrafiki tez dolur. Bu həftə hələ şansınız var.",
                "Ən yaxşı vaxtlar tez bitir. Tərəddüd etməyin.",
                "Bu fürsəti qaçırmayın - tez yazılın."
            ],
            'seasonal': [
                "Bu mövsüm ən uyğun vaxtdır. Sonra daha çətin olar.",
                "İndi ideal şəraitdir. Gözləmək əleyhinizədir.",
                "Bu dövr sağalma üçün idealdır. İstifadə edin."
            ]
        }
        
        context_builders = builders.get(context, builders['health'])
        return random.choice(context_builders)
    
    def generate_testimonial_style(self, topic: str) -> str:
        """
        Generate generic testimonial-style message
        
        Args:
            topic: Topic for testimonial
        
        Returns:
            Testimonial-style message
        """
        testimonials = {
            'surgery': "Xəstələrimiz əməliyyatdan sonra həyatlarının dəyişdiyini deyirlər.",
            'service': "Pasiyentlərimiz xidmətimizə və peşəkarlığımıza güvənirlər.",
            'results': "Uğurlu nəticələr və məmnun xəstələr bizim ən böyük mükafatımızdır.",
            'care': "Hörmətli münasibət və qayğı bizim əsas prinsipimizdir."
        }
        return testimonials.get(topic, testimonials['service'])
