from typing import List, Dict, Optional, Tuple
from .content_retriever import MedicalContentRetriever


class SemanticSearch:
    """
    Semantic search for medical content.
    Handles multi-language queries, synonyms, and typos.
    """
    
    def __init__(self):
        self.retriever = MedicalContentRetriever()
        
        # Synonym mappings for better matching
        self.synonyms = {
            'az': {
                'katarakta': ['mirvari suyu', 'lens dumanlığı', 'kataract'],
                'lazer': ['lasik', 'prk', 'excimer', 'göz lazeri'],
                'qlaukoma': ['göz təzyiqi', 'glaucoma'],
                'şəkər': ['diabet', 'diabetic', 'şəkərli diabet'],
                'ağrı': ['sancı', 'acı', 'yanma'],
                'görmə': ['görmək', 'görüş', 'vision'],
                'əməliyyat': ['cərrahi', 'surgery', 'operasiya']
            },
            'ru': {
                'катаракта': ['помутнение хрусталика', 'бельмо'],
                'лазер': ['ласик', 'lasik', 'prk'],
                'глаукома': ['давление глаза'],
                'диабет': ['сахар', 'сахарный диабет'],
                'боль': ['болит', 'болезненно'],
                'операция': ['хирургия', 'оперативное']
            },
            'en': {
                'cataract': ['cloudy lens', 'lens opacity'],
                'laser': ['lasik', 'prk', 'refractive surgery'],
                'glaucoma': ['eye pressure'],
                'diabetes': ['diabetic', 'sugar'],
                'pain': ['hurt', 'ache'],
                'surgery': ['operation', 'procedure']
            }
        }
    
    def search(self, query: str, language: str = 'az', limit: int = 5) -> List[Dict]:
        """
        Search for relevant medical content.
        
        Args:
            query: User's search query
            language: Query language
            limit: Maximum number of results
        
        Returns:
            List of search results with relevance scores
        """
        
        results = []
        query_lower = query.lower()
        
        # Expand query with synonyms
        query_terms = self._expand_with_synonyms(query_lower, language)
        
        # Search in conditions and procedures
        all_content = {**self.retriever.content_cache}
        
        for key, content in all_content.items():
            score = self._calculate_relevance(content, query_terms, language)
            
            if score > 0:
                content_type_key = 'condition' if 'condition' in content else 'procedure'
                content_data = content[content_type_key]
                
                results.append({
                    'type': content_type_key,
                    'id': content_data['id'],
                    'name': content_data['name'].get(language, content_data['name'].get('az')),
                    'relevance': score,
                    'source_key': key
                })
        
        # Sort by relevance
        results.sort(key=lambda x: x['relevance'], reverse=True)
        
        return results[:limit]
    
    def _expand_with_synonyms(self, query: str, language: str) -> List[str]:
        """Expand query with synonyms."""
        terms = [query]
        
        synonyms = self.synonyms.get(language, {})
        
        for base_word, synonym_list in synonyms.items():
            if base_word in query:
                terms.extend(synonym_list)
            for synonym in synonym_list:
                if synonym in query:
                    terms.append(base_word)
                    terms.extend([s for s in synonym_list if s != synonym])
        
        return list(set(terms))
    
    def _calculate_relevance(self, content: Dict, query_terms: List[str], language: str) -> float:
        """Calculate relevance score for content."""
        score = 0.0
        
        content_type_key = 'condition' if 'condition' in content else 'procedure'
        content_data = content[content_type_key]
        
        # Check name (high weight)
        name = content_data.get('name', {}).get(language, '').lower()
        for term in query_terms:
            if term in name:
                score += 10.0
        
        # Check alternate names (medium-high weight)
        alt_names = content_data.get('alternate_names', {}).get(language, [])
        for alt_name in alt_names:
            for term in query_terms:
                if term in alt_name.lower():
                    score += 7.0
        
        # Check simple explanation (medium weight)
        simple_exp = content_data.get('simple_explanation', {}).get(language, '')
        for term in query_terms:
            if term in simple_exp.lower():
                score += 3.0
        
        # Check symptoms (medium weight)
        symptoms = content_data.get('symptoms', {})
        for stage_data in symptoms.values():
            if isinstance(stage_data, dict) and language in stage_data:
                symptom_text = ' '.join(stage_data[language]).lower()
                for term in query_terms:
                    if term in symptom_text:
                        score += 2.0
        
        # Check FAQs (low weight)
        faqs = content_data.get('faqs', [])
        for faq in faqs:
            question = faq.get('question', {}).get(language, '').lower()
            answer = faq.get('answer', {}).get(language, '').lower()
            for term in query_terms:
                if term in question or term in answer:
                    score += 1.0
        
        return score
    
    def find_similar_conditions(self, condition_id: str, limit: int = 3) -> List[Dict]:
        """Find conditions similar to the given one."""
        
        # This is a simplified version - could use more sophisticated similarity metrics
        content = self.retriever.get_condition(condition_id)
        if not content:
            return []
        
        # Use related_conditions if available
        related = self.retriever.get_related_content(condition_id)
        
        results = []
        for name in related[:limit]:
            # Try to find this content
            found = self.retriever.find_content_by_name(name)
            if found:
                content_type, found_id = found
                results.append({
                    'type': content_type,
                    'id': found_id,
                    'name': name
                })
        
        return results
    
    def suggest_queries(self, partial_query: str, language: str = 'az', limit: int = 5) -> List[str]:
        """
        Auto-complete / suggest queries based on partial input.
        
        Returns:
            List of suggested complete queries
        """
        
        suggestions = []
        partial_lower = partial_query.lower()
        
        # Get all conditions and procedures
        conditions = self.retriever.list_all_conditions(language)
        procedures = self.retriever.list_all_procedures(language)
        
        all_items = conditions + procedures
        
        for item in all_items:
            name = item['name'].lower()
            if partial_lower in name or name.startswith(partial_lower):
                suggestions.append(item['name'])
        
        return suggestions[:limit]
