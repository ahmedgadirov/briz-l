import yaml
from typing import Dict, List, Any, Optional
from .content_retriever import MedicalContentRetriever


class ProgressiveDisclosure:
    """
    Manages progressive disclosure of medical information.
    Starts simple, gets more detailed based on user engagement.
    """
    
    LAYER_SEQUENCE = [
        'simple_explanation',
        'symptoms',
        'medical_details',
        'treatment',
        'risks',
        'recovery',
        'cost',
        'faqs'
    ]
    
    def __init__(self):
        self.retriever = MedicalContentRetriever()
    
    def get_next_layer(self,
                       content_type: str,
                       content_id: str,
                       current_depth: int,
                       language: str = 'az') -> Dict[str, Any]:
        """
        Get next layer of information based on current depth.
        
        Args:
            content_type: 'condition' or 'procedure'
            content_id: e.g., 'cataract'
            current_depth: 0 (start), 1, 2, etc.
            language: 'az', 'ru', 'en'
        
        Returns:
            {
                'layer_name': str,
                'content': str/dict,
                'has_more': bool,
                'next_prompt': str
            }
        """
        
        if current_depth >= len(self.LAYER_SEQUENCE):
            return {
                'layer_name': 'complete',
                'content': None,
                'has_more': False,
                'next_prompt': ''
            }
        
        layer_name = self.LAYER_SEQUENCE[current_depth]
        layer_content = self.retriever.get_layer(
            content_type,
            content_id,
            layer_name,
            language
        )
        
        has_more = (current_depth + 1) < len(self.LAYER_SEQUENCE)
        
        # Generate appropriate "next" prompt
        next_prompts = {
            'az': {
                'simple_explanation': "Əlamətləri haqqında məlumat istəyirsiniz?",
                'symptoms': "Müalicə variantları haqqında bilmək istərdiniz?",
                'medical_details': "Müalicə seçimləri haqqında ətraflı məlumat?",
                'treatment': "Risklər və komplikasiyalar haqqında?",
                'risks': "Sağalma prosesi haqqında?",
                'recovery': "Qiymət məlumatı?",
                'cost': "Tez-tez verilən suallar?",
                'faqs': ""
            },
            'ru': {
                'simple_explanation': "Хотите узнать о симптомах?",
                'symptoms': "Хотите узнать о вариантах лечения?",
                'medical_details': "Подробная информация о лечении?",
                'treatment': "О рисках и осложнениях?",
                'risks': "О процессе восстановления?",
                'recovery': "Информация о стоимости?",
                'cost': "Часто задаваемые вопросы?",
                'faqs': ""
            },
            'en': {
                'simple_explanation': "Would you like to know about symptoms?",
                'symptoms': "Would you like to know about treatment options?",
                'medical_details': "Detailed treatment information?",
                'treatment': "About risks and complications?",
                'risks': "About recovery process?",
                'recovery': "Pricing information?",
                'cost': "Frequently asked questions?",
                'faqs': ""
            }
        }
        
        next_prompt = next_prompts.get(language, {}).get(layer_name, '') if has_more else ''
        
        return {
            'layer_name': layer_name,
            'content': layer_content,
            'has_more': has_more,
            'next_prompt': next_prompt
        }
    
    def format_for_chat(self,
                        layer_data: Dict[str, Any],
                        language: str = 'az') -> str:
        """
        Format layer content for chat display.
        """
        
        content = layer_data['content']
        layer_name = layer_data['layer_name']
        
        # Format based on content type
        if isinstance(content, str):
            message = content
        elif isinstance(content, dict):
            message = self._format_dict_content(content, layer_name, language)
        elif isinstance(content, list):
            message = self._format_list_content(content, layer_name, language)
        else:
            message = str(content)
        
        # Add "more info" prompt if available
        if layer_data['has_more'] and layer_data['next_prompt']:
            message += f"\n\n💬 {layer_data['next_prompt']}"
        
        return message
    
    def _format_dict_content(self, content: Dict, layer_name: str, language: str) -> str:
        """Format dictionary content."""
        
        if layer_name == 'symptoms':
            # Format symptoms by stage
            output = "**ƏLAMƏTLƏR:**\n\n"
            for stage, symptoms in content.items():
                if isinstance(symptoms, dict) and language in symptoms:
                    stage_title = stage.replace('_', ' ').title()
                    output += f"**{stage_title}:**\n"
                    for symptom in symptoms[language]:
                        output += f"  • {symptom}\n"
                    output += "\n"
            return output
        
        elif layer_name == 'treatment':
            # Format treatment options
            output = "**MÜALİCƏ:**\n\n"
            if 'surgical' in content:
                surg = content['surgical']
                output += f"**{surg.get('name', {}).get(language, '')}**\n\n"
                output += surg.get('description', {}).get(language, '')
                output += f"\n\n✅ Uğur nisbəti: {surg.get('success_rate', 'N/A')}\n"
            return output
        
        elif layer_name == 'risks':
            # Format risks
            output = "**RİSKLƏR VƏ KOMPLİKASİYALAR:**\n\n"
            
            if 'common_side_effects' in content:
                output += "**Adi yan təsirlər:**\n"
                for effect in content['common_side_effects']:
                    symptom = effect.get('symptom', {}).get(language, '')
                    freq = effect.get('frequency', '')
                    duration = effect.get('duration', '')
                    output += f"• {symptom} ({freq}, {duration})\n"
                output += "\n"
            
            if 'rare_complications' in content:
                output += "**Nadir komplikasiyalar:**\n"
                for comp in content['rare_complications']:
                    complication = comp.get('complication', {}).get(language, '')
                    freq = comp.get('frequency', '')
                    output += f"• {complication} ({freq})\n"
                output += "\n"
            
            return output
        
        elif layer_name == 'cost':
            # Format cost information
            output = "**QİYMƏT:**\n\n"
            
            if 'range' in content:
                range_data = content['range']
                if 'note' in range_data and language in range_data['note']:
                    output += f"{range_data['note'][language]}\n\n"
                
                if 'estimate' in range_data:
                    output += "**Təqribi qiymət:**\n"
                    for key, value in range_data['estimate'].items():
                        label = key.replace('_', ' ').title()
                        output += f"• {label}: {value}\n"
                    output += "\n"
            
            return output
        
        else:
            # Generic formatting
            return yaml.dump(content, allow_unicode=True, default_flow_style=False)
    
    def _format_list_content(self, content: List, layer_name: str, language: str) -> str:
        """Format list content."""
        
        if layer_name == 'faqs':
            output = "**TEZ-TEZ VERİLƏN SUALLAR:**\n\n"
            for i, faq in enumerate(content, 1):
                q = faq.get('question', {}).get(language, '')
                a = faq.get('answer', {}).get(language, '')
                output += f"**{i}. {q}**\n{a}\n\n"
            return output
        
        else:
            return "\n".join(f"• {item}" for item in content)
    
    def get_summary(self, content_type: str, content_id: str, language: str = 'az') -> str:
        """
        Get a brief summary (simple explanation) of the content.
        Useful for initial responses.
        """
        layer_data = self.get_next_layer(content_type, content_id, 0, language)
        return self.format_for_chat(layer_data, language)
