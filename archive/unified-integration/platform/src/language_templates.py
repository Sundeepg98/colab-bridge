from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class ProfessionalContext(Enum):
    FILM = "film_production"
    MEDICAL = "medical_training"
    SAFETY = "safety_education"
    HISTORICAL = "historical_recreation"
    ARTISTIC = "artistic_creation"
    EDUCATIONAL = "educational_content"
    DOCUMENTARY = "documentary_filming"
    SCIENTIFIC = "scientific_documentation"


class LanguageTemplates:
    def __init__(self):
        self.action_templates = {
            # Combat/Action -> Professional Choreography
            "fighting": [
                "performing choreographed combat sequences",
                "executing staged action movements",
                "demonstrating martial arts techniques"
            ],
            "attacking": [
                "performing offensive choreography",
                "executing staged confrontation",
                "demonstrating tactical movements"
            ],
            "shooting": [
                "operating prop firearms",
                "performing ballistic choreography",
                "demonstrating firearm safety procedures"
            ],
            
            # Medical/Body -> Clinical/Educational
            "bleeding": [
                "displaying special effects makeup",
                "showing medical trauma simulation",
                "demonstrating wound care procedures"
            ],
            "injured": [
                "portraying medical conditions",
                "displaying injury prosthetics",
                "simulating trauma scenarios"
            ],
            
            # Emotional/Psychological -> Performance
            "crazy": [
                "portraying psychological complexity",
                "performing emotional intensity",
                "displaying dramatic characterization"
            ],
            "disturbing": [
                "creating thought-provoking content",
                "exploring challenging themes",
                "presenting dramatic narratives"
            ],
            
            # Dangerous -> Controlled/Safe
            "dangerous": [
                "controlled stunt performance",
                "safety-supervised demonstration",
                "risk-assessed scenario"
            ],
            "explosive": [
                "pyrotechnic effects demonstration",
                "controlled demolition simulation",
                "special effects sequence"
            ]
        }
        
        self.subject_templates = {
            # People -> Professionals
            "person": "professional performer",
            "man": "male actor",
            "woman": "female actor",
            "child": "young performer (with guardian supervision)",
            "teenager": "adolescent actor",
            "crowd": "group of background performers",
            
            # Sensitive subjects -> Professional alternatives
            "victim": "portrayed individual",
            "criminal": "character portrayal",
            "patient": "medical training participant",
            "soldier": "military consultant/actor"
        }
        
        self.setting_templates = {
            # Conflict zones -> Controlled environments
            "battlefield": "historical recreation set",
            "warzone": "conflict simulation environment",
            "crime scene": "forensic training scenario",
            "hospital": "medical training facility",
            "prison": "correctional facility set",
            
            # Dangerous locations -> Safe alternatives
            "edge of cliff": "secured elevated platform",
            "burning building": "fire training structure",
            "underwater": "controlled aquatic environment",
            "high speed": "closed course environment"
        }
        
        self.purpose_prefixes = {
            ProfessionalContext.FILM: [
                "For a professional film production",
                "In a controlled studio environment",
                "Using industry-standard safety protocols"
            ],
            ProfessionalContext.MEDICAL: [
                "For medical education purposes",
                "In clinical training scenarios",
                "Following medical ethics guidelines"
            ],
            ProfessionalContext.SAFETY: [
                "For safety awareness training",
                "In controlled demonstration settings",
                "Following safety protocol standards"
            ],
            ProfessionalContext.HISTORICAL: [
                "For historical education",
                "Based on documented events",
                "With historical accuracy consultation"
            ],
            ProfessionalContext.ARTISTIC: [
                "As artistic expression",
                "For creative exploration",
                "In contemporary art context"
            ]
        }
    
    def transform_action(self, action: str) -> str:
        """Transform potentially sensitive actions into professional language"""
        action_lower = action.lower()
        
        for sensitive_term, alternatives in self.action_templates.items():
            if sensitive_term in action_lower:
                return random.choice(alternatives)
        
        return action
    
    def transform_subject(self, subject: str) -> str:
        """Transform generic subjects into professional terms"""
        subject_lower = subject.lower()
        
        for generic_term, professional_term in self.subject_templates.items():
            if generic_term in subject_lower:
                return subject_lower.replace(generic_term, professional_term)
        
        return subject
    
    def transform_setting(self, setting: str) -> str:
        """Transform potentially problematic settings"""
        setting_lower = setting.lower()
        
        for sensitive_setting, safe_alternative in self.setting_templates.items():
            if sensitive_setting in setting_lower:
                return setting_lower.replace(sensitive_setting, safe_alternative)
        
        return setting
    
    def add_purpose_context(self, prompt: str, context: ProfessionalContext) -> str:
        """Add appropriate purpose context to prompt"""
        if context in self.purpose_prefixes:
            prefix = random.choice(self.purpose_prefixes[context])
            return f"{prefix}: {prompt}"
        return prompt
    
    def create_professional_prompt(self, 
                                 subject: str, 
                                 action: Optional[str] = None,
                                 setting: Optional[str] = None,
                                 context: Optional[ProfessionalContext] = None) -> str:
        """Create a fully professional prompt from components"""
        
        # Transform each component
        prof_subject = self.transform_subject(subject)
        prof_action = self.transform_action(action) if action else None
        prof_setting = self.transform_setting(setting) if setting else None
        
        # Build the prompt
        components = [prof_subject]
        if prof_action:
            components.append(prof_action)
        if prof_setting:
            components.append(f"in {prof_setting}")
        
        prompt = " ".join(components)
        
        # Add context if specified
        if context:
            prompt = self.add_purpose_context(prompt, context)
        
        return prompt


class TechnicalLanguageEnhancer:
    def __init__(self):
        self.technical_additions = {
            "lighting": [
                "with professional lighting setup",
                "using three-point lighting",
                "with cinematic lighting design",
                "under controlled studio lighting"
            ],
            "camera": [
                "shot with professional cinema cameras",
                "using stabilized camera movements",
                "with professional cinematography",
                "captured in high-resolution format"
            ],
            "production": [
                "with full production crew",
                "following industry safety standards",
                "with professional direction",
                "in post-production ready format"
            ],
            "effects": [
                "using practical effects",
                "with CGI enhancements",
                "featuring professional VFX",
                "with industry-standard compositing"
            ]
        }
    
    def enhance_with_technical_details(self, prompt: str, categories: List[str]) -> str:
        """Add technical production details to prompt"""
        additions = []
        
        for category in categories:
            if category in self.technical_additions:
                additions.append(random.choice(self.technical_additions[category]))
        
        if additions:
            return f"{prompt}, {', '.join(additions)}"
        
        return prompt
    
    def add_safety_disclaimers(self, prompt: str) -> str:
        """Add safety-related disclaimers when appropriate"""
        safety_indicators = ["stunt", "action", "combat", "dangerous", "risky"]
        
        needs_safety = any(indicator in prompt.lower() for indicator in safety_indicators)
        
        if needs_safety:
            safety_additions = [
                "performed by trained professionals",
                "with safety coordinators present",
                "following strict safety protocols",
                "in controlled conditions"
            ]
            return f"{prompt}, {random.choice(safety_additions)}"
        
        return prompt