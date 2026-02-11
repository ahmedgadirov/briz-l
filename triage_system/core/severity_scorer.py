import yaml
from typing import Dict, List, Tuple, Any
import re
import os

class SeverityScorer:
    """
    Scores symptom severity based on keyword matching and natural language patterns.
    """
    
    def __init__(self, config_path: str = "triage_system/data/symptom_matrix.yml"):
        # Handle relative path if needed, assuming run from project root
        if not os.path.isabs(config_path):
            config_path = os.path.abspath(config_path)
            
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.symptoms = self.config.get('symptoms', {})
    
    def score_severity(self, 
                       user_message: str, 
                       language: str = 'az') -> Tuple[float, str, Dict]:
        """
        Calculate severity score from user message.
        
        Args:
            user_message: Patient's description
            language: Language code (az, ru, en)
            
        Returns:
            (severity_score, matched_symptom, symptom_details)
        """
        
        user_message = user_message.lower() if user_message else ""
        best_match = None
        best_score = 0
        best_symptom_name = None
        
        # Check each symptom in matrix
        for symptom_name, symptom_data in self.symptoms.items():
            keywords = symptom_data.get('keywords', {}).get(language, [])
            
            # Count keyword matches
            matches = sum(1 for keyword in keywords if keyword.lower() in user_message)
            
            if matches > best_score:
                best_score = matches
                best_match = symptom_data
                best_symptom_name = symptom_name
        
        if best_match:
            severity = best_match.get('severity', 5)
            return float(severity), best_symptom_name, best_match
        
        # No specific match - analyze pain descriptors
        severity = self._analyze_pain_descriptors(user_message, language)
        return float(severity), "unspecified", {}
    
    def _analyze_pain_descriptors(self, message: str, language: str) -> float:
        """
        Analyze pain intensity from descriptive words.
        """
        
        if language == 'az':
            severe_words = ['dözülməz', 'çox pis', 'ölürəm', 'dəhşətli', 'ciddi', 'güclü']
            moderate_words = ['ağrı', 'yanır', 'narahat', 'pis', 'incidir']
            mild_words = ['yüngül', 'az', 'xeyli', 'arada']
        elif language == 'ru':
            severe_words = ['невыносимо', 'очень сильно', 'ужасно', 'кошмар', 'сильная']
            moderate_words = ['боль', 'болит', 'жжет', 'беспокоит']
            mild_words = ['легкая', 'немного', 'слегка']
        else:  # English
            severe_words = ['unbearable', 'excruciating', 'terrible', 'worst', 'severe']
            moderate_words = ['painful', 'hurts', 'burning', 'bothering']
            mild_words = ['mild', 'slight', 'little']
        
        if any(word in message for word in severe_words):
            return 8.0
        elif any(word in message for word in moderate_words):
            return 6.0
        elif any(word in message for word in mild_words):
            return 3.0
        
        return 5.0  # Default moderate
