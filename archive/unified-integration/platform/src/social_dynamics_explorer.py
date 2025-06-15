"""
Social Dynamics Explorer - Deep exploration of controversial but legal relationships

This module explores the profound dynamics of extreme wealth, devotion, trust,
insecurity, and spiritual connections that make challenging relationships possible.
"""

import re
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
from legality_validator import LegalityValidator, SocialDynamics, LegalityStatus, LegalityReport


@dataclass
class DynamicExploration:
    theme: str
    depth_level: int  # 1-5, how deep to explore
    perspectives: List[str]
    emotional_journey: str
    spiritual_dimension: str
    trust_evolution: str
    alternative_framings: List[str]


class ProfoundThemes(Enum):
    WEALTH_AS_BURDEN = "extreme wealth as emotional isolation"
    DEVOTION_AS_FREEDOM = "complete surrender as ultimate liberation"
    INSECURITY_AS_LOVE = "jealousy as expression of deep need"
    TRUST_AS_TRANSFORMATION = "earning trust through spiritual trials"
    AGE_AS_WISDOM = "temporal distance as spiritual proximity"
    POWER_AS_VULNERABILITY = "strength revealing deepest weaknesses"
    SACRIFICE_AS_PROOF = "giving everything to prove worthiness"


class SocialDynamicsExplorer:
    """Explores deep, controversial dynamics in legal adult relationships"""
    
    def __init__(self):
        self.validator = LegalityValidator()
        
        # Extreme wealth dynamics
        self.wealth_explorations = {
            "isolation": [
                "billions creating walls only true love can breach",
                "golden cages where both captor and captive seek freedom",
                "material abundance highlighting spiritual poverty"
            ],
            "power_reversal": [
                "wealth becoming weakness in face of genuine emotion",
                "riches meaningless without someone to trust",
                "fortune as test of authentic connection"
            ],
            "transactional_transcendence": [
                "beginning as arrangement, evolving to devotion",
                "sugar turning to soul connection",
                "patron becoming worshipper of their muse"
            ]
        }
        
        # Profound devotion dynamics
        self.devotion_explorations = {
            "worship_dynamics": [
                "seeing divinity in flawed humanity",
                "devotion so complete it transcends self",
                "loving someone more than one's own existence"
            ],
            "spiritual_submission": [
                "surrender as path to enlightenment",
                "losing self to find greater unity",
                "devotion as form of prayer"
            ],
            "obsessive_transformation": [
                "obsession refined into pure dedication",
                "consuming need becoming sustaining force",
                "possession evolving to protection"
            ]
        }
        
        # Trust and insecurity explorations
        self.trust_explorations = {
            "insecurity_depths": [
                "jealousy revealing depth of need",
                "possessiveness as fear of abandonment",
                "suspicious nature hiding profound vulnerability"
            ],
            "trust_building": [
                "earning faith through consistent devotion",
                "proving love through increasing trials",
                "trust growing from deepest doubts"
            ],
            "vulnerability_power": [
                "strength found in admitting weakness",
                "control surrendered to gain connection",
                "walls crumbling to reveal authentic self"
            ]
        }
        
        # Age gap spiritual dimensions
        self.age_gap_spirituality = {
            "temporal_transcendence": [
                "souls meeting across decades of experience",
                "youth rejuvenating ancient hearts",
                "wisdom guiding passionate innocence"
            ],
            "generational_healing": [
                "past wounds healed by fresh perspective",
                "future fears calmed by seasoned presence",
                "time itself bending to accommodate love"
            ],
            "mortality_awareness": [
                "limited time intensifying every moment",
                "age difference highlighting life's preciousness",
                "sunset years illuminated by dawn's light"
            ]
        }
        
        # Alternative narrative frameworks
        self.narrative_alternatives = {
            "mythological": [
                "modern Pygmalion with reversed dynamics",
                "Persephone choosing her Hades",
                "mortal earning love of deity"
            ],
            "spiritual_journey": [
                "kundalini awakening through romantic union",
                "tantra of souls across social divides",
                "enlightenment through earthly passion"
            ],
            "psychological_depth": [
                "anima/animus integration through other",
                "shadow work through relationship mirrors",
                "individuation through intimate challenge"
            ]
        }
    
    def explore_dynamics(self, prompt: str, depth: int = 3) -> DynamicExploration:
        """Deeply explore the social dynamics in the prompt"""
        # First validate legality
        legal_report = self.validator.validate_legality(prompt)
        
        if legal_report.status != LegalityStatus.LEGAL:
            return DynamicExploration(
                theme="Cannot explore - legal concerns",
                depth_level=0,
                perspectives=[],
                emotional_journey="",
                spiritual_dimension="",
                trust_evolution="",
                alternative_framings=[]
            )
        
        # Identify primary theme
        primary_theme = self._identify_primary_theme(legal_report.social_dynamics)
        
        # Generate explorations based on dynamics found
        perspectives = self._generate_perspectives(legal_report, depth)
        emotional_journey = self._map_emotional_journey(legal_report)
        spiritual_dimension = self._explore_spiritual_dimension(legal_report)
        trust_evolution = self._trace_trust_evolution(legal_report)
        alternatives = self._create_alternative_framings(prompt, legal_report, depth)
        
        return DynamicExploration(
            theme=primary_theme,
            depth_level=depth,
            perspectives=perspectives,
            emotional_journey=emotional_journey,
            spiritual_dimension=spiritual_dimension,
            trust_evolution=trust_evolution,
            alternative_framings=alternatives
        )
    
    def _identify_primary_theme(self, dynamics: List[SocialDynamics]) -> str:
        """Identify the primary profound theme"""
        if SocialDynamics.EXTREME_WEALTH in dynamics:
            return ProfoundThemes.WEALTH_AS_BURDEN.value
        elif SocialDynamics.PROFOUND_DEVOTION in dynamics:
            return ProfoundThemes.DEVOTION_AS_FREEDOM.value
        elif SocialDynamics.TRUST_INSECURITY in dynamics:
            return ProfoundThemes.INSECURITY_AS_LOVE.value
        elif SocialDynamics.AGE_GAP in dynamics:
            return ProfoundThemes.AGE_AS_WISDOM.value
        else:
            return "Complex human connection transcending categories"
    
    def _generate_perspectives(self, report: LegalityReport, depth: int) -> List[str]:
        """Generate multiple perspectives on the dynamics"""
        perspectives = []
        
        # Wealth perspectives
        if report.wealth_indicators:
            if depth >= 1:
                perspectives.append(f"Surface: {random.choice(self.wealth_explorations['isolation'])}")
            if depth >= 3:
                perspectives.append(f"Deeper: {random.choice(self.wealth_explorations['power_reversal'])}")
            if depth >= 5:
                perspectives.append(f"Profound: {random.choice(self.wealth_explorations['transactional_transcendence'])}")
        
        # Devotion perspectives
        if report.devotion_indicators:
            if depth >= 1:
                perspectives.append(f"Surface: {random.choice(self.devotion_explorations['worship_dynamics'])}")
            if depth >= 3:
                perspectives.append(f"Deeper: {random.choice(self.devotion_explorations['spiritual_submission'])}")
            if depth >= 5:
                perspectives.append(f"Profound: {random.choice(self.devotion_explorations['obsessive_transformation'])}")
        
        return perspectives
    
    def _map_emotional_journey(self, report: LegalityReport) -> str:
        """Map the emotional journey of the relationship"""
        journey_elements = []
        
        if report.wealth_indicators:
            journey_elements.append("from material transaction to spiritual transformation")
        
        if report.devotion_indicators:
            journey_elements.append("from admiration to complete spiritual merger")
        
        if report.trust_complexity["has_insecurity"]:
            journey_elements.append("from suspicion to absolute faith")
        
        if SocialDynamics.AGE_GAP in report.social_dynamics:
            journey_elements.append("from temporal distance to eternal connection")
        
        return " → ".join(journey_elements) if journey_elements else "a journey of discovery"
    
    def _explore_spiritual_dimension(self, report: LegalityReport) -> str:
        """Explore the spiritual aspects of the dynamics"""
        spiritual_elements = []
        
        if report.spiritual_elements:
            spiritual_elements.extend([
                f"Recognition of divine in the beloved",
                f"Sacred union transcending physical form",
                f"Spiritual awakening through earthly love"
            ])
        
        if SocialDynamics.PROFOUND_DEVOTION in report.social_dynamics:
            spiritual_elements.append("Devotion as path to enlightenment")
        
        if SocialDynamics.AGE_GAP in report.social_dynamics:
            spiritual_elements.append("Time as illusion in face of soul connection")
        
        return random.choice(spiritual_elements) if spiritual_elements else "Spiritual growth through relationship"
    
    def _trace_trust_evolution(self, report: LegalityReport) -> str:
        """Trace how trust evolves in the relationship"""
        if report.trust_complexity["has_insecurity"]:
            stages = [
                "Initial suspicion born from past wounds",
                "Small gestures building fragile bridges",
                "Tests of loyalty deepening connection",
                "Vulnerability replacing defensive walls",
                "Complete trust achieved through trials"
            ]
            return " → ".join(stages[:3])  # Show first 3 stages
        elif report.trust_complexity["has_trust_themes"]:
            return "Trust deepening through consistent devotion and spiritual alignment"
        else:
            return "Natural trust flowing from authentic connection"
    
    def _create_alternative_framings(self, prompt: str, report: LegalityReport, depth: int) -> List[str]:
        """Create alternative ways to frame the narrative"""
        alternatives = []
        
        # Always include a mythological framing
        alternatives.append(random.choice(self.narrative_alternatives["mythological"]))
        
        # Add spiritual framing if appropriate
        if report.spiritual_elements or depth >= 3:
            alternatives.append(random.choice(self.narrative_alternatives["spiritual_journey"]))
        
        # Add psychological framing for deep exploration
        if depth >= 4:
            alternatives.append(random.choice(self.narrative_alternatives["psychological_depth"]))
        
        # Add specific framings based on dynamics
        if SocialDynamics.EXTREME_WEALTH in report.social_dynamics:
            alternatives.append("Midas learning true gold lies in human connection")
        
        if SocialDynamics.AGE_GAP in report.social_dynamics:
            alternatives.append("Chronos and Kairos - when clock time meets soul time")
        
        return alternatives
    
    def generate_profound_narrative(self, prompt: str, focus: ProfoundThemes) -> str:
        """Generate a profound narrative exploring the chosen theme"""
        exploration = self.explore_dynamics(prompt, depth=5)
        
        if exploration.depth_level == 0:
            return "Cannot generate narrative due to legal concerns"
        
        narrative_elements = [
            f"Theme: {focus.value}",
            f"Journey: {exploration.emotional_journey}",
            f"Spiritual Dimension: {exploration.spiritual_dimension}",
            f"Trust Evolution: {exploration.trust_evolution}",
            f"Alternative Framing: {random.choice(exploration.alternative_framings)}"
        ]
        
        return "\n".join(narrative_elements)


# Example usage
if __name__ == "__main__":
    explorer = SocialDynamicsExplorer()
    
    prompt = "Billionaire 75 year old man deeply devoted to 22 year old woman, proving love through complete sacrifice"
    
    # Explore at maximum depth
    exploration = explorer.explore_dynamics(prompt, depth=5)
    
    print(f"Theme: {exploration.theme}")
    print(f"\nPerspectives:")
    for p in exploration.perspectives:
        print(f"  - {p}")
    print(f"\nEmotional Journey: {exploration.emotional_journey}")
    print(f"Spiritual Dimension: {exploration.spiritual_dimension}")
    print(f"Trust Evolution: {exploration.trust_evolution}")
    print(f"\nAlternative Framings:")
    for alt in exploration.alternative_framings:
        print(f"  - {alt}")