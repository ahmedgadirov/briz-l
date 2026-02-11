import yaml
from typing import Dict, List, Any, Tuple
from datetime import datetime

class RiskAssessor:
    """
    Evaluates patient risk factors and calculates risk-adjusted severity score.
    """
    
    def __init__(self, config_path: str = "triage_system/data/symptom_matrix.yml"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.modifiers = self.config.get('modifiers', {})
        self.duration_scaling = self.config.get('duration_scaling', {})
    
    def assess_risk(self, 
                    base_severity: float,
                    patient_data: Dict[str, Any]) -> Tuple[float, List[str]]:
        """
        Calculate risk-adjusted severity score.
        
        Args:
            base_severity: Base symptom severity (0-10)
            patient_data: Dictionary containing patient information
            
        Returns:
            (adjusted_severity, risk_factors_applied)
        """
        
        adjusted_severity = base_severity
        risk_factors_applied = []
        
        # Age modifiers
        age = patient_data.get('age')
        # Age might come as string from slots, try to convert
        if age:
            try:
                age = int(age)
                if age > 60 and 'age_over_60' in self.modifiers:
                    multiplier = self.modifiers['age_over_60']['multiplier']
                    adjusted_severity *= multiplier
                    risk_factors_applied.append(
                        f"Yaş 60+ ({self.modifiers['age_over_60']['reason']})"
                    )
                elif age < 5 and 'age_under_5' in self.modifiers:
                    multiplier = self.modifiers['age_under_5']['multiplier']
                    adjusted_severity *= multiplier
                    risk_factors_applied.append(
                        f"Uşaq <5 yaş ({self.modifiers['age_under_5']['reason']})"
                    )
            except ValueError:
                pass # Age is not a number, skip age checks
        
        # Medical history modifiers
        if patient_data.get('has_diabetes') and 'diabetes' in self.modifiers:
            multiplier = self.modifiers['diabetes']['multiplier']
            adjusted_severity *= multiplier
            risk_factors_applied.append(
                f"Şəkərli diabet ({self.modifiers['diabetes']['reason']})"
            )
        
        if patient_data.get('previous_retinal_detachment'):
            multiplier = self.modifiers['previous_retinal_detachment']['multiplier']
            adjusted_severity *= multiplier
            risk_factors_applied.append(
                f"Retina ayrılması tarixçəsi ({self.modifiers['previous_retinal_detachment']['reason']})"
            )
        
        if patient_data.get('only_functional_eye'):
            multiplier = self.modifiers['only_functional_eye']['multiplier']
            adjusted_severity *= multiplier
            risk_factors_applied.append(
                f"Tək işləyən göz ({self.modifiers['only_functional_eye']['reason']})"
            )
        
        if patient_data.get('bilateral_symptoms'):
            multiplier = self.modifiers['bilateral_symptoms']['multiplier']
            adjusted_severity *= multiplier
            risk_factors_applied.append(
                f"Hər iki göz ({self.modifiers['bilateral_symptoms']['reason']})"
            )
        
        if patient_data.get('is_pregnant'):
            multiplier = self.modifiers['pregnancy']['multiplier']
            adjusted_severity *= multiplier
            risk_factors_applied.append(
                f"Hamiləlik ({self.modifiers['pregnancy']['reason']})"
            )
        
        if patient_data.get('immunocompromised'):
            multiplier = self.modifiers['immunocompromised']['multiplier']
            adjusted_severity *= multiplier
            risk_factors_applied.append(
                f"İmmunitet zəifliyi ({self.modifiers['immunocompromised']['reason']})"
            )
        
        # Duration impact
        duration = patient_data.get('symptom_duration', '')
        if duration:
            duration = duration.lower()
            for duration_key, duration_data in self.duration_scaling.items():
                keywords = duration_data['keywords']
                if any(keyword in duration for keyword in keywords):
                    multiplier = duration_data['multiplier']
                    adjusted_severity *= multiplier
                    risk_factors_applied.append(f"Müddət faktoru: {duration_key}")
                    break
        
        # Cap at 10
        adjusted_severity = min(adjusted_severity, 10.0)
        
        return adjusted_severity, risk_factors_applied
