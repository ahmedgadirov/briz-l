import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from triage_system.core.triage_decision import TriageDecisionEngine

class TestTriageSystem:
    
    @pytest.fixture
    def triage_engine(self):
        """Create a triage engine instance for testing."""
        return TriageDecisionEngine()
    
    def test_emergency_sudden_vision_loss(self, triage_engine):
        """Test emergency triage for sudden vision loss."""
        
        user_message = "birdən sağ gözümlə heç nə görmürəm, qara oldu"
        patient_data = {'age': 65, 'has_diabetes': True}
        
        report = triage_engine.triage(user_message, patient_data, 'az')
        
        assert report['urgency_level'] == 'emergency'
        assert report['adjusted_severity'] >= 9
        assert report['symptom_identified'] == 'sudden_vision_loss'
        assert len(report['recommendations']) > 0
        assert 'dərhal' in report['recommendations'][0].lower() or 'təcili' in report['recommendations'][0].lower()
    
    def test_urgent_flashes_floaters(self, triage_engine):
        """Test urgent triage for retinal detachment symptoms."""
        
        user_message = "işıq çaxmaları görürəm və qaranlıq nöqtələr var"
        patient_data = {'age': 50, 'previous_retinal_detachment': True}
        
        report = triage_engine.triage(user_message, patient_data, 'az')
        
        # Should be urgent or emergency due to retinal detachment risk
        assert report['urgency_level'] in ['emergency', 'urgent']
        assert report['adjusted_severity'] >= 8
        assert report['symptom_identified'] == 'flashes_floaters'
        # Check for safety alert about retinal detachment
        assert any('retinal' in alert.lower() or 'retina' in alert.lower() 
                   for alert in report['safety_alerts'])
    
    def test_routine_gradual_blur(self, triage_engine):
        """Test routine triage for gradual vision changes."""
        
        user_message = "son 6 ayda yavaş-yavaş dumanlı görürəm"
        patient_data = {'age': 70}
        
        report = triage_engine.triage(user_message, patient_data, 'az')
        
        # Should be routine or soon, not urgent/emergency
        assert report['urgency_level'] in ['routine', 'soon']
        assert report['adjusted_severity'] < 7
        assert report['symptom_identified'] in ['gradual_blurry_vision', 'unspecified']
    
    def test_risk_factor_escalation(self, triage_engine):
        """Test that risk factors increase severity."""
        
        user_message = "dumanlı görürəm"
        
        # Without risk factors
        report1 = triage_engine.triage(user_message, {'age': 30}, 'az')
        
        # With multiple risk factors
        report2 = triage_engine.triage(
            user_message,
            {
                'age': 70,
                'has_diabetes': True,
                'only_functional_eye': True
            },
            'az'
        )
        
        # Adjusted severity should be higher with risk factors
        assert report2['adjusted_severity'] > report1['adjusted_severity']
        assert len(report2['risk_factors']) >= 3
    
    def test_chemical_burn_emergency(self, triage_engine):
        """Test chemical burn is classified as emergency."""
        
        user_message = "gözümə kimyəvi maddə dəydi, çox yanır"
        patient_data = {'age': 35}
        
        report = triage_engine.triage(user_message, patient_data, 'az')
        
        assert report['urgency_level'] == 'emergency'
        assert report['symptom_identified'] == 'chemical_burn'
        # Should have first aid recommendation about irrigating
        assert any('yuyun' in rec.lower() or 'su' in rec.lower() 
                   for rec in report['recommendations'])
    
    def test_eye_trauma_emergency(self, triage_engine):
        """Test eye trauma is classified as emergency."""
        
        user_message = "gözümü vurdu, çox ağrıyır"
        patient_data = {'age': 25}
        
        report = triage_engine.triage(user_message, patient_data, 'az')
        
        assert report['urgency_level'] == 'emergency'
        assert report['symptom_identified'] == 'eye_trauma'
        assert report['adjusted_severity'] >= 9
    
    def test_dry_eyes_routine(self, triage_engine):
        """Test dry eyes is routine priority."""
        
        user_message = "gözlərim quru, qum kimi hiss edirəm"
        patient_data = {'age': 40}
        
        report = triage_engine.triage(user_message, patient_data, 'az')
        
        assert report['urgency_level'] in ['routine', 'elective']
        assert report['symptom_identified'] == 'dry_eyes'
        assert report['adjusted_severity'] <= 5
    
    def test_pediatric_case_escalation(self, triage_engine):
        """Test that pediatric cases get appropriate attention."""
        
        user_message = "uşağın gözü qırmızı"
        patient_data = {'age': 3}
        
        report = triage_engine.triage(user_message, patient_data, 'az')
        
        # Should have pediatric safety alert
        assert any('pediatric' in alert.lower() or 'uşaq' in alert.lower() 
                   for alert in report['safety_alerts'])
        # Severity should be escalated due to age
        assert len(report['risk_factors']) >= 1
    
    def test_only_functional_eye_critical(self, triage_engine):
        """Test that only functional eye cases are flagged as critical."""
        
        user_message = "dumanlı görürəm"
        patient_data = {'age': 55, 'only_functional_eye': True}
        
        report = triage_engine.triage(user_message, patient_data, 'az')
        
        # Should have risk factor for only functional eye
        assert any('tək işləyən göz' in factor.lower() or 'only functional' in factor.lower()
                   for factor in report['risk_factors'])
        # Severity should be escalated
        assert report['adjusted_severity'] > report['base_severity']
    
    def test_duration_impact(self, triage_engine):
        """Test that sudden onset increases severity."""
        
        user_message = "dumanlı görürəm"
        
        # Sudden onset
        report1 = triage_engine.triage(
            user_message,
            {'age': 50, 'symptom_duration': 'birdən başladı'},
            'az'
        )
        
        # Gradual over months
        report2 = triage_engine.triage(
            user_message,
            {'age': 50, 'symptom_duration': 'aylar ərzində'},
            'az'
        )
        
        # Sudden onset should have higher severity
        assert report1['adjusted_severity'] > report2['adjusted_severity']
    
    def test_diabetic_vision_change_alert(self, triage_engine):
        """Test that diabetic patients with vision changes get special attention."""
        
        user_message = "son günlər dumanlı görürəm"
        patient_data = {'age': 60, 'has_diabetes': True}
        
        report = triage_engine.triage(user_message, patient_data, 'az')
        
        # Should have diabetes risk factor
        assert any('diabet' in factor.lower() for factor in report['risk_factors'])
        # Should have diabetic retinopathy safety check
        assert any('diabet' in alert.lower() or 'retinopathy' in alert.lower()
                   for alert in report['safety_alerts'])
    
    def test_russian_language(self, triage_engine):
        """Test triage works with Russian language."""
        
        user_message = "внезапная потеря зрения"
        patient_data = {'age': 65}
        
        report = triage_engine.triage(user_message, patient_data, 'ru')
        
        assert report['urgency_level'] == 'emergency'
        assert report['symptom_identified'] == 'sudden_vision_loss'
    
    def test_english_language(self, triage_engine):
        """Test triage works with English language."""
        
        user_message = "sudden vision loss in my right eye"
        patient_data = {'age': 65}
        
        report = triage_engine.triage(user_message, patient_data, 'en')
        
        assert report['urgency_level'] == 'emergency'
        assert report['symptom_identified'] == 'sudden_vision_loss'
    
    def test_report_structure(self, triage_engine):
        """Test that triage report has all required fields."""
        
        user_message = "gözüm ağrıyır"
        patient_data = {'age': 40}
        
        report = triage_engine.triage(user_message, patient_data, 'az')
        
        # Check all required fields are present
        required_fields = [
            'timestamp', 'patient_id', 'symptom_identified',
            'base_severity', 'adjusted_severity', 'risk_factors',
            'urgency_level', 'urgency_details', 'protocol',
            'recommendations', 'safety_alerts', 'requires_human_review',
            'estimated_appointment_time'
        ]
        
        for field in required_fields:
            assert field in report, f"Missing required field: {field}"
        
        # Check data types
        assert isinstance(report['base_severity'], (int, float))
        assert isinstance(report['adjusted_severity'], (int, float))
        assert isinstance(report['risk_factors'], list)
        assert isinstance(report['recommendations'], list)
        assert isinstance(report['safety_alerts'], list)
        assert isinstance(report['requires_human_review'], bool)
