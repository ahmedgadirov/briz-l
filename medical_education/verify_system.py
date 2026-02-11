#!/usr/bin/env python3
"""
Quick verification script for medical education system.
Tests core functionality without requiring pytest.
"""

import sys
from pathlib import Path

# Add medical_education to path
medical_education_path = Path(__file__).parent
sys.path.insert(0, str(medical_education_path))

from core.content_retriever import MedicalContentRetriever
from core.progressive_disclosure import ProgressiveDisclosure
from core.personalization_engine import PersonalizationEngine
from core.semantic_search import SemanticSearch


def test_content_retriever():
    """Test content retrieval."""
    print("\n🧪 Testing Content Retriever...")
    
    retriever = MedicalContentRetriever()
    
    # Test 1: Content loaded
    assert len(retriever.content_cache) > 0, "Content cache is empty!"
    print(f"✅ Loaded {len(retriever.content_cache)} content files")
    
    # Test 2: Get condition
    cataract = retriever.get_condition('cataract')
    assert cataract is not None, "Cataract content not found!"
    print("✅ Retrieved cataract condition")
    
    # Test 3: Get layer
    simple = retriever.get_layer('condition', 'cataract', 'simple_explanation', 'az')
    assert simple is not None and len(simple) > 0, "Layer retrieval failed!"
    print("✅ Retrieved simple explanation layer")
    
    # Test 4: Find by name
    result = retriever.find_content_by_name('katarakta', 'az')
    assert result == ('condition', 'cataract'), "Find by name failed!"
    print("✅ Found content by name")
    
    print("✅ Content Retriever: ALL TESTS PASS")


def test_progressive_disclosure():
    """Test progressive disclosure."""
    print("\n🧪 Testing Progressive Disclosure...")
    
    progressive = ProgressiveDisclosure()
    
    # Test 1: Get first layer
    layer = progressive.get_next_layer('condition', 'cataract', 0, 'az')
    assert layer['layer_name'] == 'simple_explanation', "Wrong layer name!"
    assert layer['has_more'] is True, "Should have more layers!"
    print("✅ Got first layer (simple_explanation)")
    
    # Test 2: Get second layer
    layer = progressive.get_next_layer('condition', 'cataract', 1, 'az')
    assert layer['layer_name'] == 'symptoms', "Wrong second layer!"
    print("✅ Got second layer (symptoms)")
    
    # Test 3: Format for chat
    formatted = progressive.format_for_chat(layer, 'az')
    assert len(formatted) > 0, "Formatted content is empty!"
    print("✅ Formatted content for chat")
    
    print("✅ Progressive Disclosure: ALL TESTS PASS")


def test_personalization():
    """Test personalization engine."""
    print("\n🧪 Testing Personalization Engine...")
    
    personalizer = PersonalizationEngine()
    
    # Test 1: Detect lay knowledge level
    messages = ["gözüm dumanlıdır", "görə bilmirəm"]
    level = personalizer.detect_knowledge_level(messages)
    assert level == 'lay', f"Expected 'lay', got '{level}'"
    print(f"✅ Detected knowledge level: {level}")
    
    # Test 2: Detect anxious state
    message = "çox qorxuram, təhlükəlidir?"
    state = personalizer.detect_emotional_state(message, 'az')
    assert state == 'anxious', f"Expected 'anxious', got '{state}'"
    print(f"✅ Detected emotional state: {state}")
    
    # Test 3: Personalize content
    content = "Katarakta əməliyyatı."
    personalized = personalizer.personalize_content(
        content,
        emotional_state='anxious',
        language='az'
    )
    assert '💙' in personalized, "Reassurance emoji not found!"
    print("✅ Personalized content for anxious patient")
    
    print("✅ Personalization Engine: ALL TESTS PASS")


def test_semantic_search():
    """Test semantic search."""
    print("\n🧪 Testing Semantic Search...")
    
    search = SemanticSearch()
    
    # Test 1: Basic search
    results = search.search('katarakta', 'az', limit=5)
    assert len(results) > 0, "No search results!"
    assert results[0]['id'] == 'cataract', "Wrong top result!"
    print(f"✅ Search found {len(results)} results")
    
    # Test 2: Synonym search
    results = search.search('mirvari suyu', 'az', limit=5)
    assert any(r['id'] == 'cataract' for r in results), "Synonym search failed!"
    print("✅ Synonym search works")
    
    # Test 3: Query suggestions
    suggestions = search.suggest_queries('kata', 'az', limit=5)
    assert len(suggestions) > 0, "No suggestions!"
    print(f"✅ Generated {len(suggestions)} query suggestions")
    
    print("✅ Semantic Search: ALL TESTS PASS")


def demonstrate_usage():
    """Demonstrate the system in action."""
    print("\n" + "="*60)
    print("📚 MEDICAL EDUCATION SYSTEM DEMO")
    print("="*60)
    
    progressive = ProgressiveDisclosure()
    personalizer = PersonalizationEngine()
    
    # Demo 1: Progressive disclosure
    print("\n--- Demo 1: Progressive Disclosure ---")
    print("User: Katarakta nədir?\n")
    
    layer = progressive.get_next_layer('condition', 'cataract', 0, 'az')
    message = progressive.format_for_chat(layer, 'az')
    print("Bot:", message[:300] + "...\n")
    
    print("User: Daha ətraflı\n")
    layer = progressive.get_next_layer('condition', 'cataract', 1, 'az')
    message = progressive.format_for_chat(layer, 'az')
    print("Bot:", message[:200] + "...\n")
    
    # Demo 2: Personalization
    print("\n--- Demo 2: Personalization for Anxious Patient ---")
    print("User: Əməliyyatdan çox qorxuram, ağrılıdırmı?\n")
    
    content = "Katarakta əməliyyatı lokal anesteziya ilə edilir."
    personalized = personalizer.personalize_content(
        content,
        knowledge_level='lay',
        emotional_state='anxious',
        language='az'
    )
    print("Bot:", personalized[:250] + "...\n")
    
    # Demo 3: Multi-language
    print("\n--- Demo 3: Multi-Language Support ---")
    layer_az = progressive.get_next_layer('condition', 'cataract', 0, 'az')
    layer_ru = progressive.get_next_layer('condition', 'cataract', 0, 'ru')
    layer_en = progressive.get_next_layer('condition', 'cataract', 0, 'en')
    
    print("Azerbaijani:", progressive.format_for_chat(layer_az, 'az')[:100] + "...")
    print("Russian:", progressive.format_for_chat(layer_ru, 'ru')[:100] + "...")
    print("English:", progressive.format_for_chat(layer_en, 'en')[:100] + "...")


def main():
    """Run all tests and demo."""
    print("="*60)
    print("🚀 MEDICAL EDUCATION SYSTEM VERIFICATION")
    print("="*60)
    
    try:
        test_content_retriever()
        test_progressive_disclosure()
        test_personalization()
        test_semantic_search()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        
        demonstrate_usage()
        
        print("\n" + "="*60)
        print("🎉 VERIFICATION COMPLETE - System is working correctly!")
        print("="*60)
        
        return 0
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
