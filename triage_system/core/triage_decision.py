from typing import Dict, Any, List
# Use relative imports assuming this file is in triage_system/core/
from .severity_scorer import SeverityScorer
from .risk_assessor import RiskAssessor
from .urgency_calculator import UrgencyCalculator
import json
import os
from datetime import datetime, timedelta

class TriageDecisionEngine:
    """
    Main triage engine that coordinates all components.
    """
    
    def __init__(self, config_path: str = "triage_system/data/symptom_matrix.yml"):
        if not os.path.isabs(config_path):
             config_path = os.path.abspath(config_path)
             
        self.severity_scorer = SeverityScorer(config_path)
        self.risk_assessor = RiskAssessor(config_path)
        self.urgency_calculator = UrgencyCalculator()
    
    def triage(self, 
               user_message: str,
               patient_data: Dict[str, Any],
               language: str = 'az') -> Dict[str, Any]:
        """
        Complete triage assessment.
        
        Args:
            user_message: Patient's symptom description
            patient_data: Patient demographics and history
            language: Language code
            
        Returns:
            Complete triage report with recommendations
        """
        
        # Step 1: Score base severity
        base_severity, symptom_name, symptom_details = \
            self.severity_scorer.score_severity(user_message, language)
        
        # Step 2: Assess risk factors
        adjusted_severity, risk_factors = \
            self.risk_assessor.assess_risk(base_severity, patient_data)
        
        # Step 3: Calculate urgency
        urgency_level, urgency_details = \
            self.urgency_calculator.calculate_urgency(
                adjusted_severity,
                symptom_details,
                risk_factors
            )
        
        # Step 4: Generate recommendations
        recommendations = self._generate_recommendations(
            urgency_level,
            symptom_details,
            patient_data,
            language
        )
        
        # Step 5: Safety checks
        safety_alerts = self._check_safety_protocols(
            symptom_name,
            urgency_level,
            patient_data
        )
        
        # Compile triage report
        triage_report = {
            'timestamp': str(datetime.now()),
            'patient_id': patient_data.get('id', 'unknown'),
            'symptom_identified': symptom_name,
            'base_severity': base_severity,
            'adjusted_severity': round(adjusted_severity, 2),
            'risk_factors': risk_factors,
            'urgency_level': urgency_level,
            'urgency_details': urgency_details,
            'protocol': symptom_details.get('protocol', 'general_assessment'),
            'recommendations': recommendations,
            'safety_alerts': safety_alerts,
            'requires_human_review': urgency_level in ['emergency', 'urgent'],
            'estimated_appointment_time': self._estimate_appointment_time(urgency_level, language)
        }
        
        return triage_report
    
    def _generate_recommendations(self,
                                  urgency: str,
                                  symptom_details: Dict,
                                  patient_data: Dict,
                                  language: str = 'az') -> List[str]:
        """Generate actionable recommendations."""
        
        recommendations = []
        
        # Simple localization for recommendations
        if language == 'az':
            if urgency == 'emergency':
                recommendations.extend([
                    "❗ Dərhal klinikamıza zəng edin",
                    "☎️ Telefon: +994 12 541 19 00",
                    "📱 WhatsApp: https://wa.me/994555512400",
                    "🏥 Yaxınlıqdakı təcili göz yardımına gedin"
                ])
                protocol = symptom_details.get('protocol')
                if protocol == 'chemical_injury':
                    recommendations.insert(0, "⚠️ ƏVVƏLCƏ: 15 dəqiqə təmiz su ilə gözü yuyun")
                elif protocol == 'eye_trauma':
                    recommendations.insert(0, "⚠️ Göz ovuşdurmayın, təzyiq etməyin")
            elif urgency == 'urgent':
                recommendations.extend([
                    "📞 Bu gün və ya sabah üçün təcili müayinə",
                    "WhatsApp yazın: https://wa.me/994555512400",
                    "Zəng edin: +994 12 541 19 00"
                ])
            elif urgency == 'soon':
                recommendations.extend([
                    "📋 Bu həftə müayinə tövsiyə olunur",
                    "Əlverişli vaxt seçin və qeydiyyat edin",
                    "WhatsApp: https://wa.me/994555512400"
                ])
            else:
                 recommendations.extend([
                    "✅ Planlı müayinə",
                    "Sizə uyğun tarixi seçə bilərsiniz",
                    "Əlaqə: +994 12 541 19 00"
                ])
                
            if symptom_details:
                timeframe = symptom_details.get('timeframe')
                if timeframe:
                    # In a real app we would localize the timeframe string too
                    recommendations.append(f"⏰ Tövsiyə olunan müddət: {timeframe}")
                    
        elif language == 'ru':
             if urgency == 'emergency':
                recommendations.extend([
                    "❗ Немедленно позвоните в нашу клинику",
                    "☎️ Телефон: +994 12 541 19 00",
                    "📱 WhatsApp: https://wa.me/994555512400",
                    "🏥 Обратитесь в ближайшую неотложную глазную помощь"
                ])
             # ... (Add Russian logic if needed, keeping it simple for now)
        else: # English fallback
             if urgency == 'emergency':
                recommendations.extend([
                    "❗ Call our clinic immediately",
                    "☎️ Phone: +994 12 541 19 00",
                    "📱 WhatsApp: https://wa.me/994555512400",
                    "🏥 Go to the nearest emergency eye care"
                ])

        return recommendations
    
    def _check_safety_protocols(self,
                                symptom_name: str,
                                urgency: str,
                                patient_data: Dict) -> List[str]:
        """Check for safety concerns that need immediate attention."""
        
        alerts = []
        
        # Critical combinations
        if patient_data.get('only_functional_eye') and urgency in ['emergency', 'urgent']:
            alerts.append("⚠️ CRITICAL: Only functional eye - prioritize immediately")
        
        if symptom_name == 'sudden_vision_loss' and int(patient_data.get('age', 0) or 0) > 50:
            alerts.append("⚠️ Possible stroke/retinal artery occlusion - emergency")
        
        if symptom_name in ['flashes_floaters'] and patient_data.get('previous_retinal_detachment'):
            alerts.append("⚠️ High risk retinal detachment - urgent assessment needed")
        
        if patient_data.get('has_diabetes') and 'vision' in (symptom_name or ""):
            alerts.append("⚠️ Diabetic patient with vision change - check for retinopathy")
        
        # Pediatric alerts
        if int(patient_data.get('age', 100) or 100) < 5:
            alerts.append("⚠️ Pediatric case - ensure appropriate specialist")
        
        return alerts
    
    def _estimate_appointment_time(self, urgency: str, language: str = 'az') -> str:
        """Estimate when appointment should occur."""
        
        now = datetime.now()
        
        if language == 'az':
            if urgency == 'emergency':
                return "İndi (dərhal)"
            elif urgency == 'urgent':
                target = now + timedelta(hours=12)
                return target.strftime("%d.%m.%Y, %H:00-a qədər")
            elif urgency == 'soon':
                target = now + timedelta(days=5)
                return target.strftime("%d.%m.%Y-a qədər")
            elif urgency == 'routine':
                target = now + timedelta(weeks=3)
                return target.strftime("%d.%m.%Y-a qədər")
            else:
                return "Çevik"
        else:
            return "ASAP" if urgency == 'emergency' else "Flexible"
