#!/usr/bin/env python3
"""
Quick Intelligence System Test
Tests the 5-layer intelligence architecture
"""

import sys
sys.path.insert(0, '.')

from intelligence.user_profiler import UserProfiler, generate_adaptive_prompt
from intelligence.symptom_triage import SymptomTriage
from intelligence.knowledge_base import (
    detect_knowledge_level,
    match_symptom_to_conditions,
    get_surgery_info
)

def test_user_profiling():
    """Test user profiling system"""
    print("=" * 60)
    print("🧠 TEST 1: USER PROFILING")
    print("=" * 60)
    
    profiler = UserProfiler()
    
    test_cases = [
        ("gözüm pis görür, nə edim bilmirəm", "beginner"),
        ("katarakta əməliyyatı nə qədər çəkir?", "intermediate"),
        ("Fakoemulsifikasiya zamanı IOL seçimi", "expert"),
    ]
    
    for message, expected_level in test_cases:
        profile = profiler.analyze_user("test_user", message, [])
        print(f"\n📝 Message: \"{message}\"")
        print(f"   Knowledge Level: {profile['knowledge_level']} (Expected: {expected_level})")
        print(f"   Intent: {profile['intent']}")
        print(f"   Confidence: {profile['confidence_level']}")
        print(f"   ✅ PASS" if profile['knowledge_level'] == expected_level else "   ❌ FAIL")
    
    print("\n" + "=" * 60)

def test_symptom_triage():
    """Test symptom triage system"""
    print("=" * 60)
    print("🩺 TEST 2: SYMPTOM TRIAGE")
    print("=" * 60)
    
    triage = SymptomTriage()
    
    test_cases = [
        ("uzağı görmürəm", "routine", ["Excimer laser"]),
        ("dumanlı görürəm", "urgent", ["Katarakta (mirvari suyu)"]),
        ("göz çox ağrıyır, qəfil görmə azaldı", "emergency", []),
    ]
    
    for message, expected_urgency, expected_surgeries in test_cases:
        result = triage.analyze_symptoms("test_user", message, "beginner")
        print(f"\n📝 Message: \"{message}\"")
        print(f"   Urgency: {result['urgency']} (Expected: {expected_urgency})")
        print(f"   Conditions: {result['matched_conditions']}")
        print(f"   Surgeries: {result['suggested_surgeries']}")
        print(f"   Questions: {len(result['diagnostic_questions'])} diagnostic questions")
        urgency_match = result['urgency'] == expected_urgency
        print(f"   ✅ PASS" if urgency_match else "   ❌ FAIL")
    
    print("\n" + "=" * 60)

def test_knowledge_base():
    """Test knowledge base"""
    print("=" * 60)
    print("📚 TEST 3: KNOWLEDGE BASE")
    print("=" * 60)
    
    # Test surgery info
    print("\n🔍 Testing Surgery Information:")
    surgery = get_surgery_info("excimer_laser", "beginner")
    if surgery:
        print(f"   Surgery: {surgery['name']}")
        print(f"   Description: {surgery['description'][:50]}...")
        print(f"   Explanation: {surgery['explanation'][:60]}...")
        print(f"   ✅ Surgery info retrieved")
    else:
        print(f"   ❌ Failed to get surgery info")
    
    # Test symptom matching
    print("\n🔍 Testing Symptom Matching:")
    matches = match_symptom_to_conditions("dumanlı görürəm")
    if matches:
        print(f"   Matched {len(matches)} conditions")
        for match in matches[:2]:
            if 'conditions' in match:
                print(f"   Condition: {match['conditions']}")
                print(f"   Surgeries: {match['surgeries']}")
                print(f"   Urgency: {match['urgency']}")
        print(f"   ✅ Symptom matching works")
    else:
        print(f"   ❌ No matches found")
    
    # Test knowledge level detection
    print("\n🔍 Testing Knowledge Level Detection:")
    test_messages = [
        ("görmürəm", "beginner"),
        ("katarakta əməliyyatı", "intermediate"),
        ("IOL implantasiyası", "expert")
    ]
    
    for message, expected in test_messages:
        level = detect_knowledge_level(message)
        print(f"   \"{message}\" -> {level} (Expected: {expected})")
        print(f"   {'✅' if level == expected else '❌'}")
    
    print("\n" + "=" * 60)

def test_adaptive_prompt():
    """Test adaptive prompt generation"""
    print("=" * 60)
    print("💬 TEST 4: ADAPTIVE PROMPT GENERATION")
    print("=" * 60)
    
    profile = {
        'knowledge_level': 'beginner',
        'intent': 'symptom_inquiry',
        'confidence_level': 'lost',
        'conversation_stage': 'questioning'
    }
    
    triage_result = {
        'urgency': 'urgent',
        'matched_conditions': ['Katarakta'],
        'suggested_surgeries': ['Katarakta (mirvari suyu)']
    }
    
    prompt = generate_adaptive_prompt(profile, triage_result)
    print("\n📝 Generated Adaptive Prompt:")
    print(prompt[:200] + "...")
    print(f"\n✅ Prompt contains user level adaptation: {'Başlanğıc' in prompt}")
    print(f"✅ Prompt contains triage info: {'Tezliklə müayinə' in prompt}")
    
    print("\n" + "=" * 60)

def test_emergency_detection():
    """Test emergency detection"""
    print("=" * 60)
    print("🚨 TEST 5: EMERGENCY DETECTION")
    print("=" * 60)
    
    triage = SymptomTriage()
    
    emergency_messages = [
        "göz çox ağrıyır",
        "qəfil görmürəm",
        "işıq çaxması görürəm",
        "gözə zədə dəydi"
    ]
    
    for message in emergency_messages:
        is_emergency = triage.check_emergency_indicators(message)
        print(f"\n📝 Message: \"{message}\"")
        print(f"   Emergency Detected: {is_emergency}")
        print(f"   {'🚨 ALERT' if is_emergency else '✓ Normal'}")
    
    print("\n" + "=" * 60)

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "🧠 BRIZ-L INTELLIGENCE SYSTEM TESTS" + " " * 13 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")
    
    try:
        test_user_profiling()
        test_symptom_triage()
        test_knowledge_base()
        test_adaptive_prompt()
        test_emergency_detection()
        
        print("\n")
        print("╔" + "=" * 58 + "╗")
        print("║" + " " * 15 + "✅ ALL TESTS COMPLETED!" + " " * 19 + "║")
        print("╚" + "=" * 58 + "╝")
        print("\n")
        print("🎉 Your intelligent bot is ready!")
        print("📖 See INTELLIGENCE_GUIDE.md for usage examples")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
