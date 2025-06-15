"""
Smart Optimizer Module - Advanced Prompt Optimization Techniques
Implements pattern-based learning, contextual understanding, style transfer,
semantic enhancement, and multi-stage optimization pipeline.
"""

from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import re
import json
from collections import defaultdict, Counter
import math
import random
from datetime import datetime


class OptimizationMode(Enum):
    """Different optimization modes for various use cases"""
    ENHANCE = "enhance"          # Basic enhancement
    TRANSFORM = "transform"      # Complete transformation
    STYLIZE = "stylize"         # Style transfer
    CONTEXTUALIZE = "contextualize"  # Deep context addition
    HYBRIDIZE = "hybridize"     # Combine multiple approaches


class PatternType(Enum):
    """Types of patterns for pattern-based learning"""
    STRUCTURAL = "structural"    # Sentence structure patterns
    SEMANTIC = "semantic"        # Meaning-based patterns
    STYLISTIC = "stylistic"     # Style and tone patterns
    CONTEXTUAL = "contextual"   # Context-specific patterns
    NARRATIVE = "narrative"     # Story-telling patterns


@dataclass
class PatternMatch:
    """Represents a matched pattern in the prompt"""
    pattern_type: PatternType
    pattern: str
    match_text: str
    confidence: float
    suggestions: List[str] = field(default_factory=list)


@dataclass
class OptimizationProfile:
    """Profile for how to optimize a prompt"""
    mode: OptimizationMode
    target_style: Optional[str] = None
    emphasis_areas: List[str] = field(default_factory=list)
    preserve_elements: List[str] = field(default_factory=list)
    enhancement_level: float = 0.7  # 0-1 scale


@dataclass
class SmartOptimizationResult:
    """Result of smart optimization"""
    original_prompt: str
    optimized_prompt: str
    optimization_profile: OptimizationProfile
    patterns_detected: List[PatternMatch]
    transformations_applied: List[str]
    confidence_score: float
    semantic_score: float
    style_score: float
    alternative_versions: List[str] = field(default_factory=list)


class PatternLearner:
    """Learns from successful prompts to identify effective patterns"""
    
    def __init__(self):
        # Successful prompt patterns database
        self.successful_patterns = {
            PatternType.STRUCTURAL: [
                # Opening patterns
                r"^(Cinematic|Dramatic|Beautiful|Stunning|Breathtaking)\s+\w+",
                r"^A\s+(wide|close|medium)\s+shot\s+of",
                r"^In\s+the\s+style\s+of\s+[\w\s]+,",
                
                # Technical specification patterns
                r"(shot\s+on|filmed\s+with|captured\s+using)\s+[\w\s]+",
                r"(f\/\d+\.?\d*|ISO\s*\d+|bokeh|depth\s+of\s+field)",
                r"(4K|8K|high\s+resolution|ultra\s+detailed)",
                
                # Composition patterns
                r"(rule\s+of\s+thirds|golden\s+ratio|symmetrical\s+composition)",
                r"(foreground|midground|background)\s+elements",
            ],
            
            PatternType.SEMANTIC: [
                # Emotion and mood patterns
                r"(evoking|conveying|expressing)\s+[\w\s]+\s+(emotion|feeling|mood)",
                r"(atmosphere|ambiance)\s+of\s+[\w\s]+",
                
                # Action and movement patterns
                r"(dynamic|fluid|graceful)\s+(movement|motion|action)",
                r"(transitioning|transforming|morphing)\s+from\s+[\w\s]+\s+to",
                
                # Conceptual patterns
                r"(symbolizing|representing|embodying)\s+[\w\s]+",
                r"(metaphor|allegory)\s+for\s+[\w\s]+",
            ],
            
            PatternType.STYLISTIC: [
                # Artistic style patterns
                r"in\s+the\s+style\s+of\s+([\w\s]+\s+and\s+)*[\w\s]+",
                r"(impressionist|surrealist|minimalist|maximalist)\s+approach",
                r"(noir|vintage|retro|modern|futuristic)\s+aesthetic",
                
                # Color and lighting patterns
                r"(warm|cool|neutral)\s+color\s+palette",
                r"(golden\s+hour|blue\s+hour|magic\s+hour)\s+lighting",
                r"(dramatic|soft|harsh|natural)\s+lighting",
            ],
            
            PatternType.CONTEXTUAL: [
                # Setting and environment patterns
                r"set\s+in\s+[\w\s]+\s+(era|period|time)",
                r"(urban|rural|suburban|wilderness)\s+environment",
                
                # Cultural context patterns
                r"(inspired\s+by|drawing\s+from)\s+[\w\s]+\s+culture",
                r"(traditional|contemporary|fusion)\s+elements",
            ],
            
            PatternType.NARRATIVE: [
                # Story structure patterns
                r"(beginning|middle|climax|resolution)\s+of\s+[\w\s]+",
                r"(protagonist|character)\s+[\w\s]+\s+(journey|transformation)",
                
                # Temporal patterns
                r"(moment\s+before|during|after)\s+[\w\s]+",
                r"(flashback|flash-forward|parallel)\s+narrative",
            ]
        }
        
        # Pattern effectiveness scores (learned from hypothetical successful prompts)
        self.pattern_scores = defaultdict(lambda: 0.5)
        self._initialize_pattern_scores()
    
    def _initialize_pattern_scores(self):
        """Initialize pattern scores based on hypothetical success data"""
        # High-scoring patterns
        high_score_patterns = [
            r"^Cinematic",
            r"4K|8K",
            r"golden\s+hour",
            r"in\s+the\s+style\s+of",
            r"depth\s+of\s+field"
        ]
        for pattern in high_score_patterns:
            self.pattern_scores[pattern] = 0.85
        
        # Medium-scoring patterns
        medium_score_patterns = [
            r"atmosphere",
            r"dynamic\s+movement",
            r"symbolizing"
        ]
        for pattern in medium_score_patterns:
            self.pattern_scores[pattern] = 0.65
    
    def detect_patterns(self, prompt: str) -> List[PatternMatch]:
        """Detect successful patterns in a prompt"""
        detected_patterns = []
        
        for pattern_type, patterns in self.successful_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, prompt, re.IGNORECASE)
                for match in matches:
                    confidence = self.pattern_scores.get(pattern, 0.5)
                    detected_patterns.append(PatternMatch(
                        pattern_type=pattern_type,
                        pattern=pattern,
                        match_text=match.group(),
                        confidence=confidence,
                        suggestions=self._generate_suggestions(pattern_type, match.group())
                    ))
        
        return detected_patterns
    
    def _generate_suggestions(self, pattern_type: PatternType, matched_text: str) -> List[str]:
        """Generate enhancement suggestions based on pattern type"""
        suggestions = []
        
        if pattern_type == PatternType.STRUCTURAL:
            suggestions.extend([
                f"Consider adding technical details after '{matched_text}'",
                f"Enhance with composition elements",
                f"Add camera movement description"
            ])
        elif pattern_type == PatternType.SEMANTIC:
            suggestions.extend([
                f"Deepen the emotional context",
                f"Add sensory details",
                f"Expand on the conceptual meaning"
            ])
        elif pattern_type == PatternType.STYLISTIC:
            suggestions.extend([
                f"Specify color grading details",
                f"Add texture and material descriptions",
                f"Include atmospheric effects"
            ])
        
        return suggestions[:2]  # Return top 2 suggestions


class ContextualUnderstandingEngine:
    """NLP-based contextual understanding for prompts"""
    
    def __init__(self):
        # Semantic field mappings
        self.semantic_fields = {
            "emotion": {
                "joy": ["happiness", "delight", "euphoria", "bliss", "elation"],
                "sadness": ["melancholy", "sorrow", "grief", "despair", "longing"],
                "fear": ["anxiety", "dread", "terror", "apprehension", "unease"],
                "anger": ["rage", "fury", "irritation", "frustration", "wrath"],
                "love": ["affection", "passion", "devotion", "tenderness", "romance"]
            },
            "atmosphere": {
                "mysterious": ["enigmatic", "cryptic", "puzzling", "mystical", "arcane"],
                "peaceful": ["serene", "tranquil", "calm", "placid", "harmonious"],
                "tense": ["suspenseful", "anxious", "strained", "fraught", "edgy"],
                "energetic": ["dynamic", "vibrant", "lively", "vigorous", "animated"]
            },
            "visual": {
                "bright": ["luminous", "radiant", "brilliant", "gleaming", "dazzling"],
                "dark": ["shadowy", "dim", "murky", "gloomy", "tenebrous"],
                "colorful": ["vibrant", "chromatic", "prismatic", "kaleidoscopic", "vivid"],
                "monochrome": ["grayscale", "achromatic", "noir", "sepia", "desaturated"]
            }
        }
        
        # Context expansion templates
        self.context_templates = {
            "temporal": "During {time_context}, {main_content}, creating a sense of {temporal_mood}",
            "spatial": "In {location_context}, {main_content}, with {spatial_details} defining the space",
            "emotional": "{main_content}, evoking feelings of {emotion} through {emotional_cues}",
            "cultural": "{main_content}, incorporating {cultural_elements} that reflect {cultural_context}"
        }
    
    def analyze_context(self, prompt: str) -> Dict[str, Any]:
        """Analyze the contextual elements of a prompt"""
        analysis = {
            "primary_theme": self._identify_primary_theme(prompt),
            "semantic_fields": self._extract_semantic_fields(prompt),
            "missing_contexts": self._identify_missing_contexts(prompt),
            "context_suggestions": self._generate_context_suggestions(prompt)
        }
        return analysis
    
    def _identify_primary_theme(self, prompt: str) -> str:
        """Identify the main theme of the prompt"""
        theme_keywords = {
            "narrative": ["story", "character", "plot", "scene", "moment"],
            "descriptive": ["landscape", "portrait", "still life", "architecture"],
            "action": ["movement", "action", "dynamic", "motion", "activity"],
            "conceptual": ["abstract", "symbolic", "metaphorical", "representing"],
            "documentary": ["real", "authentic", "actual", "documentary", "factual"]
        }
        
        prompt_lower = prompt.lower()
        theme_scores = {}
        
        for theme, keywords in theme_keywords.items():
            score = sum(1 for keyword in keywords if keyword in prompt_lower)
            theme_scores[theme] = score
        
        return max(theme_scores, key=theme_scores.get) if max(theme_scores.values()) > 0 else "general"
    
    def _extract_semantic_fields(self, prompt: str) -> Dict[str, List[str]]:
        """Extract semantic fields present in the prompt"""
        found_fields = defaultdict(list)
        prompt_lower = prompt.lower()
        
        for field_category, field_groups in self.semantic_fields.items():
            for field_name, related_words in field_groups.items():
                for word in related_words:
                    if word in prompt_lower:
                        found_fields[field_category].append(field_name)
                        break
        
        return dict(found_fields)
    
    def _identify_missing_contexts(self, prompt: str) -> List[str]:
        """Identify what contextual elements are missing"""
        missing = []
        prompt_lower = prompt.lower()
        
        # Check for temporal context
        temporal_indicators = ["morning", "evening", "night", "dawn", "dusk", "season", "year", "era"]
        if not any(indicator in prompt_lower for indicator in temporal_indicators):
            missing.append("temporal")
        
        # Check for spatial context
        spatial_indicators = ["location", "place", "setting", "environment", "space", "room", "outdoor", "indoor"]
        if not any(indicator in prompt_lower for indicator in spatial_indicators):
            missing.append("spatial")
        
        # Check for emotional context
        if "emotion" not in self._extract_semantic_fields(prompt):
            missing.append("emotional")
        
        # Check for technical details
        technical_indicators = ["shot", "angle", "lens", "camera", "composition", "framing"]
        if not any(indicator in prompt_lower for indicator in technical_indicators):
            missing.append("technical")
        
        return missing
    
    def _generate_context_suggestions(self, prompt: str) -> List[str]:
        """Generate suggestions for adding context"""
        suggestions = []
        missing_contexts = self._identify_missing_contexts(prompt)
        
        if "temporal" in missing_contexts:
            suggestions.append("Add time of day or era for temporal context")
        if "spatial" in missing_contexts:
            suggestions.append("Specify the location or environment")
        if "emotional" in missing_contexts:
            suggestions.append("Include emotional tone or mood")
        if "technical" in missing_contexts:
            suggestions.append("Add camera angle or shot composition details")
        
        return suggestions
    
    def enhance_with_context(self, prompt: str, context_type: str) -> str:
        """Enhance prompt with specific context type"""
        if context_type == "temporal":
            time_contexts = ["golden hour", "blue hour", "midnight", "dawn", "twilight"]
            temporal_moods = ["nostalgic", "timeless", "ephemeral", "eternal"]
            return self.context_templates["temporal"].format(
                time_context=random.choice(time_contexts),
                main_content=prompt,
                temporal_mood=random.choice(temporal_moods)
            )
        elif context_type == "emotional":
            emotions = ["wonder", "serenity", "anticipation", "contemplation"]
            emotional_cues = ["subtle lighting", "body language", "atmospheric elements"]
            return self.context_templates["emotional"].format(
                main_content=prompt,
                emotion=random.choice(emotions),
                emotional_cues=random.choice(emotional_cues)
            )
        
        return prompt


class StyleTransferEngine:
    """Handles style transfer capabilities for prompts"""
    
    def __init__(self):
        # Style signatures - characteristics of different styles
        self.style_signatures = {
            "cinematic": {
                "keywords": ["cinematic", "filmic", "dramatic lighting", "depth of field"],
                "structure": "wide establishing shot → medium shot → close-up progression",
                "technical": ["anamorphic lens", "color grading", "film grain"],
                "mood": ["epic", "dramatic", "atmospheric"]
            },
            "documentary": {
                "keywords": ["authentic", "real", "unscripted", "observational"],
                "structure": "objective observation with contextual details",
                "technical": ["handheld camera", "natural lighting", "minimal post-processing"],
                "mood": ["truthful", "raw", "immediate"]
            },
            "artistic": {
                "keywords": ["artistic", "creative", "expressive", "interpretive"],
                "structure": "concept-driven with symbolic elements",
                "technical": ["experimental techniques", "creative framing", "artistic filters"],
                "mood": ["evocative", "thought-provoking", "aesthetic"]
            },
            "minimalist": {
                "keywords": ["minimal", "simple", "clean", "uncluttered"],
                "structure": "single focus with negative space",
                "technical": ["simple composition", "limited color palette", "clean lines"],
                "mood": ["calm", "focused", "zen-like"]
            },
            "maximalist": {
                "keywords": ["elaborate", "detailed", "ornate", "complex"],
                "structure": "layered elements with rich details",
                "technical": ["complex composition", "vibrant colors", "multiple focal points"],
                "mood": ["overwhelming", "rich", "abundant"]
            }
        }
        
        # Style transfer rules
        self.transfer_rules = {
            "preserve_subject": True,
            "adapt_descriptors": True,
            "add_style_markers": True,
            "maintain_coherence": True
        }
    
    def detect_current_style(self, prompt: str) -> Optional[str]:
        """Detect the current style of a prompt"""
        prompt_lower = prompt.lower()
        style_scores = {}
        
        for style, signature in self.style_signatures.items():
            score = 0
            for keyword in signature["keywords"]:
                if keyword in prompt_lower:
                    score += 1
            style_scores[style] = score
        
        if max(style_scores.values()) > 0:
            return max(style_scores, key=style_scores.get)
        return None
    
    def transfer_style(self, prompt: str, target_style: str) -> str:
        """Transfer prompt to a target style"""
        if target_style not in self.style_signatures:
            return prompt
        
        # Extract core elements
        core_elements = self._extract_core_elements(prompt)
        
        # Apply target style
        styled_prompt = self._apply_style_signature(core_elements, target_style)
        
        return styled_prompt
    
    def _extract_core_elements(self, prompt: str) -> Dict[str, str]:
        """Extract the core elements from a prompt"""
        elements = {
            "subject": "",
            "action": "",
            "setting": "",
            "descriptors": []
        }
        
        # Simple extraction logic (in real implementation, would use more sophisticated NLP)
        # Extract subject (typically noun phrases)
        subject_match = re.search(r"(?:a|an|the)\s+([^,\.]+?)(?:\s+(?:in|at|on|doing|performing))", prompt, re.IGNORECASE)
        if subject_match:
            elements["subject"] = subject_match.group(1)
        
        # Extract action (typically verb phrases)
        action_match = re.search(r"(?:is|are|was|were)?\s*(\w+ing)\s+", prompt)
        if action_match:
            elements["action"] = action_match.group(1)
        
        # Extract setting
        setting_match = re.search(r"(?:in|at|on)\s+(?:a|an|the)?\s*([^,\.]+)", prompt)
        if setting_match:
            elements["setting"] = setting_match.group(1)
        
        # Extract descriptors (adjectives)
        descriptors = re.findall(r"\b(beautiful|stunning|dramatic|peaceful|vibrant|mysterious)\b", prompt, re.IGNORECASE)
        elements["descriptors"] = descriptors
        
        return elements
    
    def _apply_style_signature(self, elements: Dict[str, str], style: str) -> str:
        """Apply style signature to core elements"""
        signature = self.style_signatures[style]
        
        # Build styled prompt
        styled_parts = []
        
        # Add style-specific opening
        if style == "cinematic":
            styled_parts.append("Cinematic shot:")
        elif style == "documentary":
            styled_parts.append("Documentary footage capturing")
        elif style == "artistic":
            styled_parts.append("Artistic interpretation of")
        elif style == "minimalist":
            styled_parts.append("Minimalist composition featuring")
        elif style == "maximalist":
            styled_parts.append("Elaborate and detailed scene of")
        
        # Add subject with style-appropriate descriptors
        if elements["subject"]:
            style_descriptors = signature["mood"]
            descriptor = random.choice(style_descriptors)
            styled_parts.append(f"{descriptor} {elements['subject']}")
        
        # Add action if present
        if elements["action"]:
            styled_parts.append(elements["action"])
        
        # Add setting with style elements
        if elements["setting"]:
            styled_parts.append(f"in {elements['setting']}")
        
        # Add style-specific technical details
        technical_detail = random.choice(signature["technical"])
        styled_parts.append(f"with {technical_detail}")
        
        return " ".join(styled_parts)


class SemanticEnhancer:
    """Enhances prompts through semantic analysis and expansion"""
    
    def __init__(self):
        # Semantic relationships
        self.semantic_relations = {
            "synonyms": self._load_synonyms(),
            "hypernyms": self._load_hypernyms(),  # More general terms
            "hyponyms": self._load_hyponyms(),    # More specific terms
            "meronyms": self._load_meronyms()     # Part-whole relationships
        }
        
        # Enhancement strategies
        self.enhancement_strategies = {
            "specificity": self._enhance_specificity,
            "vividness": self._enhance_vividness,
            "coherence": self._enhance_coherence,
            "depth": self._enhance_depth
        }
    
    def _load_synonyms(self) -> Dict[str, List[str]]:
        """Load synonym database"""
        return {
            "beautiful": ["stunning", "gorgeous", "breathtaking", "magnificent", "exquisite"],
            "walk": ["stroll", "stride", "saunter", "march", "wander"],
            "big": ["large", "enormous", "massive", "colossal", "immense"],
            "small": ["tiny", "miniature", "petite", "minute", "diminutive"],
            "fast": ["quick", "rapid", "swift", "speedy", "brisk"],
            "slow": ["gradual", "leisurely", "unhurried", "languid", "deliberate"]
        }
    
    def _load_hypernyms(self) -> Dict[str, List[str]]:
        """Load hypernym database (more general terms)"""
        return {
            "rose": ["flower", "plant", "organism"],
            "car": ["vehicle", "transport", "machine"],
            "dog": ["canine", "animal", "mammal"],
            "chair": ["furniture", "seat", "object"]
        }
    
    def _load_hyponyms(self) -> Dict[str, List[str]]:
        """Load hyponym database (more specific terms)"""
        return {
            "flower": ["rose", "tulip", "daisy", "lily", "orchid"],
            "vehicle": ["car", "truck", "motorcycle", "bicycle", "bus"],
            "color": ["crimson", "azure", "emerald", "amber", "violet"],
            "movement": ["glide", "leap", "creep", "dash", "float"]
        }
    
    def _load_meronyms(self) -> Dict[str, List[str]]:
        """Load meronym database (part-whole relationships)"""
        return {
            "tree": ["branches", "leaves", "trunk", "roots", "bark"],
            "face": ["eyes", "nose", "mouth", "cheeks", "forehead"],
            "building": ["walls", "windows", "doors", "roof", "foundation"],
            "story": ["plot", "characters", "setting", "conflict", "resolution"]
        }
    
    def enhance_semantically(self, prompt: str, strategy: str = "all") -> str:
        """Enhance prompt using semantic techniques"""
        if strategy == "all":
            enhanced = prompt
            for strat_name, strat_func in self.enhancement_strategies.items():
                enhanced = strat_func(enhanced)
            return enhanced
        elif strategy in self.enhancement_strategies:
            return self.enhancement_strategies[strategy](prompt)
        else:
            return prompt
    
    def _enhance_specificity(self, prompt: str) -> str:
        """Make vague terms more specific"""
        words = prompt.split()
        enhanced_words = []
        
        for word in words:
            word_lower = word.lower().strip('.,!?')
            if word_lower in self.semantic_relations["hyponyms"]:
                # Replace with more specific term
                specific_options = self.semantic_relations["hyponyms"][word_lower]
                specific_word = random.choice(specific_options)
                enhanced_words.append(word.replace(word_lower, specific_word))
            else:
                enhanced_words.append(word)
        
        return " ".join(enhanced_words)
    
    def _enhance_vividness(self, prompt: str) -> str:
        """Add vivid descriptors and sensory details"""
        # Sensory descriptor templates
        sensory_additions = {
            "visual": ["bathed in {light}", "with {texture} surfaces", "displaying {color} hues"],
            "auditory": ["accompanied by {sound}", "echoing with {noise}", "filled with {audio}"],
            "tactile": ["featuring {texture} textures", "with {feel} surfaces"],
            "atmospheric": ["creating an atmosphere of {mood}", "evoking {feeling}"]
        }
        
        # Add a random sensory detail
        sense_type = random.choice(list(sensory_additions.keys()))
        template = random.choice(sensory_additions[sense_type])
        
        # Fill in the template
        if "{light}" in template:
            light_options = ["golden", "silvery", "dappled", "ethereal", "dramatic"]
            addition = template.format(light=random.choice(light_options))
        elif "{texture}" in template:
            texture_options = ["smooth", "rough", "glossy", "matte", "weathered"]
            addition = template.format(texture=random.choice(texture_options))
        elif "{color}" in template:
            color_options = ["vibrant", "muted", "contrasting", "harmonious", "shifting"]
            addition = template.format(color=random.choice(color_options))
        elif "{mood}" in template:
            mood_options = ["mystery", "tranquility", "excitement", "nostalgia", "wonder"]
            addition = template.format(mood=random.choice(mood_options))
        else:
            addition = ""
        
        return f"{prompt}, {addition}" if addition else prompt
    
    def _enhance_coherence(self, prompt: str) -> str:
        """Improve logical flow and coherence"""
        # Add transitional phrases and logical connectors
        if "and" in prompt:
            prompt = prompt.replace(" and ", " while simultaneously ")
        
        # Add causal relationships
        if "," in prompt:
            parts = prompt.split(",")
            if len(parts) == 2:
                prompt = f"{parts[0]}, creating {parts[1].strip()}"
        
        return prompt
    
    def _enhance_depth(self, prompt: str) -> str:
        """Add layers of meaning and complexity"""
        # Add symbolic or metaphorical layer
        depth_additions = [
            ", symbolizing the passage of time",
            ", representing the duality of existence",
            ", embodying the tension between order and chaos",
            ", capturing the essence of transformation",
            ", illustrating the beauty of impermanence"
        ]
        
        # Only add if prompt doesn't already have symbolic language
        if not any(word in prompt.lower() for word in ["symbolizing", "representing", "embodying", "metaphor"]):
            return prompt + random.choice(depth_additions)
        
        return prompt


class MultiStageOptimizer:
    """Orchestrates multi-stage optimization pipeline"""
    
    def __init__(self):
        self.pattern_learner = PatternLearner()
        self.context_engine = ContextualUnderstandingEngine()
        self.style_engine = StyleTransferEngine()
        self.semantic_enhancer = SemanticEnhancer()
        
        # Pipeline stages
        self.stages = [
            ("analysis", self._stage_analysis),
            ("pattern_enhancement", self._stage_pattern_enhancement),
            ("contextual_enrichment", self._stage_contextual_enrichment),
            ("semantic_enhancement", self._stage_semantic_enhancement),
            ("style_application", self._stage_style_application),
            ("final_polish", self._stage_final_polish)
        ]
    
    def _stage_analysis(self, prompt: str, profile: OptimizationProfile, metadata: Dict) -> Tuple[str, Dict]:
        """Stage 1: Analyze the prompt"""
        patterns = self.pattern_learner.detect_patterns(prompt)
        context_analysis = self.context_engine.analyze_context(prompt)
        current_style = self.style_engine.detect_current_style(prompt)
        
        metadata = {
            "patterns_found": len(patterns),
            "primary_theme": context_analysis["primary_theme"],
            "current_style": current_style,
            "missing_contexts": context_analysis["missing_contexts"]
        }
        
        return prompt, metadata
    
    def _stage_pattern_enhancement(self, prompt: str, profile: OptimizationProfile, metadata: Dict) -> Tuple[str, Dict]:
        """Stage 2: Enhance based on successful patterns"""
        patterns = self.pattern_learner.detect_patterns(prompt)
        
        # Add missing high-value patterns
        if not any(p.pattern_type == PatternType.STRUCTURAL for p in patterns):
            prompt = f"Cinematic {prompt}"
        
        if not any(p.pattern_type == PatternType.STYLISTIC for p in patterns):
            if "lighting" not in prompt.lower():
                prompt += ", with dramatic lighting"
        
        metadata["patterns_added"] = 2
        return prompt, metadata
    
    def _stage_contextual_enrichment(self, prompt: str, profile: OptimizationProfile, metadata: Dict) -> Tuple[str, Dict]:
        """Stage 3: Add contextual depth"""
        missing_contexts = metadata.get("missing_contexts", [])
        
        for context_type in missing_contexts[:2]:  # Add up to 2 missing contexts
            prompt = self.context_engine.enhance_with_context(prompt, context_type)
        
        metadata["contexts_added"] = min(2, len(missing_contexts))
        return prompt, metadata
    
    def _stage_semantic_enhancement(self, prompt: str, profile: OptimizationProfile, metadata: Dict) -> Tuple[str, Dict]:
        """Stage 4: Semantic enhancement"""
        if profile.enhancement_level > 0.5:
            prompt = self.semantic_enhancer.enhance_semantically(prompt, "vividness")
        
        if profile.enhancement_level > 0.7:
            prompt = self.semantic_enhancer.enhance_semantically(prompt, "depth")
        
        metadata["semantic_enhancements"] = 2 if profile.enhancement_level > 0.7 else 1
        return prompt, metadata
    
    def _stage_style_application(self, prompt: str, profile: OptimizationProfile, metadata: Dict) -> Tuple[str, Dict]:
        """Stage 5: Apply style transfer if requested"""
        if profile.target_style and profile.mode in [OptimizationMode.STYLIZE, OptimizationMode.TRANSFORM]:
            prompt = self.style_engine.transfer_style(prompt, profile.target_style)
            metadata["style_applied"] = profile.target_style
        
        return prompt, metadata
    
    def _stage_final_polish(self, prompt: str, profile: OptimizationProfile, metadata: Dict) -> Tuple[str, Dict]:
        """Stage 6: Final polish and coherence check"""
        # Remove redundancies
        prompt = self._remove_redundancies(prompt)
        
        # Ensure proper grammar and flow
        prompt = self._ensure_grammar(prompt)
        
        # Add final technical details if missing
        if "resolution" not in prompt.lower() and "4k" not in prompt.lower():
            prompt += ", ultra high definition"
        
        metadata["final_polish_applied"] = True
        return prompt, metadata
    
    def _remove_redundancies(self, prompt: str) -> str:
        """Remove redundant words and phrases"""
        # Simple redundancy removal
        words = prompt.split()
        seen = set()
        result = []
        
        for word in words:
            word_lower = word.lower().strip('.,!?')
            if word_lower not in seen or word_lower in ['the', 'a', 'an', 'in', 'on', 'at', 'with']:
                result.append(word)
                seen.add(word_lower)
        
        return " ".join(result)
    
    def _ensure_grammar(self, prompt: str) -> str:
        """Ensure proper grammar and punctuation"""
        # Capitalize first letter
        if prompt:
            prompt = prompt[0].upper() + prompt[1:]
        
        # Ensure ends with period
        if prompt and not prompt[-1] in '.!?':
            prompt += '.'
        
        # Fix common grammar issues
        prompt = prompt.replace(" ,", ",")
        prompt = prompt.replace("  ", " ")
        
        return prompt


class SmartOptimizer:
    """Main class for smart prompt optimization"""
    
    def __init__(self):
        self.multi_stage_optimizer = MultiStageOptimizer()
        self.pattern_learner = PatternLearner()
        self.context_engine = ContextualUnderstandingEngine()
        self.style_engine = StyleTransferEngine()
        self.semantic_enhancer = SemanticEnhancer()
        
        # Optimization history for learning
        self.optimization_history = []
    
    def optimize(self, prompt: str, profile: Optional[OptimizationProfile] = None) -> SmartOptimizationResult:
        """Main optimization method"""
        if profile is None:
            profile = self._auto_detect_profile(prompt)
        
        # Detect initial patterns
        initial_patterns = self.pattern_learner.detect_patterns(prompt)
        
        # Run through multi-stage pipeline
        optimized_prompt = prompt
        metadata = {}
        transformations = []
        
        for stage_name, stage_func in self.multi_stage_optimizer.stages:
            optimized_prompt, stage_metadata = stage_func(optimized_prompt, profile, metadata)
            metadata.update(stage_metadata)
            transformations.append(f"Applied {stage_name}")
        
        # Generate alternative versions
        alternatives = self._generate_alternatives(prompt, profile)
        
        # Calculate scores
        confidence_score = self._calculate_confidence(optimized_prompt, initial_patterns)
        semantic_score = self._calculate_semantic_score(prompt, optimized_prompt)
        style_score = self._calculate_style_score(optimized_prompt, profile)
        
        # Create result
        result = SmartOptimizationResult(
            original_prompt=prompt,
            optimized_prompt=optimized_prompt,
            optimization_profile=profile,
            patterns_detected=initial_patterns,
            transformations_applied=transformations,
            confidence_score=confidence_score,
            semantic_score=semantic_score,
            style_score=style_score,
            alternative_versions=alternatives
        )
        
        # Store in history for learning
        self.optimization_history.append(result)
        
        return result
    
    def _auto_detect_profile(self, prompt: str) -> OptimizationProfile:
        """Automatically detect the best optimization profile"""
        context_analysis = self.context_engine.analyze_context(prompt)
        current_style = self.style_engine.detect_current_style(prompt)
        
        # Determine optimization mode
        if len(prompt.split()) < 10:
            mode = OptimizationMode.ENHANCE
        elif "style of" in prompt.lower():
            mode = OptimizationMode.STYLIZE
        elif len(context_analysis["missing_contexts"]) > 2:
            mode = OptimizationMode.CONTEXTUALIZE
        else:
            mode = OptimizationMode.TRANSFORM
        
        # Determine target style
        target_style = None
        if mode == OptimizationMode.STYLIZE and not current_style:
            target_style = "cinematic"  # Default to cinematic
        
        # Determine emphasis areas based on analysis
        emphasis_areas = []
        if "technical" in context_analysis["missing_contexts"]:
            emphasis_areas.append("technical_details")
        if not context_analysis["semantic_fields"]:
            emphasis_areas.append("emotional_depth")
        
        return OptimizationProfile(
            mode=mode,
            target_style=target_style,
            emphasis_areas=emphasis_areas,
            enhancement_level=0.7
        )
    
    def _generate_alternatives(self, original_prompt: str, profile: OptimizationProfile) -> List[str]:
        """Generate alternative optimized versions"""
        alternatives = []
        
        # Style variation
        if profile.target_style != "minimalist":
            minimalist_profile = OptimizationProfile(
                mode=OptimizationMode.STYLIZE,
                target_style="minimalist",
                enhancement_level=0.5
            )
            minimalist_version = self.multi_stage_optimizer._stage_style_application(
                original_prompt, minimalist_profile, {}
            )[0]
            alternatives.append(minimalist_version)
        
        # Semantic variation
        semantic_variation = self.semantic_enhancer.enhance_semantically(
            original_prompt, "specificity"
        )
        alternatives.append(semantic_variation)
        
        # Context variation
        if "temporal" not in self.context_engine._identify_missing_contexts(original_prompt):
            temporal_version = self.context_engine.enhance_with_context(
                original_prompt, "temporal"
            )
            alternatives.append(temporal_version)
        
        return alternatives[:2]  # Return top 2 alternatives
    
    def _calculate_confidence(self, optimized_prompt: str, initial_patterns: List[PatternMatch]) -> float:
        """Calculate confidence score for optimization"""
        # Base confidence
        confidence = 0.5
        
        # Boost for successful patterns
        pattern_score = sum(p.confidence for p in initial_patterns) / max(len(initial_patterns), 1)
        confidence += pattern_score * 0.2
        
        # Boost for prompt length (optimal range)
        word_count = len(optimized_prompt.split())
        if 20 <= word_count <= 50:
            confidence += 0.2
        elif 10 <= word_count <= 60:
            confidence += 0.1
        
        # Boost for technical details
        technical_terms = ["4k", "8k", "composition", "lighting", "shot", "angle"]
        technical_count = sum(1 for term in technical_terms if term in optimized_prompt.lower())
        confidence += min(technical_count * 0.05, 0.2)
        
        return min(confidence, 0.95)
    
    def _calculate_semantic_score(self, original: str, optimized: str) -> float:
        """Calculate semantic preservation and enhancement score"""
        # Simple word overlap metric
        original_words = set(original.lower().split())
        optimized_words = set(optimized.lower().split())
        
        # Preservation score
        preservation = len(original_words.intersection(optimized_words)) / max(len(original_words), 1)
        
        # Enhancement score (new meaningful words added)
        enhancement = len(optimized_words - original_words) / max(len(optimized_words), 1)
        
        # Balance preservation and enhancement
        semantic_score = (preservation * 0.6) + (enhancement * 0.4)
        
        return min(semantic_score, 1.0)
    
    def _calculate_style_score(self, optimized_prompt: str, profile: OptimizationProfile) -> float:
        """Calculate how well the style was applied"""
        if not profile.target_style:
            return 0.8  # Default score if no specific style requested
        
        detected_style = self.style_engine.detect_current_style(optimized_prompt)
        
        if detected_style == profile.target_style:
            return 0.95
        elif detected_style is not None:
            return 0.7
        else:
            return 0.5
    
    def get_optimization_insights(self) -> Dict[str, Any]:
        """Get insights from optimization history"""
        if not self.optimization_history:
            return {"message": "No optimization history available"}
        
        insights = {
            "total_optimizations": len(self.optimization_history),
            "average_confidence": sum(r.confidence_score for r in self.optimization_history) / len(self.optimization_history),
            "most_common_patterns": self._get_most_common_patterns(),
            "optimization_trends": self._get_optimization_trends()
        }
        
        return insights
    
    def _get_most_common_patterns(self) -> List[Tuple[str, int]]:
        """Get most commonly detected patterns"""
        pattern_counter = Counter()
        
        for result in self.optimization_history:
            for pattern in result.patterns_detected:
                pattern_counter[pattern.pattern_type.value] += 1
        
        return pattern_counter.most_common(3)
    
    def _get_optimization_trends(self) -> Dict[str, float]:
        """Analyze optimization trends"""
        if len(self.optimization_history) < 2:
            return {}
        
        recent_results = self.optimization_history[-10:]
        older_results = self.optimization_history[:-10] if len(self.optimization_history) > 10 else []
        
        if not older_results:
            return {
                "trend": "insufficient_data",
                "recent_avg_confidence": sum(r.confidence_score for r in recent_results) / len(recent_results)
            }
        
        recent_avg = sum(r.confidence_score for r in recent_results) / len(recent_results)
        older_avg = sum(r.confidence_score for r in older_results) / len(older_results)
        
        return {
            "trend": "improving" if recent_avg > older_avg else "stable",
            "recent_avg_confidence": recent_avg,
            "improvement": recent_avg - older_avg
        }


# Utility function for easy integration
def create_smart_optimizer() -> SmartOptimizer:
    """Factory function to create a smart optimizer instance"""
    return SmartOptimizer()


# Example usage and testing
if __name__ == "__main__":
    # Create optimizer
    optimizer = create_smart_optimizer()
    
    # Test prompts
    test_prompts = [
        "A person walking in a forest",
        "Beautiful sunset over the ocean with waves",
        "Abstract representation of time passing"
    ]
    
    for prompt in test_prompts:
        print(f"\nOriginal: {prompt}")
        result = optimizer.optimize(prompt)
        print(f"Optimized: {result.optimized_prompt}")
        print(f"Confidence: {result.confidence_score:.2f}")
        print(f"Semantic Score: {result.semantic_score:.2f}")
        print(f"Style Score: {result.style_score:.2f}")
        print(f"Transformations: {', '.join(result.transformations_applied)}")
        
        if result.alternative_versions:
            print("Alternatives:")
            for i, alt in enumerate(result.alternative_versions, 1):
                print(f"  {i}. {alt}")