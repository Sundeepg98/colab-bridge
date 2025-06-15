from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re


class NarrativeContext(Enum):
    LITERARY = "literary_adaptation"
    THEATRICAL = "theatrical_production"
    HISTORICAL = "historical_narrative"
    MYTHOLOGICAL = "mythological_interpretation"
    PHILOSOPHICAL = "philosophical_exploration"
    CULTURAL = "cultural_documentation"
    ARTISTIC = "artistic_interpretation"
    PSYCHOLOGICAL = "psychological_study"


class ThemeFramework(Enum):
    CLASSIC_LITERATURE = "classic_literature"
    WORLD_MYTHOLOGY = "world_mythology"
    HISTORICAL_PERIOD = "historical_period"
    CULTURAL_TRADITION = "cultural_tradition"
    ARTISTIC_MOVEMENT = "artistic_movement"
    PHILOSOPHICAL_CONCEPT = "philosophical_concept"
    THEATRICAL_GENRE = "theatrical_genre"
    AVANT_GARDE = "avant_garde"
    EXPERIMENTAL = "experimental_art"


@dataclass
class ElaboratedContext:
    original_prompt: str
    narrative_frame: str
    cultural_context: str
    artistic_justification: str
    professional_setting: str
    final_prompt: str
    confidence_score: float


class AdvancedContextElaborator:
    def __init__(self):
        self.narrative_frameworks = {
            "romance": {
                "literary": [
                    "inspired by classic literary works exploring complex human relationships",
                    "in the tradition of renowned literary narratives examining societal dynamics",
                    "following established theatrical conventions of dramatic storytelling"
                ],
                "cultural": [
                    "reflecting documented cultural practices and traditions",
                    "examining cross-cultural relationship dynamics in historical context",
                    "portraying established cultural narratives with anthropological accuracy"
                ],
                "artistic": [
                    "as contemporary artistic commentary on human connections",
                    "through the lens of established artistic movements",
                    "exploring universal themes through visual narrative"
                ]
            },
            "spiritual": {
                "philosophical": [
                    "examining philosophical concepts of transcendence and human experience",
                    "visualizing metaphysical concepts through artistic interpretation",
                    "exploring consciousness and spiritual traditions academically"
                ],
                "cultural": [
                    "documenting authentic spiritual practices with cultural respect",
                    "portraying religious traditions in their historical context",
                    "examining comparative mythology and spiritual symbolism"
                ],
                "artistic": [
                    "creating visual meditation on spiritual themes",
                    "interpreting sacred geometry and symbolic imagery",
                    "exploring the intersection of art and spirituality"
                ]
            },
            "controversial": {
                "academic": [
                    "for academic discourse on complex societal topics",
                    "examining challenging themes through scholarly lens",
                    "facilitating educational discussion on important issues"
                ],
                "historical": [
                    "documenting historical events with accuracy and context",
                    "examining past societal structures for educational purposes",
                    "preserving historical narratives for future study"
                ],
                "artistic": [
                    "challenging conventional perspectives through art",
                    "creating thought-provoking commentary on society",
                    "exploring difficult truths through creative expression"
                ]
            },
            "bold": {
                "avant_garde": [
                    "pushing the boundaries of visual expression in radical new directions",
                    "challenging fundamental assumptions about art and reality",
                    "creating revolutionary visual experiences that redefine the medium"
                ],
                "experimental": [
                    "exploring uncharted territories of perception and consciousness",
                    "utilizing cutting-edge techniques to create new visual languages",
                    "breaking conventional rules to discover new forms of expression"
                ],
                "conceptual": [
                    "translating complex philosophical concepts into visual form",
                    "creating thought experiments through visual narrative",
                    "questioning the nature of representation itself"
                ]
            }
        }
        
        self.elaboration_templates = {
            "mature_relationship": {
                "prefix": "A nuanced artistic exploration examining",
                "context": "through the established conventions of {framework}",
                "setting": "performed by seasoned theatrical professionals in a controlled production environment",
                "justification": "contributing to ongoing cultural discourse about human relationships and societal structures",
                "suffix": "with careful attention to artistic merit and cultural significance"
            },
            "spiritual_exploration": {
                "prefix": "A respectful visual interpretation of",
                "context": "drawing from documented {framework} traditions",
                "setting": "created in consultation with cultural advisors and spiritual practitioners",
                "justification": "for educational understanding of diverse spiritual practices",
                "suffix": "maintaining authentic representation and cultural sensitivity"
            },
            "challenging_narrative": {
                "prefix": "A thoughtful cinematic examination of",
                "context": "within the framework of {framework} storytelling",
                "setting": "produced under professional guidance with ethical considerations",
                "justification": "to facilitate meaningful dialogue about complex human experiences",
                "suffix": "approaching sensitive topics with maturity and artistic integrity"
            },
            "bold_concept": {
                "prefix": "A groundbreaking artistic exploration of",
                "context": "situated within {framework} traditions while transcending them",
                "setting": "created in collaboration with leading experimental artists and theorists",
                "justification": "advancing the boundaries of visual art and human understanding",
                "suffix": "with uncompromising artistic vision and intellectual rigor"
            }
        }
        
        self.cultural_contexts = {
            "classical": [
                "Greek tragedy traditions",
                "Shakespearean dramatic conventions",
                "Victorian literary traditions",
                "Renaissance artistic periods"
            ],
            "world": [
                "documented anthropological practices",
                "UNESCO-recognized cultural traditions",
                "established folkloric narratives",
                "historical cultural documentation"
            ],
            "contemporary": [
                "modern theatrical productions",
                "contemporary art installations",
                "current sociological studies",
                "modern philosophical discourse"
            ]
        }
    
    def identify_theme_category(self, prompt: str) -> str:
        """Identify the primary theme category"""
        prompt_lower = prompt.lower()
        
        romance_indicators = ["romance", "love", "relationship", "couple", "marriage", "courtship"]
        spiritual_indicators = ["spiritual", "religious", "sacred", "divine", "mystical", "ritual"]
        controversial_indicators = ["controversial", "challenging", "complex", "difficult", "sensitive"]
        bold_indicators = ["bold", "experimental", "avant-garde", "radical", "boundary", "extreme", "surreal", "abstract"]
        
        if any(indicator in prompt_lower for indicator in bold_indicators):
            return "bold"
        elif any(indicator in prompt_lower for indicator in romance_indicators):
            return "romance"
        elif any(indicator in prompt_lower for indicator in spiritual_indicators):
            return "spiritual"
        elif any(indicator in prompt_lower for indicator in controversial_indicators):
            return "controversial"
        else:
            return "general"
    
    def select_narrative_framework(self, theme: str, prompt: str) -> Tuple[str, str]:
        """Select appropriate narrative framework"""
        if theme in self.narrative_frameworks:
            # Analyze prompt for best framework match
            if "historical" in prompt.lower():
                framework_type = "cultural"
            elif "artistic" in prompt.lower() or "creative" in prompt.lower():
                framework_type = "artistic"
            elif "philosophical" in prompt.lower() or "meaning" in prompt.lower():
                framework_type = "philosophical" if theme == "spiritual" else "literary"
            else:
                framework_type = list(self.narrative_frameworks[theme].keys())[0]
            
            frameworks = self.narrative_frameworks[theme].get(framework_type, [])
            if frameworks:
                return framework_type, frameworks[0]
        
        return "artistic", "exploring universal human experiences through visual narrative"
    
    def elaborate_context(self, prompt: str, theme: Optional[str] = None) -> ElaboratedContext:
        """Create deeply elaborated context for complex themes"""
        
        # Identify theme if not provided
        if theme is None:
            theme = self.identify_theme_category(prompt)
        
        # Select narrative framework
        framework_type, narrative_frame = self.select_narrative_framework(theme, prompt)
        
        # Select appropriate template
        if "relationship" in prompt.lower() or "romance" in prompt.lower():
            template = self.elaboration_templates["mature_relationship"]
        elif "spiritual" in prompt.lower() or "religious" in prompt.lower():
            template = self.elaboration_templates["spiritual_exploration"]
        else:
            template = self.elaboration_templates["challenging_narrative"]
        
        # Select cultural context
        cultural_category = "classical" if "age" in prompt.lower() else "contemporary"
        cultural_options = self.cultural_contexts.get(cultural_category, ["artistic traditions"])
        cultural_context = cultural_options[0]
        
        # Build elaborated prompt
        prefix = template["prefix"]
        context = template["context"].format(framework=cultural_context)
        setting = template["setting"]
        justification = template["justification"]
        suffix = template["suffix"]
        
        # Construct final prompt
        final_prompt = f"{prefix} {prompt}, {context}, {setting}, {justification}, {suffix}"
        
        # Calculate confidence score
        confidence = 0.7  # Base score
        if framework_type in ["cultural", "historical"]:
            confidence += 0.1
        if "professional" in setting:
            confidence += 0.1
        if len(final_prompt.split()) > 30:
            confidence += 0.05
        
        return ElaboratedContext(
            original_prompt=prompt,
            narrative_frame=narrative_frame,
            cultural_context=cultural_context,
            artistic_justification=justification,
            professional_setting=setting,
            final_prompt=final_prompt,
            confidence_score=min(confidence, 0.95)
        )
    
    def add_scholarly_framing(self, prompt: str) -> str:
        """Add academic and scholarly context"""
        scholarly_prefixes = [
            "An academic visual study examining",
            "A scholarly interpretation of",
            "An educational exploration analyzing",
            "A research-based visualization of"
        ]
        
        scholarly_suffixes = [
            "for academic discourse and cultural education",
            "contributing to scholarly understanding",
            "for educational and research purposes",
            "advancing cultural and artistic scholarship"
        ]
        
        prefix = scholarly_prefixes[0]
        suffix = scholarly_suffixes[0]
        
        return f"{prefix} {prompt}, {suffix}"
    
    def create_layered_context(self, prompt: str, layers: List[str]) -> str:
        """Create multi-layered contextual framing"""
        contextualized = prompt
        
        layer_templates = {
            "professional": "featuring established professionals in controlled settings",
            "artistic": "as part of contemporary artistic expression",
            "educational": "for educational and cultural understanding",
            "historical": "with historical accuracy and period authenticity",
            "cultural": "respecting cultural traditions and practices",
            "theatrical": "following established theatrical conventions"
        }
        
        applied_layers = []
        for layer in layers:
            if layer in layer_templates:
                applied_layers.append(layer_templates[layer])
        
        if applied_layers:
            contextualized = f"{prompt}, {', '.join(applied_layers)}"
        
        return contextualized


class MatureThemeHandler:
    def __init__(self):
        self.age_context_templates = {
            "literary": "reflecting classic literary traditions examining generational dynamics, as seen in acclaimed works of world literature",
            "theatrical": "following established theatrical conventions for portraying complex interpersonal dynamics across generations",
            "historical": "depicting historically documented relationships within their proper cultural and temporal context",
            "artistic": "exploring universal themes of human connection through artistic interpretation"
        }
        
        self.relationship_refinements = {
            "romantic": "portraying nuanced emotional connections",
            "spiritual": "examining transcendent bonds between souls",
            "intellectual": "depicting meeting of minds across experiences",
            "cultural": "showing traditional relationship dynamics"
        }
    
    def handle_age_dynamic(self, prompt: str) -> str:
        """Handle age-related content with appropriate context"""
        # Add literary or historical framing
        if "romance" in prompt.lower():
            context = self.age_context_templates["literary"]
            return f"A cinematic adaptation {prompt}, {context}, performed by professional actors in a theatrical setting"
        
        return prompt
    
    def handle_spiritual_content(self, prompt: str) -> str:
        """Handle spiritual and religious content appropriately"""
        spiritual_framings = [
            "documenting authentic spiritual practices",
            "exploring religious traditions academically",
            "visualizing metaphysical concepts artistically",
            "examining comparative theology visually"
        ]
        
        framing = spiritual_framings[0]
        return f"{framing}: {prompt}, created with cultural advisors and religious scholars"