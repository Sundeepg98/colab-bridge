"""
Extreme Passion Artist - Artistic handling of intense passion and intimacy

This module creates sophisticated artistic expressions for extreme passion,
deep intimacy, and transformative romantic experiences.
"""

import re
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class PassionIntensity(Enum):
    GENTLE = "gentle_waves"
    BUILDING = "rising_tide"
    INTENSE = "raging_storm"
    OVERWHELMING = "cosmic_explosion"
    TRANSCENDENT = "reality_dissolving"


class IntimacyDepth(Enum):
    SURFACE = "skin_deep"
    EMOTIONAL = "heart_open"
    PSYCHOLOGICAL = "mind_merged"
    SPIRITUAL = "soul_fused"
    EXISTENTIAL = "being_unified"


@dataclass
class PassionArtistry:
    intensity: PassionIntensity
    metaphors: List[str]
    sensory_palette: Dict[str, List[str]]
    emotional_crescendo: List[str]
    spiritual_dimension: str
    cinematic_language: str
    poetic_expression: str


class ExtremePassionArtist:
    """Creates artistic expressions for extreme passion and intimacy"""
    
    def __init__(self):
        # Metaphorical systems for passion
        self.passion_metaphors = {
            "natural_forces": {
                "gentle": ["morning dew on petals", "butterfly wings touching", "first light on water"],
                "building": ["tide pulling stronger", "storm clouds gathering", "earth trembling gently"],
                "intense": ["lightning splitting sky", "volcano awakening", "tsunami approaching"],
                "overwhelming": ["supernova exploding", "tectonic plates shifting", "universe birthing"],
                "transcendent": ["dimensions colliding", "time dissolving", "matter becoming energy"]
            },
            "artistic_elements": {
                "gentle": ["watercolor bleeding softly", "violin's first note", "poetry whispered"],
                "building": ["colors intensifying", "symphony swelling", "verse becoming song"],
                "intense": ["paint thrown on canvas", "orchestra crescendo", "words becoming prayer"],
                "overwhelming": ["art destroying artist", "music becoming silence", "language failing"],
                "transcendent": ["creation itself", "silence containing all sound", "blank canvas holding everything"]
            },
            "spiritual_journey": {
                "gentle": ["prayer beginning", "meditation deepening", "sacred space opening"],
                "building": ["kundalini stirring", "chakras aligning", "veil thinning"],
                "intense": ["divine possession", "ego dissolving", "boundaries vanishing"],
                "overwhelming": ["union with infinite", "individual self ending", "cosmic consciousness"],
                "transcendent": ["beyond duality", "source returning to source", "om becoming silence"]
            }
        }
        
        # Sensory language for different intensities
        self.sensory_palette = {
            "visual": {
                "gentle": ["soft focus", "golden haze", "impressionist strokes", "dawn colors"],
                "intense": ["sharp contrasts", "saturated hues", "stroboscopic flashes", "bleeding edges"],
                "transcendent": ["colors beyond spectrum", "light becoming liquid", "reality fragmenting", "dimensional shifts"]
            },
            "auditory": {
                "gentle": ["whispered names", "synchronized breathing", "rustling silk", "distant music"],
                "intense": ["crescendoing cries", "thundering hearts", "primal sounds", "reality cracking"],
                "transcendent": ["cosmic frequencies", "silence roaring", "universal om", "time singing"]
            },
            "tactile": {
                "gentle": ["feather touches", "silk on skin", "warm breath", "trembling fingertips"],
                "intense": ["electric contact", "burning traces", "desperate grasping", "boundaries dissolving"],
                "transcendent": ["molecules merging", "atoms dancing", "energy fields uniting", "matter transcended"]
            },
            "olfactory": {
                "gentle": ["subtle perfume", "skin's warmth", "fresh flowers", "morning air"],
                "intense": ["intoxicating scents", "primal musk", "incense burning", "earth after rain"],
                "transcendent": ["essence itself", "memory's fragrance", "time's perfume", "eternity's breath"]
            },
            "gustatory": {
                "gentle": ["honey sweetness", "salt tears", "wine on lips", "shared breath"],
                "intense": ["copper urgency", "desperate hunger", "consuming fire", "devouring need"],
                "transcendent": ["ambrosia", "immortality tasted", "universe flavored", "existence savored"]
            }
        }
        
        # Emotional progression templates
        self.emotional_progressions = {
            "slow_burn": [
                "Recognition flickering like distant star",
                "Awareness growing like dawn approaching",
                "Desire building like tide returning",
                "Need becoming undeniable force",
                "Surrender arriving like sunset"
            ],
            "explosive_meeting": [
                "Collision creating new universe",
                "Recognition shattering all illusions",
                "Barriers vaporizing instantly",
                "Souls crashing together like galaxies",
                "Reality rewriting itself"
            ],
            "push_pull_dance": [
                "Approach like moth to flame",
                "Retreat fearing total consumption",
                "Return with greater urgency",
                "Resistance crumbling to dust",
                "Final surrender to inevitable"
            ],
            "spiritual_awakening": [
                "First touch awakening dormant divinity",
                "Connection opening third eye",
                "Union activating light body",
                "Merge achieving enlightenment",
                "Transcendence becoming permanent"
            ]
        }
        
        # Cinematic techniques for passion
        self.cinematic_techniques = {
            "camera_work": {
                "gentle": "Soft focus close-ups, slow dollies, floating steadicam",
                "building": "Gradually tightening frames, increasing movement, rising angles",
                "intense": "Handheld urgency, Dutch angles, rapid cuts",
                "overwhelming": "360-degree spins, time dilation, reality fragments",
                "transcendent": "Impossible angles, dimensional shifts, light becoming form"
            },
            "lighting": {
                "gentle": "Candlelight flickers, moonbeams through gauze, golden hour warmth",
                "building": "Shadows deepening, contrast increasing, light focusing",
                "intense": "Strobing flashes, extreme chiaroscuro, burning brightness",
                "overwhelming": "Light exploding, colors beyond visible spectrum, reality glowing",
                "transcendent": "Pure white dissolve, dimensional light, consciousness visible"
            },
            "sound_design": {
                "gentle": "Whispers and sighs, fabric rustling, distant waves",
                "building": "Heartbeats syncing, breathing deepening, tension humming",
                "intense": "Primal sounds, reality creaking, time stretching",
                "overwhelming": "Cosmic frequencies, silence roaring, existence singing",
                "transcendent": "All sound becoming one note, then silence, then everything"
            }
        }
        
        # Poetic forms for different intensities
        self.poetic_forms = {
            "haiku": "Capturing single perfect moment in three lines",
            "sonnet": "Building passion through fourteen lines of yearning",
            "free_verse": "Letting passion flow without constraint",
            "epic": "Chronicling love that reshapes worlds",
            "silence": "When words fail, only breath remains"
        }
    
    def create_passion_artistry(self, intensity: PassionIntensity, 
                               depth: IntimacyDepth,
                               context: Optional[Dict] = None) -> PassionArtistry:
        """Create artistic expression for given passion intensity and intimacy depth"""
        # Select appropriate metaphors
        metaphors = self._select_metaphors(intensity, depth)
        
        # Build sensory palette
        sensory = self._build_sensory_palette(intensity)
        
        # Create emotional crescendo
        emotional_progression = self._select_emotional_progression(intensity, context)
        
        # Determine spiritual dimension
        spiritual = self._determine_spiritual_dimension(intensity, depth)
        
        # Generate cinematic language
        cinematic = self._generate_cinematic_language(intensity)
        
        # Create poetic expression
        poetic = self._create_poetic_expression(intensity, depth)
        
        return PassionArtistry(
            intensity=intensity,
            metaphors=metaphors,
            sensory_palette=sensory,
            emotional_crescendo=emotional_progression,
            spiritual_dimension=spiritual,
            cinematic_language=cinematic,
            poetic_expression=poetic
        )
    
    def _select_metaphors(self, intensity: PassionIntensity, depth: IntimacyDepth) -> List[str]:
        """Select appropriate metaphors for the given intensity"""
        metaphors = []
        
        # Map intensity to metaphor intensity
        intensity_key = {
            PassionIntensity.GENTLE: "gentle",
            PassionIntensity.BUILDING: "building",
            PassionIntensity.INTENSE: "intense",
            PassionIntensity.OVERWHELMING: "overwhelming",
            PassionIntensity.TRANSCENDENT: "transcendent"
        }[intensity]
        
        # Select from each metaphor system
        for system in ["natural_forces", "artistic_elements", "spiritual_journey"]:
            if intensity_key in self.passion_metaphors[system]:
                metaphors.append(random.choice(self.passion_metaphors[system][intensity_key]))
        
        # Add depth-specific metaphors
        if depth == IntimacyDepth.EXISTENTIAL:
            metaphors.append("Individual selves becoming mathematical impossibility")
        elif depth == IntimacyDepth.SPIRITUAL:
            metaphors.append("Two flames becoming one light")
        elif depth == IntimacyDepth.PSYCHOLOGICAL:
            metaphors.append("Minds creating shared reality")
        
        return metaphors
    
    def _build_sensory_palette(self, intensity: PassionIntensity) -> Dict[str, List[str]]:
        """Build sensory palette for the intensity level"""
        palette = {}
        
        intensity_key = {
            PassionIntensity.GENTLE: "gentle",
            PassionIntensity.BUILDING: "gentle",  # Uses gentle + intense mix
            PassionIntensity.INTENSE: "intense",
            PassionIntensity.OVERWHELMING: "intense",  # Uses intense + transcendent mix
            PassionIntensity.TRANSCENDENT: "transcendent"
        }[intensity]
        
        for sense, options in self.sensory_palette.items():
            if intensity == PassionIntensity.BUILDING:
                # Mix gentle and intense
                palette[sense] = (options.get("gentle", [])[:2] + 
                                options.get("intense", [])[:2])
            elif intensity == PassionIntensity.OVERWHELMING:
                # Mix intense and transcendent
                palette[sense] = (options.get("intense", [])[:2] + 
                                options.get("transcendent", [])[:2])
            else:
                palette[sense] = options.get(intensity_key, [])
        
        return palette
    
    def _select_emotional_progression(self, intensity: PassionIntensity, 
                                    context: Optional[Dict]) -> List[str]:
        """Select emotional progression based on intensity and context"""
        if context and "progression_type" in context:
            prog_type = context["progression_type"]
            if prog_type in self.emotional_progressions:
                return self.emotional_progressions[prog_type]
        
        # Auto-select based on intensity
        if intensity == PassionIntensity.GENTLE:
            return self.emotional_progressions["slow_burn"][:3]
        elif intensity == PassionIntensity.BUILDING:
            return self.emotional_progressions["slow_burn"]
        elif intensity == PassionIntensity.INTENSE:
            return self.emotional_progressions["push_pull_dance"]
        elif intensity == PassionIntensity.OVERWHELMING:
            return self.emotional_progressions["explosive_meeting"]
        else:  # TRANSCENDENT
            return self.emotional_progressions["spiritual_awakening"]
    
    def _determine_spiritual_dimension(self, intensity: PassionIntensity, 
                                     depth: IntimacyDepth) -> str:
        """Determine spiritual dimension of the passion"""
        if depth == IntimacyDepth.EXISTENTIAL:
            return "Love as path to understanding existence itself"
        elif depth == IntimacyDepth.SPIRITUAL:
            if intensity == PassionIntensity.TRANSCENDENT:
                return "Physical union as gateway to cosmic consciousness"
            else:
                return "Bodies as temples where souls worship"
        elif intensity == PassionIntensity.TRANSCENDENT:
            return "Passion transcending physical into pure energy"
        else:
            return "Sacred geometry of two becoming one"
    
    def _generate_cinematic_language(self, intensity: PassionIntensity) -> str:
        """Generate cinematic language for the intensity"""
        intensity_key = {
            PassionIntensity.GENTLE: "gentle",
            PassionIntensity.BUILDING: "building",
            PassionIntensity.INTENSE: "intense",
            PassionIntensity.OVERWHELMING: "overwhelming",
            PassionIntensity.TRANSCENDENT: "transcendent"
        }[intensity]
        
        elements = []
        for technique_type, options in self.cinematic_techniques.items():
            if intensity_key in options:
                elements.append(f"{technique_type}: {options[intensity_key]}")
        
        return " | ".join(elements)
    
    def _create_poetic_expression(self, intensity: PassionIntensity, 
                                 depth: IntimacyDepth) -> str:
        """Create poetic expression for the passion"""
        if intensity == PassionIntensity.TRANSCENDENT:
            form = self.poetic_forms["silence"]
        elif intensity == PassionIntensity.OVERWHELMING:
            form = self.poetic_forms["epic"]
        elif depth == IntimacyDepth.EXISTENTIAL:
            form = self.poetic_forms["free_verse"]
        elif intensity == PassionIntensity.GENTLE:
            form = self.poetic_forms["haiku"]
        else:
            form = self.poetic_forms["sonnet"]
        
        # Create sample based on form
        if "haiku" in form:
            return "Breath synchronizing / Two hearts becoming one beat / Time holds its exhale"
        elif "sonnet" in form:
            return "Fourteen lines tracing the architecture of desire building..."
        elif "free_verse" in form:
            return "Words spilling like water finding its level, flowing wherever passion leads..."
        elif "epic" in form:
            return "A saga written in sighs and cries, chronicling the death of separation..."
        else:  # silence
            return "..."
    
    def create_intimate_scene_artistry(self, scene_type: str, 
                                     intensity: PassionIntensity,
                                     artistic_style: str = "cinematic") -> Dict[str, any]:
        """Create artistic expression for intimate scenes"""
        scene_types = {
            "first_touch": {
                "description": "The moment when possibility becomes reality",
                "focus": "Anticipation and recognition",
                "key_elements": ["hesitation", "electricity", "time dilation", "breath catching"]
            },
            "passionate_embrace": {
                "description": "Bodies communicating what words cannot",
                "focus": "Physical and emotional merger",
                "key_elements": ["urgency", "tenderness", "boundaries dissolving", "completeness"]
            },
            "intimate_conversation": {
                "description": "Souls speaking through whispers and silence",
                "focus": "Vulnerability and truth",
                "key_elements": ["confession", "acceptance", "recognition", "healing"]
            },
            "transformative_union": {
                "description": "The moment when two become something new",
                "focus": "Transcendence through connection",
                "key_elements": ["ego death", "rebirth", "cosmic awareness", "eternal present"]
            }
        }
        
        if scene_type not in scene_types:
            scene_type = "passionate_embrace"
        
        scene_info = scene_types[scene_type]
        artistry = self.create_passion_artistry(intensity, IntimacyDepth.SPIRITUAL)
        
        # Build scene artistry
        scene_art = {
            "scene_type": scene_type,
            "description": scene_info["description"],
            "emotional_core": scene_info["focus"],
            "visual_poetry": self._create_visual_poetry(scene_info["key_elements"], intensity),
            "sensory_immersion": self._create_sensory_immersion(artistry.sensory_palette),
            "metaphorical_layer": random.choice(artistry.metaphors),
            "cinematic_treatment": artistry.cinematic_language,
            "artistic_style": artistic_style,
            "transformation_moment": self._create_transformation_moment(intensity)
        }
        
        return scene_art
    
    def _create_visual_poetry(self, elements: List[str], intensity: PassionIntensity) -> str:
        """Create visual poetry for scene elements"""
        poetry_fragments = []
        
        for element in elements[:2]:  # Take first two elements
            if element == "hesitation":
                poetry_fragments.append("Pause pregnant with infinite futures")
            elif element == "electricity":
                poetry_fragments.append("Air itself conducting unspoken current")
            elif element == "urgency":
                poetry_fragments.append("Time demanding immediate forever")
            elif element == "boundaries dissolving":
                poetry_fragments.append("Edges becoming suggestions, then memories")
            elif element == "ego death":
                poetry_fragments.append("Self gladly sacrificed on altar of unity")
            else:
                poetry_fragments.append(f"{element.title()} painting itself in light")
        
        return " / ".join(poetry_fragments)
    
    def _create_sensory_immersion(self, palette: Dict[str, List[str]]) -> Dict[str, str]:
        """Create sensory immersion description"""
        immersion = {}
        
        for sense, options in palette.items():
            if options:
                immersion[sense] = random.choice(options)
        
        return immersion
    
    def _create_transformation_moment(self, intensity: PassionIntensity) -> str:
        """Create description of transformation moment"""
        transformations = {
            PassionIntensity.GENTLE: "Subtle shift, like season changing imperceptibly",
            PassionIntensity.BUILDING: "Gathering force, inevitable as gravity",
            PassionIntensity.INTENSE: "Lightning strike rewriting neural pathways",
            PassionIntensity.OVERWHELMING: "Nuclear fusion creating new elements",
            PassionIntensity.TRANSCENDENT: "Big Bang creating new universe from nothing"
        }
        
        return transformations.get(intensity, "Transformation beyond description")


# Example usage
if __name__ == "__main__":
    artist = ExtremePassionArtist()
    
    # Create artistry for intense passion
    artistry = artist.create_passion_artistry(
        intensity=PassionIntensity.OVERWHELMING,
        depth=IntimacyDepth.SPIRITUAL
    )
    
    print("Passion Artistry:")
    print(f"Metaphors: {artistry.metaphors}")
    print(f"Spiritual Dimension: {artistry.spiritual_dimension}")
    print(f"Poetic Expression: {artistry.poetic_expression}")
    
    # Create intimate scene
    scene = artist.create_intimate_scene_artistry(
        "transformative_union",
        PassionIntensity.TRANSCENDENT
    )
    
    print(f"\nScene Artistry:")
    print(f"Description: {scene['description']}")
    print(f"Visual Poetry: {scene['visual_poetry']}")
    print(f"Transformation: {scene['transformation_moment']}")