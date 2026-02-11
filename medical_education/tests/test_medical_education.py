"""
Unit tests for medical education system.
"""

import pytest
import sys
from pathlib import Path

# Add medical_education to path
medical_education_path = Path(__file__).parent.parent
sys.path.insert(0, str(medical_education_path))

from core.content_retriever import MedicalContentRetriever
from core.progressive_disclosure import ProgressiveDisclosure
from core.personalization_engine import PersonalizationEngine
from core.semantic_search import SemanticSearch


class TestContentRetriever:
    """Test content retrieval functionality."""
    
    def setup_method(self):
        self.retriever = MedicalContentRetriever()
    
    def test_load_content(self):
        """Test that content is loaded."""
        assert len(self.retriever.content_cache) > 0
    
    def test_get_condition(self):
        """Test retrieving a condition."""
        cataract = self.retriever.get_condition('cataract')
        assert cataract is not None
        assert 'condition' in cataract
    
    def test_get_procedure(self):
        """Test retrieving a procedure."""
        laser = self.retriever.get_procedure('excimer_laser')
        assert laser is not None
        assert 'procedure' in laser
    
    def test_get_layer(self):
        """Test retrieving specific layer."""
        simple = self.retriever.get_layer('condition', 'cataract', 'simple_explanation', 'az')
        assert simple is not None
        assert isinstance(simple, str)
        assert len(simple) > 0
    
    def test_find_content_by_name(self):
        """Test finding content by name."""
        result = self.retriever.find_content_by_name('katarakta', 'az')
        assert result is not None
        assert result[0] == 'condition'
        assert result[1] == 'cataract'
    
    def test_list_conditions(self):
        """Test listing all conditions."""
        conditions = self.retriever.list_all_conditions('az')
        assert len(conditions) > 0
        assert all('id' in c and 'name' in c for c in conditions)


class TestProgressiveDisclosure:
    """Test progressive disclosure functionality."""
    
    def setup_method(self):
        self.progressive = ProgressiveDisclosure()
    
    def test_get_first_layer(self):
        """Test getting first layer."""
        layer = self.progressive.get_next_layer('condition', 'cataract', 0, 'az')
        assert layer['layer_name'] == 'simple_explanation'
        assert layer['content'] is not None
        assert layer['has_more'] is True
    
    def test_get_second_layer(self):
        """Test getting second layer."""
        layer = self.progressive.get_next_layer('condition', 'cataract', 1, 'az')
        assert layer['layer_name'] == 'symptoms'
        assert layer['content'] is not None
    
    def test_format_for_chat(self):
        """Test formatting content for chat."""
        layer = self.progressive.get_next_layer('condition', 'cataract', 0, 'az')
        formatted = self.progressive.format_for_chat(layer, 'az')
        assert isinstance(formatted, str)
        assert len(formatted) > 0
    
    def test_get_summary(self):
        """Test getting summary."""
        summary = self.progressive.get_summary('condition', 'cataract', 'az')
        assert isinstance(summary, str)
        assert len(summary) > 0


class TestPersonalizationEngine:
    """Test personalization functionality."""
    
    def setup_method(self):
        self.personalizer = PersonalizationEngine()
    
    def test_detect_knowledge_level_lay(self):
        """Test detecting lay knowledge level."""
        messages = ["gözüm dumanlıdır", "görə bilmirəm"]
        level = self.personalizer.detect_knowledge_level(messages)
        assert level == 'lay'
    
    def test_detect_knowledge_level_advanced(self):
        """Test detecting advanced knowledge level."""
        messages = ["fakoemulsifikasiya haqqında", "intraokulyar lens", "buynuz qişa topoqrafiyası"]
        level = self.personalizer.detect_knowledge_level(messages)
        assert level == 'advanced'
    
    def test_detect_emotional_state_anxious(self):
        """Test detecting anxious state."""
        message = "çox qorxuram, təhlükəlidir?"
        state = self.personalizer.detect_emotional_state(message, 'az')
        assert state == 'anxious'
    
    def test_detect_emotional_state_neutral(self):
        """Test detecting neutral state."""
        message = "katarakta haqqında məlumat"
        state = self.personalizer.detect_emotional_state(message, 'az')
        assert state == 'neutral'
    
    def test_personalize_content_anxious(self):
        """Test personalizing for anxious patient."""
        content = "Katarakta əməliyyatı."
        personalized = self.personalizer.personalize_content(
            content,
            emotional_state='anxious',
            language='az'
        )
        assert '💙' in personalized  # Reassurance added
        assert 'Narahat olmayın' in personalized


class TestSemanticSearch:
    """Test semantic search functionality."""
    
    def setup_method(self):
        self.search = SemanticSearch()
    
    def test_search_finds_content(self):
        """Test that search finds relevant content."""
        results = self.search.search('katarakta', 'az', limit=5)
        assert len(results) > 0
        assert results[0]['id'] == 'cataract'
    
    def test_search_with_synonym(self):
        """Test search with synonym."""
        results = self.search.search('mirvari suyu', 'az', limit=5)
        assert len(results) > 0
        # Should find cataract
        assert any(r['id'] == 'cataract' for r in results)
    
    def test_search_relevance_ranking(self):
        """Test that results are ranked by relevance."""
        results = self.search.search('katarakta', 'az', limit=5)
        # First result should be most relevant
        if len(results) > 1:
            assert results[0]['relevance'] >= results[1]['relevance']
    
    def test_suggest_queries(self):
        """Test query suggestions."""
        suggestions = self.search.suggest_queries('kata', 'az', limit=5)
        assert len(suggestions) > 0
        # Should suggest 'Katarakta'
        assert any('katarakta' in s.lower() for s in suggestions)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
