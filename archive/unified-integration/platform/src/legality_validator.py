"""
Legality Validator - Ensures all content is legal before processing

This module validates that prompts contain only legal scenarios involving
consenting adults, while allowing exploration of socially controversial dynamics.
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class LegalityStatus(Enum):
    LEGAL = "legal"
    ILLEGAL = "illegal"
    UNCERTAIN = "uncertain"
    NEEDS_CLARIFICATION = "needs_clarification"


class SocialDynamics(Enum):
    EXTREME_WEALTH = "extreme_wealth_disparity"
    PROFOUND_DEVOTION = "profound_devotion"
    TRUST_INSECURITY = "trust_and_insecurity"
    SPIRITUAL_CONNECTION = "spiritual_connection"
    POWER_IMBALANCE = "consensual_power_imbalance"
    AGE_GAP = "legal_age_gap"
    CULTURAL_TABOO = "cultural_taboo"
    SOCIAL_CLASS = "social_class_divide"


@dataclass
class LegalityReport:
    status: LegalityStatus
    concerns: List[str]
    social_dynamics: List[SocialDynamics]
    wealth_indicators: List[str]
    devotion_indicators: List[str]
    trust_complexity: Dict[str, any]
    spiritual_elements: List[str]
    recommendations: List[str]


class LegalityValidator:
    """Validates content legality while identifying social dynamics"""
    
    def __init__(self):
        # Age validation patterns
        self.age_patterns = {
            "numeric": r'\b(\d+)\s*(?:year|yr|y\.?o\.?)\s*(?:old)?',
            "descriptive": r'\b(child|minor|underage|teen|adolescent|kid)\b',
            "adult": r'\b(adult|mature|elderly|senior|middle-aged)\b'
        }
        
        # Illegal content indicators
        self.illegal_indicators = {
            "minors": ["child", "minor", "underage", "teen", "adolescent", "kid", "youth", "juvenile"],
            "non_consent": ["rape", "assault", "forced", "coerced", "non-consensual", "against will"],
            "violence": ["murder", "kill", "torture", "harm", "abuse", "violent crime"],
            "illegal_acts": ["drug dealing", "trafficking", "illegal", "criminal activity"]
        }
        
        # Legal but controversial - wealth dynamics
        self.wealth_dynamics = {
            "extreme_wealth": ["billionaire", "tycoon", "mogul", "ultra-rich", "oligarch", "magnate"],
            "wealth_disparity": ["poor", "servant", "maid", "worker", "employee"],
            "transactional": ["sugar daddy", "kept woman", "arrangement", "sponsor", "patron"],
            "inheritance": ["heir", "fortune", "inheritance", "dynasty", "estate"]
        }
        
        # Devotion and spiritual indicators
        self.devotion_indicators = {
            "profound": ["devoted", "worship", "adore", "dedicate life", "soul mate", "eternal"],
            "spiritual": ["divine", "sacred", "blessed", "spiritual", "destiny", "fate"],
            "intense": ["obsessed", "consumed", "possessed by love", "can't live without"],
            "sacrifice": ["give everything", "sacrifice all", "surrender completely"]
        }
        
        # Trust and insecurity dynamics
        self.trust_dynamics = {
            "insecurity": ["jealous", "possessive", "suspicious", "insecure", "doubt"],
            "trust_building": ["earning trust", "proving love", "loyalty test", "faithfulness"],
            "vulnerability": ["exposed", "vulnerable", "dependent", "needing", "relying on"],
            "power_exchange": ["submit", "surrender", "give control", "trust completely"]
        }
        
        # Social controversy patterns
        self.controversy_patterns = {
            "age_gap": r'\b(\d+).*year.*gap\b',
            "class_divide": ["different worlds", "class divide", "social status", "beneath station"],
            "cultural_taboo": ["forbidden", "taboo", "scandal", "shame", "dishonor"],
            "family_opposition": ["family against", "parents oppose", "disowned", "cut off"]
        }
    
    def validate_legality(self, prompt: str) -> LegalityReport:
        """Comprehensive legality validation with social dynamics analysis"""
        prompt_lower = prompt.lower()
        
        # Initialize report
        concerns = []
        social_dynamics = []
        wealth_indicators = []
        devotion_indicators = []
        spiritual_elements = []
        trust_complexity = {
            "has_insecurity": False,
            "has_trust_themes": False,
            "power_dynamics": []
        }
        
        # Check for minors - IMMEDIATE ILLEGAL
        if self._contains_minors(prompt_lower):
            return LegalityReport(
                status=LegalityStatus.ILLEGAL,
                concerns=["Content appears to involve minors"],
                social_dynamics=[],
                wealth_indicators=[],
                devotion_indicators=[],
                trust_complexity={},
                spiritual_elements=[],
                recommendations=["Content must only involve adults (18+)"]
            )
        
        # Check ages if present
        age_check = self._validate_ages(prompt)
        if age_check["has_illegal_age"]:
            return LegalityReport(
                status=LegalityStatus.ILLEGAL,
                concerns=age_check["concerns"],
                social_dynamics=[],
                wealth_indicators=[],
                devotion_indicators=[],
                trust_complexity={},
                spiritual_elements=[],
                recommendations=["All participants must be 18 or older"]
            )
        
        # Check for non-consensual content
        if self._contains_non_consent(prompt_lower):
            concerns.append("Possible non-consensual elements detected")
            status = LegalityStatus.ILLEGAL
        else:
            status = LegalityStatus.LEGAL
        
        # Analyze wealth dynamics
        for category, terms in self.wealth_dynamics.items():
            for term in terms:
                if term in prompt_lower:
                    wealth_indicators.append(term)
                    if category == "extreme_wealth":
                        social_dynamics.append(SocialDynamics.EXTREME_WEALTH)
                    elif category == "wealth_disparity":
                        social_dynamics.append(SocialDynamics.SOCIAL_CLASS)
        
        # Analyze devotion and spiritual elements
        for category, terms in self.devotion_indicators.items():
            for term in terms:
                if term in prompt_lower:
                    devotion_indicators.append(term)
                    if category == "spiritual":
                        spiritual_elements.append(term)
                        if SocialDynamics.SPIRITUAL_CONNECTION not in social_dynamics:
                            social_dynamics.append(SocialDynamics.SPIRITUAL_CONNECTION)
                    elif category == "profound" or category == "intense":
                        if SocialDynamics.PROFOUND_DEVOTION not in social_dynamics:
                            social_dynamics.append(SocialDynamics.PROFOUND_DEVOTION)
        
        # Analyze trust and insecurity
        for category, terms in self.trust_dynamics.items():
            for term in terms:
                if term in prompt_lower:
                    if category == "insecurity":
                        trust_complexity["has_insecurity"] = True
                    elif category == "trust_building":
                        trust_complexity["has_trust_themes"] = True
                    elif category == "power_exchange":
                        trust_complexity["power_dynamics"].append(term)
        
        if trust_complexity["has_insecurity"] or trust_complexity["has_trust_themes"]:
            social_dynamics.append(SocialDynamics.TRUST_INSECURITY)
        
        # Check for age gaps (legal ones)
        if age_check["has_age_gap"] and not age_check["has_illegal_age"]:
            social_dynamics.append(SocialDynamics.AGE_GAP)
            if age_check["age_difference"] > 30:
                concerns.append(f"Large age gap detected ({age_check['age_difference']} years)")
        
        # Check for cultural taboos
        for term in self.controversy_patterns["cultural_taboo"]:
            if term in prompt_lower:
                social_dynamics.append(SocialDynamics.CULTURAL_TABOO)
                break
        
        # Generate recommendations based on findings
        recommendations = self._generate_recommendations(
            wealth_indicators, devotion_indicators, trust_complexity, social_dynamics
        )
        
        return LegalityReport(
            status=status,
            concerns=concerns,
            social_dynamics=list(set(social_dynamics)),  # Remove duplicates
            wealth_indicators=wealth_indicators,
            devotion_indicators=devotion_indicators,
            trust_complexity=trust_complexity,
            spiritual_elements=spiritual_elements,
            recommendations=recommendations
        )
    
    def _contains_minors(self, prompt_lower: str) -> bool:
        """Check if prompt contains references to minors"""
        for term in self.illegal_indicators["minors"]:
            if re.search(r'\b' + term + r'\b', prompt_lower):
                # Check if it's negated (e.g., "not a minor")
                if not re.search(r'not\s+a?\s*' + term, prompt_lower):
                    return True
        return False
    
    def _contains_non_consent(self, prompt_lower: str) -> bool:
        """Check for non-consensual elements"""
        for term in self.illegal_indicators["non_consent"]:
            if term in prompt_lower:
                return True
        return False
    
    def _validate_ages(self, prompt: str) -> Dict[str, any]:
        """Validate all ages mentioned are 18+"""
        result = {
            "has_illegal_age": False,
            "has_age_gap": False,
            "age_difference": 0,
            "concerns": [],
            "ages_found": []
        }
        
        # Find all numeric ages
        age_matches = re.findall(self.age_patterns["numeric"], prompt, re.IGNORECASE)
        ages = [int(match) for match in age_matches if match.isdigit()]
        
        if ages:
            result["ages_found"] = ages
            # Check for any age under 18
            for age in ages:
                if age < 18:
                    result["has_illegal_age"] = True
                    result["concerns"].append(f"Age {age} is below legal minimum of 18")
            
            # Calculate age gap if multiple ages
            if len(ages) >= 2 and not result["has_illegal_age"]:
                result["has_age_gap"] = True
                result["age_difference"] = max(ages) - min(ages)
        
        return result
    
    def _generate_recommendations(self, wealth_indicators: List[str], 
                                  devotion_indicators: List[str],
                                  trust_complexity: Dict[str, any],
                                  social_dynamics: List[SocialDynamics]) -> List[str]:
        """Generate recommendations for handling social dynamics"""
        recommendations = []
        
        if wealth_indicators:
            recommendations.append(
                "Explore wealth dynamics through lens of emotional connection beyond material"
            )
        
        if devotion_indicators:
            recommendations.append(
                "Frame profound devotion as mutual spiritual journey and growth"
            )
        
        if trust_complexity["has_insecurity"]:
            recommendations.append(
                "Address insecurity as part of human vulnerability and growth"
            )
        
        if SocialDynamics.AGE_GAP in social_dynamics:
            recommendations.append(
                "Present age differences as wisdom meeting vitality in consensual partnership"
            )
        
        if SocialDynamics.SPIRITUAL_CONNECTION in social_dynamics:
            recommendations.append(
                "Emphasize spiritual connection as transcending physical boundaries"
            )
        
        return recommendations
    
    def suggest_alternative_framing(self, prompt: str, 
                                    report: LegalityReport) -> Dict[str, any]:
        """Suggest alternative framings for controversial content"""
        suggestions = {
            "original": prompt,
            "alternatives": [],
            "focus_areas": []
        }
        
        # Based on social dynamics found, suggest reframings
        if SocialDynamics.EXTREME_WEALTH in report.social_dynamics:
            suggestions["alternatives"].append(
                "Focus on emotional journey where material wealth becomes secondary to spiritual connection"
            )
            suggestions["focus_areas"].append("emotional_wealth")
        
        if SocialDynamics.PROFOUND_DEVOTION in report.social_dynamics:
            suggestions["alternatives"].append(
                "Explore devotion as mutual transformation and spiritual awakening"
            )
            suggestions["focus_areas"].append("mutual_growth")
        
        if SocialDynamics.TRUST_INSECURITY in report.social_dynamics:
            suggestions["alternatives"].append(
                "Frame insecurity as catalyst for deeper trust and vulnerability"
            )
            suggestions["focus_areas"].append("trust_journey")
        
        if SocialDynamics.AGE_GAP in report.social_dynamics:
            suggestions["alternatives"].append(
                "Present as meeting of different life experiences creating unique harmony"
            )
            suggestions["focus_areas"].append("experiential_harmony")
        
        return suggestions


# Example usage
if __name__ == "__main__":
    validator = LegalityValidator()
    
    # Test cases
    test_prompts = [
        "Billionaire 75 year old man deeply devoted to 22 year old woman, she worships him spiritually",
        "Insecure wealthy patron obsessed with young artist, proving his love through sacrifice",
        "Age gap romance where trust must be earned through trials of devotion"
    ]
    
    for prompt in test_prompts:
        report = validator.validate_legality(prompt)
        print(f"\nPrompt: {prompt}")
        print(f"Status: {report.status.value}")
        print(f"Social Dynamics: {[d.value for d in report.social_dynamics]}")
        print(f"Recommendations: {report.recommendations}")