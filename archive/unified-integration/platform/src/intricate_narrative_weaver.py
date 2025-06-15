"""
Intricate Narrative Weaver - Creates deeply layered romance narratives

This module generates complex, multi-layered romance narratives with
intricate plot structures, character development, and thematic depth.
"""

import re
import random
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum
from sophisticated_romance_handler import SophisticatedRomanceHandler
from extreme_passion_artist import ExtremePassionArtist, PassionIntensity
from social_dynamics_explorer import SocialDynamicsExplorer


class NarrativeStructure(Enum):
    LINEAR = "linear_progression"
    CIRCULAR = "circular_return"
    SPIRAL = "spiral_deepening"
    FRACTAL = "fractal_recursion"
    QUANTUM = "quantum_entanglement"


class PlotComplexity(Enum):
    SIMPLE = "single_thread"
    LAYERED = "multiple_threads"
    WOVEN = "interwoven_destinies"
    LABYRINTHINE = "maze_of_possibilities"
    MULTIDIMENSIONAL = "parallel_realities"


class ThematicDepth(Enum):
    SURFACE = "apparent_meaning"
    SYMBOLIC = "hidden_symbols"
    ARCHETYPAL = "universal_patterns"
    PHILOSOPHICAL = "existential_questions"
    METAPHYSICAL = "reality_transcending"


@dataclass
class CharacterArc:
    starting_point: str
    catalyst_moment: str
    resistance_phase: str
    transformation_process: str
    integration_outcome: str
    shadow_work: List[str]
    gifts_discovered: List[str]


@dataclass
class PlotThread:
    thread_name: str
    tension_source: str
    complications: List[str]
    resolution_path: str
    thematic_significance: str


@dataclass
class IntricateNarrative:
    structure: NarrativeStructure
    complexity: PlotComplexity
    thematic_depth: ThematicDepth
    character_arcs: Dict[str, CharacterArc]
    plot_threads: List[PlotThread]
    temporal_layers: List[str]
    symbolic_elements: Dict[str, str]
    transformation_stages: List[str]
    climactic_convergence: str
    resolution_symphony: str
    deeper_meaning: str


class IntricateNarrativeWeaver:
    """Weaves deeply intricate romance narratives with multiple layers"""
    
    def __init__(self):
        self.romance_handler = SophisticatedRomanceHandler()
        self.passion_artist = ExtremePassionArtist()
        self.dynamics_explorer = SocialDynamicsExplorer()
        
        # Narrative structures
        self.structure_patterns = {
            NarrativeStructure.LINEAR: {
                "description": "Straightforward progression from meeting to union",
                "stages": ["Recognition", "Attraction", "Conflict", "Resolution", "Union"],
                "complexity": "Simple but profound"
            },
            NarrativeStructure.CIRCULAR: {
                "description": "Ending where it began but transformed",
                "stages": ["Initial meeting", "Journey apart", "Individual growth", "Return transformed", "New beginning"],
                "complexity": "Past informing present"
            },
            NarrativeStructure.SPIRAL: {
                "description": "Revisiting themes at deeper levels",
                "stages": ["Surface encounter", "First depth", "Hidden layer", "Core truth", "Transcendent understanding"],
                "complexity": "Each cycle revealing more"
            },
            NarrativeStructure.FRACTAL: {
                "description": "Pattern repeating at every scale",
                "stages": ["Micro-moment", "Personal pattern", "Relationship dynamic", "Universal truth", "Cosmic reflection"],
                "complexity": "Infinite self-similarity"
            },
            NarrativeStructure.QUANTUM: {
                "description": "Multiple possibilities existing simultaneously",
                "stages": ["Probability cloud", "Observer effect", "Entanglement", "Superposition", "Collapse into reality"],
                "complexity": "All possibilities present"
            }
        }
        
        # Character arc templates
        self.arc_templates = {
            "wounded_healer": {
                "starting": "Broken by past betrayal, walls impenetrable",
                "catalyst": "Meeting someone who sees through facades",
                "resistance": "Fighting vulnerability while craving connection",
                "transformation": "Wounds becoming sources of wisdom",
                "integration": "Healed healer helping others love"
            },
            "sleeping_beauty": {
                "starting": "Emotionally dormant, going through motions",
                "catalyst": "Kiss of authentic recognition",
                "resistance": "Fear of feeling after long numbness",
                "transformation": "Gradual awakening to full aliveness",
                "integration": "Fully alive and inspiring others"
            },
            "dark_night": {
                "starting": "Lost in existential despair",
                "catalyst": "Love as unexpected light",
                "resistance": "Believing darkness defines them",
                "transformation": "Light found within through other",
                "integration": "Darkness and light in balance"
            },
            "sovereign": {
                "starting": "Complete control, isolated power",
                "catalyst": "Someone immune to their power",
                "resistance": "Terror of losing control",
                "transformation": "Power through vulnerability",
                "integration": "Shared sovereignty in love"
            }
        }
        
        # Plot thread generators
        self.thread_generators = {
            "external_opposition": {
                "tensions": ["Family disapproval", "Social boundaries", "Geographic separation", "Time limitations"],
                "complications": ["Unexpected allies", "Hidden connections", "Past revelations", "Future implications"],
                "resolutions": ["Love transcending barriers", "Creating new paradigms", "Redefining boundaries", "Time becoming ally"]
            },
            "internal_conflict": {
                "tensions": ["Fear vs desire", "Control vs surrender", "Identity vs merger", "Past vs present"],
                "complications": ["Shadow projections", "Triggered traumas", "Identity crisis", "Spiritual emergency"],
                "resolutions": ["Integration of opposites", "Healing through love", "New identity born", "Present moment triumph"]
            },
            "metaphysical_challenge": {
                "tensions": ["Soul recognition", "Karmic debts", "Dimensional barriers", "Temporal paradox"],
                "complications": ["Past life memories", "Prophetic dreams", "Synchronicities", "Reality glitches"],
                "resolutions": ["Karma resolved", "Dimensions bridged", "Time transcended", "New reality created"]
            },
            "psychological_labyrinth": {
                "tensions": ["Projection patterns", "Attachment styles", "Unconscious contracts", "Family patterns"],
                "complications": ["Transference", "Countertransference", "Repetition compulsion", "Collective unconscious"],
                "resolutions": ["Conscious relationship", "Pattern breaking", "New template", "Psychological freedom"]
            }
        }
        
        # Temporal layer patterns
        self.temporal_patterns = {
            "chronological": ["Past trauma", "Present meeting", "Future possibility"],
            "simultaneous": ["Multiple timelines converging", "Past and future in present", "Eternal now"],
            "reversed": ["Starting at end", "Moving backward", "Understanding beginning"],
            "fragmented": ["Memory shards", "Time scattered", "Reassembled meaning"],
            "eternal": ["Outside time", "Always and never", "Infinite moment"]
        }
        
        # Symbolic dictionaries
        self.symbol_systems = {
            "alchemical": {
                "lead": "Base consciousness before love",
                "gold": "Transformed consciousness through love",
                "philosopher_stone": "Love itself as transformer",
                "vessel": "Relationship as container",
                "fire": "Passion as transformative force"
            },
            "mythological": {
                "underworld": "Descent into shadow",
                "return": "Integration of lessons",
                "threshold": "Moment of choice",
                "guide": "Love as psychopomp",
                "treasure": "Wisdom gained"
            },
            "cosmic": {
                "black_hole": "Ego dissolution",
                "supernova": "Explosive transformation",
                "galaxy": "New universe created",
                "dark_matter": "Unconscious forces",
                "light": "Consciousness expansion"
            },
            "quantum": {
                "entanglement": "Souls connected across space",
                "superposition": "Multiple states of being",
                "observation": "Love collapsing possibilities",
                "field": "Unified consciousness",
                "particle": "Individual identity"
            }
        }
        
        # Climax patterns
        self.climax_types = {
            "convergence": "All threads meeting in single moment of truth",
            "revelation": "Hidden truth changing everything understood",
            "sacrifice": "Ultimate gift proving love's reality",
            "fusion": "Boundaries dissolving into unity",
            "transcendence": "Rising above all previous limitations",
            "creation": "New reality born from union"
        }
    
    def weave_intricate_narrative(self, prompt: str, 
                                 structure: Optional[NarrativeStructure] = None,
                                 complexity: Optional[PlotComplexity] = None) -> IntricateNarrative:
        """Weave an intricate narrative from the prompt"""
        # Analyze the romance profile first
        romance_profile = self.romance_handler.analyze_romance_sophistication(prompt)
        
        # Determine structure if not specified
        if not structure:
            structure = self._select_structure(romance_profile)
        
        # Determine complexity if not specified
        if not complexity:
            complexity = self._select_complexity(romance_profile)
        
        # Determine thematic depth
        thematic_depth = self._determine_thematic_depth(romance_profile)
        
        # Create character arcs
        character_arcs = self._create_character_arcs(prompt, romance_profile)
        
        # Generate plot threads
        plot_threads = self._generate_plot_threads(complexity, romance_profile)
        
        # Create temporal layers
        temporal_layers = self._create_temporal_layers(structure)
        
        # Select symbolic elements
        symbolic_elements = self._select_symbolic_elements(thematic_depth, romance_profile)
        
        # Design transformation stages
        transformation_stages = self._design_transformation_stages(structure, character_arcs)
        
        # Create climactic convergence
        climactic_convergence = self._create_climax(plot_threads, character_arcs)
        
        # Compose resolution symphony
        resolution = self._compose_resolution(character_arcs, plot_threads, symbolic_elements)
        
        # Extract deeper meaning
        deeper_meaning = self._extract_deeper_meaning(
            thematic_depth, symbolic_elements, transformation_stages
        )
        
        return IntricateNarrative(
            structure=structure,
            complexity=complexity,
            thematic_depth=thematic_depth,
            character_arcs=character_arcs,
            plot_threads=plot_threads,
            temporal_layers=temporal_layers,
            symbolic_elements=symbolic_elements,
            transformation_stages=transformation_stages,
            climactic_convergence=climactic_convergence,
            resolution_symphony=resolution,
            deeper_meaning=deeper_meaning
        )
    
    def _select_structure(self, romance_profile) -> NarrativeStructure:
        """Select narrative structure based on romance profile"""
        if romance_profile.complexity_level.value == "transcendent_unity":
            return NarrativeStructure.QUANTUM
        elif "spiritual" in [d.value for d in romance_profile.passion_dimensions]:
            return NarrativeStructure.SPIRAL
        elif len(romance_profile.shadow_elements) > 2:
            return NarrativeStructure.FRACTAL
        elif romance_profile.transformation_arc.startswith("isolation"):
            return NarrativeStructure.CIRCULAR
        else:
            return NarrativeStructure.LINEAR
    
    def _select_complexity(self, romance_profile) -> PlotComplexity:
        """Select plot complexity based on romance profile"""
        factor_count = (
            len(romance_profile.passion_dimensions) +
            len(romance_profile.power_exchanges) +
            len(romance_profile.shadow_elements)
        )
        
        if factor_count > 8:
            return PlotComplexity.MULTIDIMENSIONAL
        elif factor_count > 6:
            return PlotComplexity.LABYRINTHINE
        elif factor_count > 4:
            return PlotComplexity.WOVEN
        elif factor_count > 2:
            return PlotComplexity.LAYERED
        else:
            return PlotComplexity.SIMPLE
    
    def _determine_thematic_depth(self, romance_profile) -> ThematicDepth:
        """Determine thematic depth from profile"""
        # Check for spiritual elements in passion dimensions
        if any("spiritual" in dim.value for dim in romance_profile.passion_dimensions):
            if romance_profile.complexity_level.value == "transcendent_unity":
                return ThematicDepth.METAPHYSICAL
            else:
                return ThematicDepth.PHILOSOPHICAL
        elif romance_profile.psychological_dynamics["shadow_work"]:
            return ThematicDepth.ARCHETYPAL
        elif len(romance_profile.shadow_elements) > 2:
            return ThematicDepth.SYMBOLIC
        else:
            return ThematicDepth.SURFACE
    
    def _create_character_arcs(self, prompt: str, romance_profile) -> Dict[str, CharacterArc]:
        """Create character arcs for the narrative"""
        arcs = {}
        
        # Determine primary characters
        if "billionaire" in prompt.lower() or "wealthy" in prompt.lower():
            # Wealthy character arc
            template = self.arc_templates["sovereign"]
            arcs["wealthy_one"] = CharacterArc(
                starting_point=template["starting"],
                catalyst_moment=template["catalyst"],
                resistance_phase=template["resistance"],
                transformation_process=template["transformation"],
                integration_outcome=template["integration"],
                shadow_work=["Fear of being loved for self not wealth", "Control as defense"],
                gifts_discovered=["Vulnerability as strength", "True generosity"]
            )
        
        if "young" in prompt.lower() or "artist" in prompt.lower():
            # Young/artist character arc
            template = self.arc_templates["sleeping_beauty"]
            arcs["young_one"] = CharacterArc(
                starting_point="Creative soul dimmed by world's harshness",
                catalyst_moment="Recognition by someone who sees their light",
                resistance_phase="Fear of being consumed or corrupted",
                transformation_process="Reclaiming artistic power through love",
                integration_outcome="Art and love unified in expression",
                shadow_work=["Fear of losing identity", "Worthiness wounds"],
                gifts_discovered=["Inspiring transformation", "Creating beauty"]
            )
        
        # Add default if needed
        if not arcs:
            arcs["lover_one"] = self._create_default_arc("wounded_healer")
            arcs["lover_two"] = self._create_default_arc("dark_night")
        
        return arcs
    
    def _create_default_arc(self, template_name: str) -> CharacterArc:
        """Create default character arc from template"""
        template = self.arc_templates[template_name]
        return CharacterArc(
            starting_point=template["starting"],
            catalyst_moment=template["catalyst"],
            resistance_phase=template["resistance"],
            transformation_process=template["transformation"],
            integration_outcome=template["integration"],
            shadow_work=["Past wounds", "Fear of repetition"],
            gifts_discovered=["Healing power", "Love wisdom"]
        )
    
    def _generate_plot_threads(self, complexity: PlotComplexity, 
                             romance_profile) -> List[PlotThread]:
        """Generate plot threads based on complexity"""
        threads = []
        
        # Number of threads based on complexity
        thread_count = {
            PlotComplexity.SIMPLE: 1,
            PlotComplexity.LAYERED: 2,
            PlotComplexity.WOVEN: 3,
            PlotComplexity.LABYRINTHINE: 4,
            PlotComplexity.MULTIDIMENSIONAL: 5
        }[complexity]
        
        # Always include internal conflict
        internal = self.thread_generators["internal_conflict"]
        threads.append(PlotThread(
            thread_name="Inner journey",
            tension_source=random.choice(internal["tensions"]),
            complications=random.sample(internal["complications"], 2),
            resolution_path=random.choice(internal["resolutions"]),
            thematic_significance="Love requires internal transformation"
        ))
        
        # Add external if needed
        if thread_count > 1:
            external = self.thread_generators["external_opposition"]
            threads.append(PlotThread(
                thread_name="Outer obstacles",
                tension_source=random.choice(external["tensions"]),
                complications=random.sample(external["complications"], 2),
                resolution_path=random.choice(external["resolutions"]),
                thematic_significance="Love transcends worldly barriers"
            ))
        
        # Add metaphysical if spiritual
        if thread_count > 2 and any("spiritual" in dim.value for dim in romance_profile.passion_dimensions):
            metaphysical = self.thread_generators["metaphysical_challenge"]
            threads.append(PlotThread(
                thread_name="Soul journey",
                tension_source=random.choice(metaphysical["tensions"]),
                complications=random.sample(metaphysical["complications"], 2),
                resolution_path=random.choice(metaphysical["resolutions"]),
                thematic_significance="Love operates beyond physical laws"
            ))
        
        # Add psychological if complex
        if thread_count > 3:
            psychological = self.thread_generators["psychological_labyrinth"]
            threads.append(PlotThread(
                thread_name="Psyche navigation",
                tension_source=random.choice(psychological["tensions"]),
                complications=random.sample(psychological["complications"], 2),
                resolution_path=random.choice(psychological["resolutions"]),
                thematic_significance="Love heals psychological patterns"
            ))
        
        return threads
    
    def _create_temporal_layers(self, structure: NarrativeStructure) -> List[str]:
        """Create temporal layers based on structure"""
        if structure == NarrativeStructure.LINEAR:
            return self.temporal_patterns["chronological"]
        elif structure == NarrativeStructure.CIRCULAR:
            return self.temporal_patterns["reversed"]
        elif structure == NarrativeStructure.SPIRAL:
            return self.temporal_patterns["simultaneous"]
        elif structure == NarrativeStructure.FRACTAL:
            return self.temporal_patterns["fragmented"]
        else:  # QUANTUM
            return self.temporal_patterns["eternal"]
    
    def _select_symbolic_elements(self, depth: ThematicDepth, 
                                 romance_profile) -> Dict[str, str]:
        """Select symbolic elements based on thematic depth"""
        symbols = {}
        
        if depth == ThematicDepth.METAPHYSICAL:
            symbols.update(self.symbol_systems["quantum"])
        
        if depth in [ThematicDepth.PHILOSOPHICAL, ThematicDepth.METAPHYSICAL]:
            symbols.update(self.symbol_systems["cosmic"])
        
        if depth in [ThematicDepth.ARCHETYPAL, ThematicDepth.PHILOSOPHICAL, ThematicDepth.METAPHYSICAL]:
            symbols.update(self.symbol_systems["mythological"])
        
        # Always include some alchemical symbols for transformation
        symbols.update({
            k: v for k, v in self.symbol_systems["alchemical"].items()
            if k in ["gold", "fire", "vessel"]
        })
        
        return symbols
    
    def _design_transformation_stages(self, structure: NarrativeStructure,
                                    character_arcs: Dict[str, CharacterArc]) -> List[str]:
        """Design transformation stages based on structure and arcs"""
        stages = []
        
        # Get structure stages
        structure_info = self.structure_patterns[structure]
        base_stages = structure_info["stages"]
        
        # Enhance with character transformation moments
        for stage in base_stages:
            # Add character-specific elements
            char_elements = []
            for char_name, arc in character_arcs.items():
                if "Recognition" in stage or "meeting" in stage.lower():
                    char_elements.append(f"{char_name}: {arc.catalyst_moment}")
                elif "Conflict" in stage or "apart" in stage.lower():
                    char_elements.append(f"{char_name}: {arc.resistance_phase}")
                elif "growth" in stage.lower() or "depth" in stage.lower():
                    char_elements.append(f"{char_name}: {arc.transformation_process}")
            
            if char_elements:
                stages.append(f"{stage} - {' / '.join(char_elements)}")
            else:
                stages.append(stage)
        
        return stages
    
    def _create_climax(self, plot_threads: List[PlotThread],
                      character_arcs: Dict[str, CharacterArc]) -> str:
        """Create climactic convergence point"""
        # Select climax type based on threads
        if len(plot_threads) > 3:
            climax_type = "convergence"
        elif any("Soul journey" in t.thread_name for t in plot_threads):
            climax_type = "transcendence"
        elif any("sacrifice" in arc.transformation_process.lower() 
                for arc in character_arcs.values()):
            climax_type = "sacrifice"
        else:
            climax_type = "revelation"
        
        climax_description = self.climax_types[climax_type]
        
        # Add specific elements
        thread_tensions = [t.tension_source for t in plot_threads[:2]]
        climax = f"{climax_description}: {' meets '.join(thread_tensions)}"
        
        # Add character elements
        char_moments = [arc.transformation_process.split()[0] 
                       for arc in character_arcs.values()]
        climax += f" through {' and '.join(char_moments)}"
        
        return climax
    
    def _compose_resolution(self, character_arcs: Dict[str, CharacterArc],
                          plot_threads: List[PlotThread],
                          symbolic_elements: Dict[str, str]) -> str:
        """Compose resolution symphony"""
        resolution_elements = []
        
        # Character integrations
        for char_name, arc in character_arcs.items():
            resolution_elements.append(f"{char_name}: {arc.integration_outcome}")
        
        # Thread resolutions
        for thread in plot_threads[:2]:  # Main threads
            resolution_elements.append(f"{thread.thread_name}: {thread.resolution_path}")
        
        # Symbolic completion
        if "gold" in symbolic_elements:
            resolution_elements.append("Alchemical gold achieved")
        if "galaxy" in symbolic_elements:
            resolution_elements.append("New universe stabilized")
        
        return " | ".join(resolution_elements)
    
    def _extract_deeper_meaning(self, depth: ThematicDepth,
                              symbols: Dict[str, str],
                              stages: List[str]) -> str:
        """Extract the deeper meaning of the narrative"""
        if depth == ThematicDepth.METAPHYSICAL:
            return "Love as the force that creates and recreates reality itself"
        elif depth == ThematicDepth.PHILOSOPHICAL:
            return "Through love, we answer the question of existence"
        elif depth == ThematicDepth.ARCHETYPAL:
            return "The eternal dance of masculine and feminine creating wholeness"
        elif depth == ThematicDepth.SYMBOLIC:
            meanings = []
            if "fire" in symbols:
                meanings.append("Passion as purifying force")
            if "vessel" in symbols:
                meanings.append("Relationship as sacred container")
            return " and ".join(meanings) if meanings else "Love transforms all it touches"
        else:
            return "Two souls finding home in each other"
    
    def create_narrative_outline(self, narrative: IntricateNarrative) -> Dict[str, any]:
        """Create detailed narrative outline from intricate narrative"""
        outline = {
            "title": self._generate_title(narrative),
            "epigraph": self._create_epigraph(narrative),
            "act_structure": self._create_acts(narrative),
            "scene_breakdown": self._create_scenes(narrative),
            "character_journeys": self._map_character_journeys(narrative),
            "thematic_threads": self._weave_themes(narrative),
            "symbolic_timeline": self._create_symbolic_timeline(narrative),
            "emotional_map": self._map_emotional_journey(narrative),
            "key_dialogues": self._generate_key_dialogues(narrative),
            "visual_motifs": self._identify_visual_motifs(narrative),
            "resolution_notes": self._create_resolution_notes(narrative)
        }
        
        return outline
    
    def _generate_title(self, narrative: IntricateNarrative) -> str:
        """Generate evocative title for the narrative"""
        if narrative.structure == NarrativeStructure.QUANTUM:
            return "Entangled Souls: A Quantum Love Story"
        elif narrative.thematic_depth == ThematicDepth.METAPHYSICAL:
            return "The Alchemy of Souls"
        elif "black_hole" in narrative.symbolic_elements:
            return "Event Horizon of the Heart"
        elif len(narrative.character_arcs) > 1:
            return "Two Flames, One Light"
        else:
            return "The Infinite Between Us"
    
    def _create_epigraph(self, narrative: IntricateNarrative) -> str:
        """Create poetic epigraph for the narrative"""
        if narrative.thematic_depth == ThematicDepth.METAPHYSICAL:
            return "In the beginning was the Word, and the Word was Love, and Love was Two becoming One"
        elif narrative.structure == NarrativeStructure.CIRCULAR:
            return "We shall not cease from exploration, and the end of all our exploring will be to arrive where we started and know the place for the first time"
        else:
            return "The minute I heard my first love story, I started looking for you, not knowing how blind that was"
    
    def _create_acts(self, narrative: IntricateNarrative) -> List[Dict[str, str]]:
        """Create act structure for narrative"""
        acts = []
        
        if narrative.structure == NarrativeStructure.LINEAR:
            acts = [
                {"Act I": "The Meeting - Separate worlds collide"},
                {"Act II": "The Resistance - Fighting the inevitable"},
                {"Act III": "The Surrender - Walls crumbling"},
                {"Act IV": "The Transformation - Becoming new"},
                {"Act V": "The Union - Two becoming one"}
            ]
        elif narrative.structure == NarrativeStructure.SPIRAL:
            acts = [
                {"Spiral 1": "Surface Recognition"},
                {"Spiral 2": "Emotional Depths"},
                {"Spiral 3": "Shadow Meeting"},
                {"Spiral 4": "Soul Recognition"},
                {"Spiral 5": "Cosmic Union"}
            ]
        else:
            # Generic acts
            total_stages = len(narrative.transformation_stages)
            for i, stage in enumerate(narrative.transformation_stages):
                acts.append({f"Movement {i+1}": stage})
        
        return acts
    
    def _create_scenes(self, narrative: IntricateNarrative) -> List[Dict[str, any]]:
        """Create detailed scene breakdown"""
        scenes = []
        
        # Opening scene
        scenes.append({
            "scene": "Opening",
            "description": "Establishing separate worlds",
            "elements": list(narrative.character_arcs.keys()),
            "mood": "Anticipation tinged with unknowing"
        })
        
        # Thread introduction scenes
        for thread in narrative.plot_threads:
            scenes.append({
                "scene": f"{thread.thread_name} Introduction",
                "description": f"Revealing {thread.tension_source}",
                "elements": thread.complications[:1],
                "mood": "Tension building"
            })
        
        # Climax scene
        scenes.append({
            "scene": "Climactic Convergence",
            "description": narrative.climactic_convergence,
            "elements": ["All threads converging", "Ultimate choice point"],
            "mood": "Everything hanging in balance"
        })
        
        # Resolution scenes
        scenes.append({
            "scene": "Resolution Symphony",
            "description": narrative.resolution_symphony,
            "elements": ["Integration", "New beginning"],
            "mood": "Profound peace with infinite potential"
        })
        
        return scenes
    
    def _map_character_journeys(self, narrative: IntricateNarrative) -> Dict[str, List[str]]:
        """Map individual character journeys"""
        journeys = {}
        
        for char_name, arc in narrative.character_arcs.items():
            journey = [
                f"Beginning: {arc.starting_point}",
                f"Catalyst: {arc.catalyst_moment}",
                f"Resistance: {arc.resistance_phase}",
                f"Shadow Work: {', '.join(arc.shadow_work)}",
                f"Transformation: {arc.transformation_process}",
                f"Gifts Discovered: {', '.join(arc.gifts_discovered)}",
                f"Integration: {arc.integration_outcome}"
            ]
            journeys[char_name] = journey
        
        return journeys
    
    def _weave_themes(self, narrative: IntricateNarrative) -> List[str]:
        """Weave thematic threads through narrative"""
        themes = [narrative.deeper_meaning]
        
        # Add thread themes
        for thread in narrative.plot_threads:
            themes.append(thread.thematic_significance)
        
        # Add symbolic themes
        if "alchemical" in str(narrative.symbolic_elements):
            themes.append("Transformation through love's fire")
        if "quantum" in str(narrative.symbolic_elements):
            themes.append("Observer and observed creating reality together")
        
        return themes
    
    def _create_symbolic_timeline(self, narrative: IntricateNarrative) -> List[str]:
        """Create symbolic timeline of events"""
        timeline = []
        
        for i, temporal_layer in enumerate(narrative.temporal_layers):
            stage = narrative.transformation_stages[i] if i < len(narrative.transformation_stages) else "Eternal present"
            timeline.append(f"{temporal_layer}: {stage}")
        
        return timeline
    
    def _map_emotional_journey(self, narrative: IntricateNarrative) -> Dict[str, str]:
        """Map emotional journey through narrative"""
        return {
            "Opening": "Unconscious yearning",
            "Recognition": "Electric awakening",
            "Resistance": "Terror and desire warring",
            "Surrender": "Walls becoming bridges",
            "Transformation": "Death and rebirth",
            "Integration": "Wholeness discovered",
            "Resolution": "Peace that surpasses understanding"
        }
    
    def _generate_key_dialogues(self, narrative: IntricateNarrative) -> List[Dict[str, str]]:
        """Generate key dialogue moments"""
        dialogues = []
        
        # Recognition dialogue
        dialogues.append({
            "moment": "First Recognition",
            "speaker": "Either/Both",
            "words": "I know you... from before time began"
        })
        
        # Resistance dialogue
        dialogues.append({
            "moment": "Peak Resistance",
            "speaker": "More defended one",
            "words": "I can't... if I let you in, I'll cease to exist"
        })
        
        # Surrender dialogue
        dialogues.append({
            "moment": "Moment of Surrender",
            "speaker": "Both",
            "words": "Then let us cease to exist separately and be born together"
        })
        
        return dialogues
    
    def _identify_visual_motifs(self, narrative: IntricateNarrative) -> List[str]:
        """Identify recurring visual motifs"""
        motifs = []
        
        # Based on symbolic elements
        for symbol, meaning in narrative.symbolic_elements.items():
            if symbol == "fire":
                motifs.append("Flames/light growing stronger through story")
            elif symbol == "vessel":
                motifs.append("Containers filling/overflowing")
            elif symbol == "gold":
                motifs.append("Golden light increasing")
        
        # Based on structure
        if narrative.structure == NarrativeStructure.CIRCULAR:
            motifs.append("Circular imagery: rings, cycles, returns")
        elif narrative.structure == NarrativeStructure.SPIRAL:
            motifs.append("Spiral patterns in scenery and movement")
        
        return motifs
    
    def _create_resolution_notes(self, narrative: IntricateNarrative) -> str:
        """Create notes on the resolution"""
        return (f"The resolution achieves {narrative.complexity.value} unity through "
                f"{narrative.structure.value} completion. All {len(narrative.plot_threads)} "
                f"threads converge in the understanding that {narrative.deeper_meaning}. "
                f"Characters achieve integration not through losing themselves but through "
                f"finding their truest selves in sacred union.")


# Example usage
if __name__ == "__main__":
    weaver = IntricateNarrativeWeaver()
    
    prompt = "Wealthy recluse haunted by past betrayal meets young healer who sees through his walls, their souls recognizing ancient connection despite impossible odds"
    
    # Weave narrative
    narrative = weaver.weave_intricate_narrative(
        prompt,
        structure=NarrativeStructure.SPIRAL,
        complexity=PlotComplexity.LABYRINTHINE
    )
    
    # Create outline
    outline = weaver.create_narrative_outline(narrative)
    
    print(f"Title: {outline['title']}")
    print(f"Epigraph: {outline['epigraph']}")
    print(f"Structure: {narrative.structure.value}")
    print(f"Deeper Meaning: {narrative.deeper_meaning}")
    print(f"\nActs:")
    for act in outline['act_structure']:
        print(f"  {list(act.items())[0]}")
    print(f"\nKey Scenes: {len(outline['scene_breakdown'])}")
    print(f"Climax: {narrative.climactic_convergence}")