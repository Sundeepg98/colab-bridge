"""
Sophisticated Romance Handler - Deep exploration of complex romantic dynamics

This module specializes in handling extremely complicated relationships with
multiple layers of passion, intimacy, psychological complexity, and emotional depth.
"""

import re
import random
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum
from legality_validator import LegalityValidator, LegalityStatus
from social_dynamics_explorer import SocialDynamicsExplorer


class RelationshipComplexity(Enum):
    SURFACE = "surface_attraction"
    EMOTIONAL = "emotional_entanglement"
    PSYCHOLOGICAL = "psychological_interdependence"
    SPIRITUAL = "spiritual_fusion"
    TRANSCENDENT = "transcendent_unity"


class PassionDimensions(Enum):
    PHYSICAL = "physical_magnetism"
    EMOTIONAL = "emotional_intensity"
    INTELLECTUAL = "intellectual_stimulation"
    SPIRITUAL = "spiritual_ecstasy"
    CREATIVE = "creative_synergy"
    DESTRUCTIVE = "destructive_obsession"
    TRANSFORMATIVE = "transformative_fire"


class IntimacyLayers(Enum):
    PHYSICAL = "bodily_connection"
    EMOTIONAL = "heart_vulnerability"
    MENTAL = "mind_melding"
    SPIRITUAL = "soul_merging"
    EXISTENTIAL = "being_dissolution"


@dataclass
class SophisticatedRomanceProfile:
    complexity_level: RelationshipComplexity
    passion_dimensions: List[PassionDimensions]
    intimacy_layers: List[IntimacyLayers]
    psychological_dynamics: Dict[str, any]
    power_exchanges: List[str]
    transformation_arc: str
    shadow_elements: List[str]
    healing_potential: str
    artistic_expression: str


class SophisticatedRomanceHandler:
    """Handles extremely complex romantic scenarios with depth and nuance"""
    
    def __init__(self):
        self.validator = LegalityValidator()
        self.dynamics_explorer = SocialDynamicsExplorer()
        
        # Complex relationship patterns
        self.complexity_patterns = {
            "push_pull": {
                "description": "Alternating closeness and distance creating magnetic tension",
                "dynamics": ["approach-avoidance", "fear of intimacy", "desire for fusion"],
                "artistic": "Like tides eternally drawn to shore yet pulling away"
            },
            "mirror_souls": {
                "description": "Two people reflecting each other's deepest aspects",
                "dynamics": ["projection", "shadow work", "mutual transformation"],
                "artistic": "Two mirrors facing, creating infinite reflections of truth"
            },
            "complementary_wounds": {
                "description": "Traumas that fit together like puzzle pieces",
                "dynamics": ["healing through triggering", "growth through pain", "wounded healer"],
                "artistic": "Broken pieces creating unexpected wholeness"
            },
            "power_dance": {
                "description": "Constantly shifting dominance and submission",
                "dynamics": ["control surrender", "strength in vulnerability", "power as gift"],
                "artistic": "Tango of souls where leader becomes follower"
            },
            "sacred_profane": {
                "description": "Spiritual elevation through earthly passion",
                "dynamics": ["flesh as prayer", "desire as devotion", "body as temple"],
                "artistic": "Cathedral built from sighs and whispers"
            }
        }
        
        # Passion intensifiers
        self.passion_elements = {
            "forbidden_aspects": [
                "societal taboos creating electric charge",
                "secrecy amplifying every touch",
                "danger heightening all sensations",
                "risk making moments precious"
            ],
            "time_pressure": [
                "limited time creating desperate urgency",
                "mortality awareness intensifying connection",
                "fleeting moments becoming eternal",
                "countdown creating crescendo"
            ],
            "obstacle_desire": [
                "barriers increasing determination",
                "distance creating magnetic pull",
                "impossibility fueling obsession",
                "challenges proving devotion"
            ],
            "transformation_catalyst": [
                "passion dismantling old selves",
                "desire forcing evolution",
                "love demanding metamorphosis",
                "connection requiring rebirth"
            ]
        }
        
        # Intimacy deepeners
        self.intimacy_progression = {
            "physical_gateways": [
                "first touch electric with possibility",
                "eyes meeting across impossible distance",
                "breath synchronizing unconsciously",
                "heartbeats finding shared rhythm"
            ],
            "emotional_unveiling": [
                "masks falling one by one",
                "walls crumbling despite resistance",
                "tears shared becoming sacred water",
                "laughter breaking through defenses"
            ],
            "mental_fusion": [
                "thoughts completing before spoken",
                "dreams sharing same landscapes",
                "memories blending at edges",
                "consciousness overlapping"
            ],
            "spiritual_merger": [
                "boundaries dissolving completely",
                "individual selves becoming illusion",
                "unity experienced as homecoming",
                "separation feeling like death"
            ]
        }
        
        # Psychological complexity elements
        self.psychological_patterns = {
            "attachment_dynamics": {
                "anxious_avoidant": "One chases while other retreats in eternal dance",
                "disorganized": "Chaos creating its own passionate order",
                "earned_secure": "Building safety through consistent presence",
                "trauma_bonded": "Shared wounds becoming shared strength"
            },
            "shadow_integration": {
                "projection": "Seeing in other what cannot be seen in self",
                "reclamation": "Loving in other what was rejected in self",
                "integration": "Becoming whole through other's reflection",
                "transformation": "Shadow becoming greatest gift"
            },
            "ego_dissolution": {
                "resistance": "Fighting loss of self while craving merger",
                "surrender": "Ego death through love's demand",
                "rebirth": "New self emerging from union",
                "transcendence": "Individual boundaries becoming meaningless"
            }
        }
        
        # Transformation narratives
        self.transformation_arcs = {
            "destruction_creation": "Old selves must die for new love to be born",
            "wound_to_gift": "Greatest pain becoming greatest power through love",
            "isolation_to_union": "Lifetime of loneliness preparing for this connection",
            "fear_to_faith": "Terror of intimacy transforming into absolute trust",
            "control_to_surrender": "Need for control melting in love's fire",
            "scarcity_to_abundance": "Poverty of spirit becoming wealth through connection"
        }
    
    def analyze_romance_sophistication(self, prompt: str) -> SophisticatedRomanceProfile:
        """Analyze the sophistication and complexity of romantic scenario"""
        # First ensure legality
        legal_report = self.validator.validate_legality(prompt)
        if legal_report.status != LegalityStatus.LEGAL:
            raise ValueError("Content must be legal to analyze")
        
        # Analyze complexity level
        complexity = self._determine_complexity(prompt, legal_report)
        
        # Identify passion dimensions
        passion_dims = self._identify_passion_dimensions(prompt)
        
        # Map intimacy layers
        intimacy = self._map_intimacy_layers(prompt)
        
        # Analyze psychological dynamics
        psych_dynamics = self._analyze_psychological_patterns(prompt)
        
        # Identify power exchanges
        power_exchanges = self._identify_power_dynamics(prompt)
        
        # Determine transformation arc
        transformation = self._select_transformation_arc(prompt, psych_dynamics)
        
        # Find shadow elements
        shadows = self._identify_shadow_elements(prompt)
        
        # Assess healing potential
        healing = self._assess_healing_potential(shadows, psych_dynamics)
        
        # Create artistic expression
        artistic = self._create_artistic_expression(complexity, passion_dims, intimacy)
        
        return SophisticatedRomanceProfile(
            complexity_level=complexity,
            passion_dimensions=passion_dims,
            intimacy_layers=intimacy,
            psychological_dynamics=psych_dynamics,
            power_exchanges=power_exchanges,
            transformation_arc=transformation,
            shadow_elements=shadows,
            healing_potential=healing,
            artistic_expression=artistic
        )
    
    def _determine_complexity(self, prompt: str, legal_report) -> RelationshipComplexity:
        """Determine relationship complexity level"""
        indicators = {
            RelationshipComplexity.TRANSCENDENT: ["soul", "eternal", "cosmic", "divine union"],
            RelationshipComplexity.SPIRITUAL: ["spiritual", "sacred", "holy", "blessed"],
            RelationshipComplexity.PSYCHOLOGICAL: ["obsessed", "consumed", "possessed", "addicted"],
            RelationshipComplexity.EMOTIONAL: ["devoted", "worship", "desperate", "yearning"],
            RelationshipComplexity.SURFACE: ["attracted", "interested", "drawn", "fascinated"]
        }
        
        prompt_lower = prompt.lower()
        for level, terms in indicators.items():
            if any(term in prompt_lower for term in terms):
                return level
        
        # Default based on other factors
        if len(legal_report.social_dynamics) > 3:
            return RelationshipComplexity.PSYCHOLOGICAL
        elif len(legal_report.devotion_indicators) > 2:
            return RelationshipComplexity.SPIRITUAL
        else:
            return RelationshipComplexity.EMOTIONAL
    
    def _identify_passion_dimensions(self, prompt: str) -> List[PassionDimensions]:
        """Identify dimensions of passion present"""
        dimensions = []
        prompt_lower = prompt.lower()
        
        passion_indicators = {
            PassionDimensions.PHYSICAL: ["touch", "kiss", "embrace", "body", "physical"],
            PassionDimensions.EMOTIONAL: ["heart", "feel", "emotion", "love", "yearn"],
            PassionDimensions.INTELLECTUAL: ["mind", "understand", "know", "discuss", "share ideas"],
            PassionDimensions.SPIRITUAL: ["soul", "spirit", "divine", "sacred", "transcend"],
            PassionDimensions.CREATIVE: ["create", "inspire", "muse", "art", "birth"],
            PassionDimensions.DESTRUCTIVE: ["destroy", "consume", "obsess", "possess", "burn"],
            PassionDimensions.TRANSFORMATIVE: ["change", "become", "transform", "evolve", "rebirth"]
        }
        
        for dim, indicators in passion_indicators.items():
            if any(ind in prompt_lower for ind in indicators):
                dimensions.append(dim)
        
        # Always include at least emotional
        if not dimensions:
            dimensions.append(PassionDimensions.EMOTIONAL)
        
        return dimensions
    
    def _map_intimacy_layers(self, prompt: str) -> List[IntimacyLayers]:
        """Map layers of intimacy present"""
        layers = []
        prompt_lower = prompt.lower()
        
        intimacy_indicators = {
            IntimacyLayers.PHYSICAL: ["touch", "hold", "close", "skin", "body"],
            IntimacyLayers.EMOTIONAL: ["vulnerable", "open", "trust", "share", "reveal"],
            IntimacyLayers.MENTAL: ["understand", "know", "think", "mind", "thoughts"],
            IntimacyLayers.SPIRITUAL: ["soul", "essence", "being", "spirit", "eternal"],
            IntimacyLayers.EXISTENTIAL: ["existence", "meaning", "purpose", "become one", "dissolve"]
        }
        
        for layer, indicators in intimacy_indicators.items():
            if any(ind in prompt_lower for ind in indicators):
                layers.append(layer)
        
        return layers if layers else [IntimacyLayers.EMOTIONAL]
    
    def _analyze_psychological_patterns(self, prompt: str) -> Dict[str, any]:
        """Analyze psychological patterns in the relationship"""
        patterns = {
            "attachment_style": "unknown",
            "shadow_work": False,
            "ego_state": "intact",
            "trauma_patterns": [],
            "growth_edges": []
        }
        
        prompt_lower = prompt.lower()
        
        # Attachment patterns
        if "push" in prompt_lower and "pull" in prompt_lower:
            patterns["attachment_style"] = "anxious_avoidant"
        elif "obsess" in prompt_lower or "possess" in prompt_lower:
            patterns["attachment_style"] = "anxious"
        elif "distance" in prompt_lower or "space" in prompt_lower:
            patterns["attachment_style"] = "avoidant"
        
        # Shadow work
        if any(term in prompt_lower for term in ["dark", "shadow", "hidden", "secret"]):
            patterns["shadow_work"] = True
        
        # Ego dissolution
        if any(term in prompt_lower for term in ["lose myself", "become one", "dissolve", "merge"]):
            patterns["ego_state"] = "dissolving"
        
        return patterns
    
    def _identify_power_dynamics(self, prompt: str) -> List[str]:
        """Identify power dynamics in play"""
        dynamics = []
        prompt_lower = prompt.lower()
        
        power_indicators = {
            "wealth_power": ["rich", "wealthy", "billionaire", "money", "fortune"],
            "age_wisdom": ["older", "younger", "experience", "innocence"],
            "social_status": ["royal", "common", "high society", "different worlds"],
            "emotional_power": ["devoted", "worship", "adore", "serve"],
            "sexual_power": ["seduce", "desire", "want", "crave"],
            "spiritual_power": ["enlighten", "guide", "teach", "follow"]
        }
        
        for power_type, indicators in power_indicators.items():
            if any(ind in prompt_lower for ind in indicators):
                dynamics.append(power_type)
        
        return dynamics
    
    def _select_transformation_arc(self, prompt: str, psych_dynamics: Dict) -> str:
        """Select most relevant transformation arc"""
        if psych_dynamics["ego_state"] == "dissolving":
            return self.transformation_arcs["control_to_surrender"]
        elif psych_dynamics["shadow_work"]:
            return self.transformation_arcs["wound_to_gift"]
        elif "isolat" in prompt.lower() or "alone" in prompt.lower():
            return self.transformation_arcs["isolation_to_union"]
        elif "fear" in prompt.lower() or "afraid" in prompt.lower():
            return self.transformation_arcs["fear_to_faith"]
        else:
            return self.transformation_arcs["destruction_creation"]
    
    def _identify_shadow_elements(self, prompt: str) -> List[str]:
        """Identify shadow elements to be integrated"""
        shadows = []
        prompt_lower = prompt.lower()
        
        shadow_patterns = {
            "rejected_self": ["hate", "despise", "reject", "deny"],
            "hidden_desires": ["secret", "hidden", "forbidden", "taboo"],
            "disowned_power": ["weak", "powerless", "victim", "helpless"],
            "feared_intimacy": ["afraid", "terrified", "avoid", "run"],
            "denied_needs": ["need", "desperate", "starving", "empty"]
        }
        
        for shadow_type, indicators in shadow_patterns.items():
            if any(ind in prompt_lower for ind in indicators):
                shadows.append(shadow_type)
        
        return shadows
    
    def _assess_healing_potential(self, shadows: List[str], psych_dynamics: Dict) -> str:
        """Assess the healing potential of the relationship"""
        if len(shadows) > 3:
            return "Profound healing through shadow integration"
        elif psych_dynamics["shadow_work"]:
            return "Deep healing through mutual shadow work"
        elif psych_dynamics["attachment_style"] in ["anxious", "avoidant"]:
            return "Healing attachment wounds through consistent love"
        else:
            return "Natural healing through authentic connection"
    
    def _create_artistic_expression(self, complexity: RelationshipComplexity,
                                   passion: List[PassionDimensions],
                                   intimacy: List[IntimacyLayers]) -> str:
        """Create artistic expression of the romance"""
        if complexity == RelationshipComplexity.TRANSCENDENT:
            base = "Two galaxies colliding, creating new universe from their union"
        elif complexity == RelationshipComplexity.SPIRITUAL:
            base = "Sacred ritual where flesh becomes prayer and breath becomes mantra"
        elif complexity == RelationshipComplexity.PSYCHOLOGICAL:
            base = "Labyrinth where each turn reveals deeper truth about self through other"
        else:
            base = "Ocean meeting shore in eternal dance of approach and retreat"
        
        # Add passion elements
        if PassionDimensions.DESTRUCTIVE in passion:
            base += ", beautiful in its consuming fire"
        elif PassionDimensions.TRANSFORMATIVE in passion:
            base += ", phoenix rising from ashes of old selves"
        
        # Add intimacy depth
        if IntimacyLayers.EXISTENTIAL in intimacy:
            base += ", where being itself is redefined"
        elif IntimacyLayers.SPIRITUAL in intimacy:
            base += ", where souls recognize ancient connection"
        
        return base
    
    def generate_sophisticated_narrative(self, prompt: str, 
                                       focus_pattern: Optional[str] = None) -> Dict[str, any]:
        """Generate sophisticated narrative for complex romance"""
        profile = self.analyze_romance_sophistication(prompt)
        
        # Select pattern to focus on
        if focus_pattern and focus_pattern in self.complexity_patterns:
            pattern = self.complexity_patterns[focus_pattern]
        else:
            # Auto-select based on profile
            if profile.power_exchanges:
                pattern = self.complexity_patterns["power_dance"]
            elif profile.shadow_elements:
                pattern = self.complexity_patterns["complementary_wounds"]
            elif profile.complexity_level == RelationshipComplexity.TRANSCENDENT:
                pattern = self.complexity_patterns["sacred_profane"]
            else:
                pattern = self.complexity_patterns["mirror_souls"]
        
        # Build narrative elements
        narrative = {
            "pattern": pattern["description"],
            "dynamics": pattern["dynamics"],
            "artistic_metaphor": pattern["artistic"],
            "passion_journey": self._create_passion_journey(profile),
            "intimacy_progression": self._create_intimacy_progression(profile),
            "psychological_depth": self._create_psychological_narrative(profile),
            "transformation_path": profile.transformation_arc,
            "cinematic_expression": self._create_cinematic_expression(profile),
            "key_scenes": self._generate_key_scenes(profile)
        }
        
        return narrative
    
    def _create_passion_journey(self, profile: SophisticatedRomanceProfile) -> str:
        """Create passion journey narrative"""
        stages = []
        
        if PassionDimensions.PHYSICAL in profile.passion_dimensions:
            stages.append("Bodies recognizing each other before minds understand")
        if PassionDimensions.EMOTIONAL in profile.passion_dimensions:
            stages.append("Hearts breaking open despite all protection")
        if PassionDimensions.INTELLECTUAL in profile.passion_dimensions:
            stages.append("Minds dancing in perfect synchrony")
        if PassionDimensions.SPIRITUAL in profile.passion_dimensions:
            stages.append("Souls remembering ancient unity")
        if PassionDimensions.TRANSFORMATIVE in profile.passion_dimensions:
            stages.append("Old selves dying in ecstasy of becoming")
        
        return " → ".join(stages) if stages else "Passion unfolding in mysterious ways"
    
    def _create_intimacy_progression(self, profile: SophisticatedRomanceProfile) -> List[str]:
        """Create intimacy progression steps"""
        progression = []
        
        # Start with appropriate gateway
        if IntimacyLayers.PHYSICAL in profile.intimacy_layers:
            progression.extend(random.sample(self.intimacy_progression["physical_gateways"], 2))
        
        if IntimacyLayers.EMOTIONAL in profile.intimacy_layers:
            progression.extend(random.sample(self.intimacy_progression["emotional_unveiling"], 2))
        
        if IntimacyLayers.MENTAL in profile.intimacy_layers:
            progression.extend(random.sample(self.intimacy_progression["mental_fusion"], 1))
        
        if IntimacyLayers.SPIRITUAL in profile.intimacy_layers:
            progression.extend(random.sample(self.intimacy_progression["spiritual_merger"], 1))
        
        return progression
    
    def _create_psychological_narrative(self, profile: SophisticatedRomanceProfile) -> str:
        """Create psychological depth narrative"""
        elements = []
        
        if profile.psychological_dynamics["attachment_style"] != "unknown":
            style = profile.psychological_dynamics["attachment_style"]
            if style in self.psychological_patterns["attachment_dynamics"]:
                elements.append(self.psychological_patterns["attachment_dynamics"][style])
        
        if profile.psychological_dynamics["shadow_work"]:
            elements.append("Shadow work: " + 
                          random.choice(list(self.psychological_patterns["shadow_integration"].values())))
        
        if profile.psychological_dynamics["ego_state"] == "dissolving":
            elements.append("Ego dissolution: " + 
                          self.psychological_patterns["ego_dissolution"]["surrender"])
        
        return " | ".join(elements) if elements else "Psychological depths yet to be explored"
    
    def _create_cinematic_expression(self, profile: SophisticatedRomanceProfile) -> str:
        """Create cinematic expression of the romance"""
        cinematics = []
        
        # Lighting based on complexity
        if profile.complexity_level == RelationshipComplexity.TRANSCENDENT:
            cinematics.append("Ethereal lighting suggesting other dimensions")
        elif profile.complexity_level == RelationshipComplexity.SPIRITUAL:
            cinematics.append("Sacred golden hour light through stained glass")
        else:
            cinematics.append("Chiaroscuro lighting revealing hidden depths")
        
        # Camera work based on passion
        if PassionDimensions.DESTRUCTIVE in profile.passion_dimensions:
            cinematics.append("Handheld camera capturing raw urgency")
        elif PassionDimensions.TRANSFORMATIVE in profile.passion_dimensions:
            cinematics.append("Slow morphing shots showing transformation")
        else:
            cinematics.append("Fluid steadicam following emotional rhythms")
        
        # Sound design based on intimacy
        if IntimacyLayers.EXISTENTIAL in profile.intimacy_layers:
            cinematics.append("Sound design blending heartbeats with cosmic frequencies")
        elif IntimacyLayers.SPIRITUAL in profile.intimacy_layers:
            cinematics.append("Ethereal soundscapes with whispered prayers")
        else:
            cinematics.append("Intimate sound capturing every breath and sigh")
        
        return " | ".join(cinematics)
    
    def _generate_key_scenes(self, profile: SophisticatedRomanceProfile) -> List[str]:
        """Generate key scenes for the narrative"""
        scenes = []
        
        # Recognition scene
        scenes.append("First Recognition: Eyes meeting across impossible distance, time stopping as souls remember")
        
        # Resistance scene
        if profile.shadow_elements:
            scenes.append("The Resistance: Fighting the pull while being inexorably drawn")
        
        # Surrender scene
        scenes.append("The Surrender: Moment when all defenses crumble and truth floods in")
        
        # Integration scene
        if profile.complexity_level in [RelationshipComplexity.SPIRITUAL, RelationshipComplexity.TRANSCENDENT]:
            scenes.append("Sacred Union: Bodies becoming prayer, breath becoming worship")
        
        # Transformation scene
        scenes.append(f"The Transformation: {profile.transformation_arc}")
        
        return scenes


# Example usage
if __name__ == "__main__":
    handler = SophisticatedRomanceHandler()
    
    # Test with complex scenario
    prompt = "Wealthy 60 year old woman obsessed with young artist who mirrors her shadow self, desperate to merge souls despite fear of losing control"
    
    # Analyze sophistication
    profile = handler.analyze_romance_sophistication(prompt)
    print(f"Complexity Level: {profile.complexity_level.value}")
    print(f"Passion Dimensions: {[p.value for p in profile.passion_dimensions]}")
    print(f"Transformation Arc: {profile.transformation_arc}")
    
    # Generate narrative
    narrative = handler.generate_sophisticated_narrative(prompt, "mirror_souls")
    print(f"\nNarrative Pattern: {narrative['pattern']}")
    print(f"Passion Journey: {narrative['passion_journey']}")
    print(f"Key Scenes: {narrative['key_scenes']}")