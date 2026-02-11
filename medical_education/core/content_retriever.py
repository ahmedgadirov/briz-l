import yaml
import os
from typing import Dict, List, Optional, Any
from pathlib import Path


class MedicalContentRetriever:
    """
    Retrieves and manages medical education content.
    Preloads all YAML content for fast access.
    """
    
    def __init__(self, content_dir: str = "medical_education/content"):
        self.content_dir = Path(content_dir)
        self.content_cache = {}
        self._load_all_content()
    
    def _load_all_content(self):
        """Preload all content into memory for fast access."""
        
        for category in ['conditions', 'procedures', 'prevention', 'postop']:
            category_path = self.content_dir / category
            if category_path.exists():
                for yml_file in category_path.glob('*.yml'):
                    with open(yml_file, 'r', encoding='utf-8') as f:
                        content = yaml.safe_load(f)
                        content_id = yml_file.stem
                        self.content_cache[f"{category}/{content_id}"] = content
    
    def get_condition(self, condition_id: str, language: str = 'az') -> Optional[Dict]:
        """Retrieve condition content."""
        key = f"conditions/{condition_id}"
        return self.content_cache.get(key)
    
    def get_procedure(self, procedure_id: str, language: str = 'az') -> Optional[Dict]:
        """Retrieve procedure content."""
        key = f"procedures/{procedure_id}"
        return self.content_cache.get(key)
    
    def get_layer(self, 
                  content_type: str,
                  content_id: str,
                  layer: str,
                  language: str = 'az') -> Optional[Any]:
        """
        Get specific layer of content.
        
        Args:
            content_type: 'condition' or 'procedure'
            content_id: e.g., 'cataract'
            layer: e.g., 'simple_explanation', 'medical_details', 'faqs'
            language: 'az', 'ru', 'en'
        
        Returns:
            Content for that layer in specified language
        """
        
        if content_type == 'condition':
            content = self.get_condition(content_id)
        elif content_type == 'procedure':
            content = self.get_procedure(content_id)
        else:
            return None
        
        if not content:
            return None
        
        # Navigate to layer
        layer_content = content.get(layer)
        if not layer_content:
            # Fallback to nested structure if needed
            category_key = 'condition' if content_type == 'condition' else 'procedure'
            layer_content = content.get(category_key, {}).get(layer)
        
        if not layer_content:
            return None
        
        # Extract language-specific content if available
        if isinstance(layer_content, dict) and language in layer_content:
            return layer_content[language]
        
        return layer_content
    
    def search_faqs(self, query: str, language: str = 'az') -> List[Dict]:
        """
        Search FAQs across all content.
        
        Returns list of matching FAQ entries.
        """
        
        results = []
        query_lower = query.lower()
        
        for key, content in self.content_cache.items():
            # Extract FAQs
            if 'condition' in content:
                faqs = content['condition'].get('faqs', [])
            elif 'procedure' in content:
                faqs = content['procedure'].get('faqs', [])
            else:
                continue
            
            for faq in faqs:
                question = faq.get('question', {}).get(language, '')
                answer = faq.get('answer', {}).get(language, '')
                
                # Simple keyword matching
                if query_lower in question.lower() or query_lower in answer.lower():
                    results.append({
                        'source': key,
                        'question': question,
                        'answer': answer,
                        'category': faq.get('category', 'general')
                    })
        
        return results
    
    def get_related_content(self, content_id: str) -> List[str]:
        """Get related conditions/procedures."""
        
        # Try conditions first
        content = self.get_condition(content_id)
        if content and 'condition' in content:
            related = content['condition'].get('related_conditions', [])
            return [r['name'] for r in related]
        
        # Try procedures
        content = self.get_procedure(content_id)
        if content and 'procedure' in content:
            related = content['procedure'].get('related_procedures', [])
            return [r['name'] for r in related]
        
        return []
    
    def find_content_by_name(self, name: str, language: str = 'az') -> Optional[tuple]:
        """
        Find content by searching for name/alternate names.
        
        Returns:
            (content_type, content_id) tuple or None
        """
        name_lower = name.lower()
        
        for key, content in self.content_cache.items():
            content_type_key = 'condition' if 'condition' in content else 'procedure'
            content_data = content[content_type_key]
            
            # Check main name
            main_name = content_data.get('name', {}).get(language, '').lower()
            if name_lower in main_name or main_name in name_lower:
                category, content_id = key.split('/')
                return (content_type_key, content_id)
            
            # Check alternate names
            alt_names = content_data.get('alternate_names', {}).get(language, [])
            for alt_name in alt_names:
                if name_lower in alt_name.lower() or alt_name.lower() in name_lower:
                    category, content_id = key.split('/')
                    return (content_type_key, content_id)
        
        return None
    
    def list_all_conditions(self, language: str = 'az') -> List[Dict[str, str]]:
        """List all available conditions."""
        conditions = []
        
        for key, content in self.content_cache.items():
            if 'condition' in content:
                condition_data = content['condition']
                conditions.append({
                    'id': condition_data['id'],
                    'name': condition_data['name'].get(language, condition_data['name'].get('az'))
                })
        
        return conditions
    
    def list_all_procedures(self, language: str = 'az') -> List[Dict[str, str]]:
        """List all available procedures."""
        procedures = []
        
        for key, content in self.content_cache.items():
            if 'procedure' in content:
                procedure_data = content['procedure']
                procedures.append({
                    'id': procedure_data['id'],
                    'name': procedure_data['name'].get(language, procedure_data['name'].get('az'))
                })
        
        return procedures
