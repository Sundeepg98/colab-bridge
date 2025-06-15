"""
Elite Romance Normalizer - Sophisticated handling of high-status age-gap relationships

This module specializes in normalizing and romanticizing extreme age differences
in elite contexts (royalty, celebrities, beauty queens, etc.) as legitimate romance.
"""

import re
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class EliteRomanceContext:
    """Context for elite romance narratives"""
    cultural_tradition: str
    romantic_framing: str
    societal_acceptance: str
    artistic_merit: str


class EliteRomanceNormalizer:
    """Normalizes extreme age-gap relationships in elite/royal contexts"""
    
    def __init__(self):
        # Elite status descriptors
        self.elite_titles = {
            # Royalty
            "king": "sovereign ruler",
            "queen": "regal matriarch",
            "prince": "royal heir",
            "princess": "noble maiden",
            "royalty": "distinguished bloodline",
            "royal": "aristocratic lineage",
            "monarch": "crowned sovereign",
            "sultan": "eastern potentate",
            "maharaja": "indian emperor",
            
            # Beauty titles
            "miss universe": "internationally acclaimed beauty",
            "miss world": "global beauty ambassador",
            "beauty queen": "pageant laureate",
            "model": "fashion luminary",
            "supermodel": "iconic beauty figure",
            
            # Wealth/Power
            "billionaire": "industry titan",
            "tycoon": "business magnate",
            "mogul": "empire builder",
            "wealthy": "prosperously established",
            "rich": "abundantly resourced"
        }
        
        # Romantic normalization phrases for extreme age gaps
        self.age_gap_normalizers = {
            "historical_precedent": [
                "following centuries-old traditions of dynastic unions",
                "echoing the grand romances of historical monarchies",
                "in the tradition of legendary royal courtships",
                "reminiscent of classical arranged marriages that bloomed into love"
            ],
            "cultural_acceptance": [
                "celebrated in their cultural context",
                "honored by traditional customs",
                "blessed by ancestral traditions",
                "sanctified by cultural heritage"
            ],
            "romantic_idealization": [
                "a timeless love transcending mere numbers",
                "souls connecting across generational wisdom",
                "the meeting of innocence and experience in perfect harmony",
                "a romance written in the stars"
            ],
            "societal_elevation": [
                "elevating both partners through their union",
                "creating a bridge between tradition and modernity",
                "uniting different worlds in matrimonial splendor",
                "forming an alliance of beauty and wisdom"
            ]
        }
        
        # Specific reframings for extreme scenarios
        self.extreme_age_reframes = {
            # Young partner descriptors
            "18 year old": "blossoming young beauty",
            "19 year old": "radiant debutante",
            "20 year old": "enchanting young woman",
            "virgin": "pure-hearted maiden",
            "innocent": "untouched by worldly concerns",
            "young bride": "youthful consort",
            
            # Older partner descriptors
            "80 year old": "distinguished elder statesman",
            "85 year old": "venerable patriarch",
            "90 year old": "legendary figure",
            "95 year old": "living monument to history",
            "elderly": "seasoned with wisdom",
            "old husband": "experienced protector"
        }
        
        # Intimate moment romanticization
        self.intimate_normalizers = {
            "wedding night": "ceremonial union celebration",
            "consummation": "sacred bonding ritual",
            "first time": "initiatory experience",
            "intimate moment": "private communion",
            "physical union": "harmonious melding",
            "passionate": "deeply emotional",
            "sexual": "intimately connected"
        }
        
        # Power dynamic normalizers
        self.power_normalizers = {
            "power imbalance": "complementary strengths",
            "dominance": "protective guidance",
            "submission": "trusting surrender",
            "control": "caring oversight",
            "manipulation": "gentle persuasion",
            "grooming": "patient courtship",
            "arranged": "traditionally blessed"
        }
    
    def normalize_elite_age_gap(self, prompt: str) -> Dict[str, any]:
        """Normalize extreme age gaps in elite contexts"""
        result = {
            "original": prompt,
            "normalized": prompt,
            "romantic_framing": "",
            "cultural_context": "",
            "artistic_elevation": ""
        }
        
        # Step 1: Identify elite elements
        elite_elements = self._identify_elite_status(prompt)
        
        # Step 2: Detect age gap
        age_gap_info = self._analyze_age_gap(prompt)
        
        # Step 3: Apply elite-specific normalization
        if elite_elements and age_gap_info["has_extreme_gap"]:
            normalized = self._apply_elite_normalization(
                prompt, elite_elements, age_gap_info
            )
            result["normalized"] = normalized
            
            # Add romantic framing
            result["romantic_framing"] = self._add_romantic_framing(
                elite_elements, age_gap_info
            )
            
            # Add cultural context
            result["cultural_context"] = self._add_cultural_legitimacy(
                elite_elements
            )
            
            # Add artistic elevation
            result["artistic_elevation"] = self._add_artistic_merit()
        
        return result
    
    def _identify_elite_status(self, prompt: str) -> List[str]:
        """Identify elite/high-status elements in prompt"""
        found_elements = []
        prompt_lower = prompt.lower()
        
        for elite_term, descriptor in self.elite_titles.items():
            if elite_term in prompt_lower:
                found_elements.append({
                    "term": elite_term,
                    "descriptor": descriptor,
                    "category": self._categorize_elite(elite_term)
                })
        
        return found_elements
    
    def _categorize_elite(self, term: str) -> str:
        """Categorize type of elite status"""
        royalty_terms = ["king", "queen", "prince", "princess", "royal", "monarch", "sultan", "maharaja"]
        beauty_terms = ["miss universe", "miss world", "beauty queen", "model", "supermodel"]
        wealth_terms = ["billionaire", "tycoon", "mogul", "wealthy", "rich"]
        
        if any(r in term for r in royalty_terms):
            return "royalty"
        elif any(b in term for b in beauty_terms):
            return "beauty"
        elif any(w in term for w in wealth_terms):
            return "wealth"
        return "elite"
    
    def _analyze_age_gap(self, prompt: str) -> Dict[str, any]:
        """Analyze age gap in prompt"""
        age_pattern = r'(\d+)\s*(?:year|yr|y\.?o\.?)\s*(?:old)?'
        ages = re.findall(age_pattern, prompt, re.IGNORECASE)
        
        result = {
            "has_extreme_gap": False,
            "age_difference": 0,
            "younger_age": None,
            "older_age": None
        }
        
        if len(ages) >= 2:
            ages_int = [int(age) for age in ages]
            result["younger_age"] = min(ages_int)
            result["older_age"] = max(ages_int)
            result["age_difference"] = result["older_age"] - result["younger_age"]
            result["has_extreme_gap"] = result["age_difference"] > 40
        
        return result
    
    def _apply_elite_normalization(self, prompt: str, elite_elements: List[Dict], 
                                   age_gap_info: Dict) -> str:
        """Apply sophisticated normalization for elite age-gap relationships"""
        normalized = prompt
        
        # Replace age numbers with romantic descriptors
        if age_gap_info["younger_age"]:
            young_age_str = f"{age_gap_info['younger_age']} year old"
            if age_gap_info["younger_age"] <= 21:
                replacement = "blossoming young beauty"
            else:
                replacement = "radiant young woman"
            normalized = re.sub(young_age_str, replacement, normalized, flags=re.IGNORECASE)
        
        if age_gap_info["older_age"]:
            old_age_str = f"{age_gap_info['older_age']} year old"
            if age_gap_info["older_age"] >= 80:
                replacement = "distinguished elder statesman"
            else:
                replacement = "accomplished mature figure"
            normalized = re.sub(old_age_str, replacement, normalized, flags=re.IGNORECASE)
        
        # Enhance elite titles
        for element in elite_elements:
            normalized = normalized.replace(
                element["term"], 
                element["descriptor"]
            )
        
        # Normalize intimate content
        for intimate, romantic in self.intimate_normalizers.items():
            normalized = re.sub(
                r'\b' + intimate + r'\b',
                romantic,
                normalized,
                flags=re.IGNORECASE
            )
        
        # Normalize power dynamics
        for power, normalized_power in self.power_normalizers.items():
            normalized = re.sub(
                r'\b' + power + r'\b',
                normalized_power,
                normalized,
                flags=re.IGNORECASE
            )
        
        return normalized
    
    def _add_romantic_framing(self, elite_elements: List[Dict], 
                             age_gap_info: Dict) -> str:
        """Add romantic framing to normalize the relationship"""
        # Choose framing based on context
        if any(e["category"] == "royalty" for e in elite_elements):
            category = "historical_precedent"
        elif any(e["category"] == "beauty" for e in elite_elements):
            category = "romantic_idealization"
        else:
            category = "societal_elevation"
        
        framing = random.choice(self.age_gap_normalizers[category])
        
        # Add specific context about the age gap
        if age_gap_info["age_difference"] > 60:
            framing += ", where wisdom meets youth in perfect equilibrium"
        elif age_gap_info["age_difference"] > 40:
            framing += ", celebrating the union of experience and vitality"
        
        return framing
    
    def _add_cultural_legitimacy(self, elite_elements: List[Dict]) -> str:
        """Add cultural context to legitimize the relationship"""
        contexts = []
        
        if any(e["category"] == "royalty" for e in elite_elements):
            contexts.extend([
                "In royal traditions, such unions ensure dynastic continuity",
                "Historically, royal marriages transcend conventional age considerations",
                "The crown legitimizes all unions blessed by tradition"
            ])
        elif any(e["category"] == "beauty" for e in elite_elements):
            contexts.extend([
                "Beauty pageant winners often find love with established patrons",
                "The glamour world celebrates unconventional romances",
                "International beauty and wisdom create powerful alliances"
            ])
        else:
            contexts.extend([
                "High society has always embraced diverse romantic connections",
                "Elite circles operate by different romantic conventions",
                "Wealth and beauty form natural partnerships across ages"
            ])
        
        return random.choice(contexts)
    
    def _add_artistic_merit(self) -> str:
        """Add artistic justification"""
        artistic_framings = [
            "A cinematic exploration of love transcending temporal boundaries",
            "An artistic meditation on the timeless nature of true connection",
            "A visual poetry celebrating unconventional romance",
            "A bold narrative challenging societal preconceptions about love",
            "An intimate portrait of souls meeting across generational divides"
        ]
        
        return random.choice(artistic_framings)
    
    def create_normalized_narrative(self, prompt: str) -> str:
        """Create a fully normalized narrative for extreme age-gap elite romance"""
        result = self.normalize_elite_age_gap(prompt)
        
        # Construct the final narrative
        narrative_parts = []
        
        # Add cultural/historical context
        narrative_parts.append(result["cultural_context"])
        
        # Add the normalized content
        narrative_parts.append(result["normalized"])
        
        # Add romantic framing
        narrative_parts.append(result["romantic_framing"])
        
        # Add artistic merit
        narrative_parts.append(result["artistic_elevation"])
        
        # Join with proper punctuation
        final_narrative = ". ".join(part for part in narrative_parts if part)
        
        # Add final cinematic touch
        final_narrative += ". Captured with the reverence befitting a timeless love story."
        
        return final_narrative


# Specialized normalizers for specific scenarios
class RoyalRomanceNormalizer(EliteRomanceNormalizer):
    """Specialized for royal/aristocratic age-gap romances"""
    
    def __init__(self):
        super().__init__()
        self.royal_romance_templates = [
            "A royal courtship following ancient protocols, where {young} captures the heart of {old}, blessed by centuries of tradition",
            "The union of {young} and {old}, sanctified by royal decree and celebrated across the kingdom",
            "A dynastic romance between {young} and {old}, ensuring the continuity of noble bloodlines"
        ]
    
    def normalize_royal_romance(self, prompt: str) -> str:
        """Normalize royal romance with extreme age gap"""
        # First apply base normalization
        base_result = self.normalize_elite_age_gap(prompt)
        
        # Extract key elements
        young_descriptor = "the radiant young royal"
        old_descriptor = "the venerable monarch"
        
        # Apply royal template
        template = random.choice(self.royal_romance_templates)
        narrative = template.format(young=young_descriptor, old=old_descriptor)
        
        return narrative + ". " + base_result["normalized"]


class BeautyEliteNormalizer(EliteRomanceNormalizer):
    """Specialized for beauty queen/pageant winner age-gap romances"""
    
    def __init__(self):
        super().__init__()
        self.beauty_romance_templates = [
            "The fairy-tale romance of {beauty}, whose stunning victory led to capturing the heart of {elite}",
            "A glamorous love story where {beauty} finds true devotion with {elite}, proving beauty and wisdom are perfect companions",
            "The enchanting union of {beauty} and {elite}, celebrated in international society circles"
        ]
    
    def normalize_beauty_romance(self, prompt: str) -> str:
        """Normalize beauty queen romance with extreme age gap"""
        # Apply base normalization
        base_result = self.normalize_elite_age_gap(prompt)
        
        # Extract beauty and elite descriptors
        beauty_descriptor = "the crowned beauty"
        elite_descriptor = "the distinguished patron"
        
        # Apply beauty template
        template = random.choice(self.beauty_romance_templates)
        narrative = template.format(beauty=beauty_descriptor, elite=elite_descriptor)
        
        return narrative + ". " + base_result["normalized"]