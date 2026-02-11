#!/usr/bin/env python3
"""
Manual validation script for the triage system.
Run this to verify the triage logic works correctly.
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from triage_system.core.triage_decision import TriageDecisionEngine
import json

def print_header(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}")

def print_report(report, test_name):
    print(f"\n{test_name}")
    print(f"{'-'*70}")
    print(f"Symptom: {report['symptom_identified']}")
    print(f"Base Severity: {report['base_severity']}")
    print(f"Adjusted Severity: {report['adjusted_severity']}")
    print(f"Urgency: {report['urgency_level']} {report['urgency_details']['color']}")
    print(f"Risk Factors: {len(report['risk_factors'])}")
    for rf in report['risk_factors']:
        print(f"  - {rf}")
    if report['safety_alerts']:
        print(f"Safety Alerts:")
        for alert in report['safety_alerts']:
            print(f"  ⚠️  {alert}")
    print(f"Recommendations: {len(report['recommendations'])}")
    for i, rec in enumerate(report['recommendations'][:3], 1):
        print(f"  {i}. {rec}")
    print(f"✓ PASSED" if verify_report(report) else "✗ FAILED")

def verify_report(report):
    """Basic validation that report has all required fields."""
    required_fields = [
        'timestamp', 'patient_id', 'symptom_identified',
        'base_severity', 'adjusted_severity', 'risk_factors',
        'urgency_level', 'urgency_details', 'protocol',
        'recommendations', 'safety_alerts', 'requires_human_review',
        'estimated_appointment_time'
    ]
    return all(field in report for field in required_fields)

def main():
    print_header("TRIAGE SYSTEM VALIDATION")
    
    engine = TriageDecisionEngine()
    
    # Test 1: Emergency - Sudden vision loss
    print_header("TEST 1: Emergency - Sudden Vision Loss")
    report1 = engine.triage(
        "birdən sağ gözümlə heç nə görmürəm, qara oldu",
        {'age': 65, 'has_diabetes': True},
        'az'
    )
    print_report(report1, "Sudden vision loss with diabetes")
    assert report1['urgency_level'] == 'emergency', "Should be emergency"
    assert report1['adjusted_severity'] >= 9, "Should be severity 9+"
    
    # Test 2: Emergency - Chemical burn
    print_header("TEST 2: Emergency - Chemical Burn")
    report2 = engine.triage(
        "gözümə kimyəvi maddə dəydi, çox yanır",
        {'age': 35},
        'az'
    )
    print_report(report2, "Chemical burn")
    assert report2['urgency_level'] == 'emergency', "Should be emergency"
    assert report2['symptom_identified'] == 'chemical_burn', "Should identify chemical burn"
    
    # Test 3: Urgent - Flashes and floaters
    print_header("TEST 3: Urgent - Retinal Detachment Risk")
    report3 = engine.triage(
        "işıq çaxmaları görürəm və qaranlıq nöqtələr var",
        {'age': 50, 'previous_retinal_detachment': True},
        'az'
    )
    print_report(report3, "Flashes and floaters with RD history")
    assert report3['urgency_level'] in ['urgent', 'emergency'], "Should be urgent/emergency"
    assert len(report3['safety_alerts']) > 0, "Should have safety alerts"
    
    # Test 4: Routine - Gradual blurry vision
    print_header("TEST 4: Routine - Gradual Vision Changes")
    report4 = engine.triage(
        "son 6 ayda yavaş-yavaş dumanlı görürəm",
        {'age': 70},
        'az'
    )
    print_report(report4, "Gradual blurry vision")
    assert report4['urgency_level'] in ['routine', 'soon'], "Should be routine/soon"
    assert report4['adjusted_severity'] < 7, "Should be lower severity"
    
    # Test 5: Risk factor escalation
    print_header("TEST 5: Risk Factor Escalation")
    report5a = engine.triage(
        "dumanlı görürəm",
        {'age': 30},
        'az'
    )
    report5b = engine.triage(
        "dumanlı görürəm",
        {'age': 70, 'has_diabetes': True, 'only_functional_eye': True},
        'az'
    )
    print_report(report5a, "Blurry vision - no risk factors")
    print_report(report5b, "Blurry vision - multiple risk factors")
    assert report5b['adjusted_severity'] > report5a['adjusted_severity'], "Risk factors should escalate severity"
    assert len(report5b['risk_factors']) >= 3, "Should have 3+ risk factors"
    
    # Test 6: Russian language
    print_header("TEST 6: Russian Language Support")
    report6 = engine.triage(
        "внезапная потеря зрения",
        {'age': 65},
        'ru'
    )
    print_report(report6, "Russian: Sudden vision loss")
    assert report6['urgency_level'] == 'emergency', "Should work in Russian"
    
    # Test 7: Pediatric case
    print_header("TEST 7: Pediatric Case")
    report7 = engine.triage(
        "uşağın gözü qırmızı və ağrıyır",
        {'age': 3},
        'az'
    )
    print_report(report7, "Pediatric red eye with pain")
    assert any('uşaq' in alert.lower() or 'pediatric' in alert.lower() 
               for alert in report7['safety_alerts']), "Should have pediatric alert"
    
    print_header("VALIDATION COMPLETE")
    print("\n✅ All tests passed successfully!")
    print("\nThe triage system is working correctly and ready for integration.")

if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
