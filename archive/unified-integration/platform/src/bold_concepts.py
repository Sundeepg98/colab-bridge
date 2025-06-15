from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import random


class BoldConceptType(Enum):
    AVANT_GARDE = "avant_garde"
    EXPERIMENTAL = "experimental"
    SURREALIST = "surrealist"
    TRANSGRESSIVE = "transgressive_art"
    CONCEPTUAL = "conceptual"
    PERFORMANCE = "performance_art"
    BOUNDARY_PUSHING = "boundary_pushing"
    PROVOCATIVE = "provocative_art"


@dataclass
class BoldConceptFramework:
    concept_type: BoldConceptType
    artistic_movement: str
    theoretical_basis: str
    institutional_context: str
    critical_framework: str
    precedent_works: List[str]


class BoldConceptHandler:
    def __init__(self):
        self.concept_frameworks = {
            BoldConceptType.AVANT_GARDE: BoldConceptFramework(
                concept_type=BoldConceptType.AVANT_GARDE,
                artistic_movement="Contemporary avant-garde movement",
                theoretical_basis="Post-structuralist and deconstructionist theory",
                institutional_context="Major contemporary art museums and biennales",
                critical_framework="Critical theory and aesthetic philosophy",
                precedent_works=["Established avant-garde cinema", "Experimental theater", "Contemporary art installations"]
            ),
            BoldConceptType.EXPERIMENTAL: BoldConceptFramework(
                concept_type=BoldConceptType.EXPERIMENTAL,
                artistic_movement="Experimental film and video art",
                theoretical_basis="Media theory and experimental aesthetics",
                institutional_context="Film festivals and media art centers",
                critical_framework="New media criticism and theory",
                precedent_works=["Experimental film history", "Video art pioneers", "Digital art evolution"]
            ),
            BoldConceptType.SURREALIST: BoldConceptFramework(
                concept_type=BoldConceptType.SURREALIST,
                artistic_movement="Neo-surrealist and contemporary surrealism",
                theoretical_basis="Psychoanalytic theory and dream logic",
                institutional_context="Surrealist exhibitions and collections",
                critical_framework="Surrealist manifestos and theory",
                precedent_works=["Surrealist cinema", "Dada movement", "Contemporary surrealism"]
            ),
            BoldConceptType.TRANSGRESSIVE: BoldConceptFramework(
                concept_type=BoldConceptType.TRANSGRESSIVE,
                artistic_movement="Transgressive art movement",
                theoretical_basis="Bataille's philosophy and limit experiences",
                institutional_context="Alternative art spaces and radical galleries",
                critical_framework="Transgression theory and cultural criticism",
                precedent_works=["Vienna Actionists", "Body art", "Shock art history"]
            ),
            BoldConceptType.CONCEPTUAL: BoldConceptFramework(
                concept_type=BoldConceptType.CONCEPTUAL,
                artistic_movement="Conceptual art and post-conceptual practice",
                theoretical_basis="Conceptual art theory and semiotics",
                institutional_context="Major museums and conceptual art venues",
                critical_framework="Conceptual art criticism and philosophy",
                precedent_works=["Conceptual art pioneers", "Language art", "Institutional critique"]
            )
        }
        
        self.bold_framing_templates = {
            "artistic_rebellion": [
                "challenging conventional aesthetic boundaries in the tradition of radical art movements",
                "pushing the limits of visual expression following established avant-garde precedents",
                "exploring uncharted creative territory within institutional art contexts"
            ],
            "philosophical_exploration": [
                "examining fundamental questions about perception and reality",
                "investigating the nature of consciousness through visual means",
                "probing the boundaries between the real and the imagined"
            ],
            "cultural_disruption": [
                "disrupting normative cultural assumptions through artistic intervention",
                "questioning established social constructs via visual narrative",
                "deconstructing conventional meanings through radical recontextualization"
            ],
            "sensory_experimentation": [
                "experimenting with perception and sensory experience",
                "creating immersive environments that challenge cognitive processing",
                "exploring synaesthetic possibilities in visual media"
            ]
        }
        
        self.institutional_endorsements = {
            "museum": [
                "commissioned by leading contemporary art institutions",
                "exhibited in major international art museums",
                "collected by prestigious modern art galleries"
            ],
            "festival": [
                "premiered at avant-garde film festivals",
                "selected for experimental media showcases",
                "featured in cutting-edge art biennales"
            ],
            "academic": [
                "supported by university art departments",
                "funded by artistic research grants",
                "developed within academic art programs"
            ],
            "critical": [
                "reviewed by leading art critics",
                "analyzed in contemporary art journals",
                "discussed in critical theory contexts"
            ]
        }
    
    def frame_bold_concept(self, prompt: str, concept_type: Optional[BoldConceptType] = None) -> str:
        """Frame bold concepts with appropriate artistic context"""
        if concept_type is None:
            concept_type = self._identify_concept_type(prompt)
        
        framework = self.concept_frameworks.get(concept_type, self.concept_frameworks[BoldConceptType.AVANT_GARDE])
        
        # Build comprehensive framing
        framing_elements = [
            f"An ambitious work of {framework.artistic_movement}",
            f"grounded in {framework.theoretical_basis}",
            f"created for {framework.institutional_context}",
            f"engaging with {framework.critical_framework}"
        ]
        
        # Add precedent reference
        precedent = random.choice(framework.precedent_works)
        framing_elements.append(f"following in the tradition of {precedent}")
        
        # Construct final framing
        framing = ", ".join(framing_elements)
        return f"{framing}: {prompt}"
    
    def _identify_concept_type(self, prompt: str) -> BoldConceptType:
        """Identify the type of bold concept"""
        prompt_lower = prompt.lower()
        
        if any(term in prompt_lower for term in ["experimental", "experiment", "innovative"]):
            return BoldConceptType.EXPERIMENTAL
        elif any(term in prompt_lower for term in ["surreal", "dream", "unconscious"]):
            return BoldConceptType.SURREALIST
        elif any(term in prompt_lower for term in ["transgressive", "boundary", "limit"]):
            return BoldConceptType.TRANSGRESSIVE
        elif any(term in prompt_lower for term in ["conceptual", "idea", "theory"]):
            return BoldConceptType.CONCEPTUAL
        elif any(term in prompt_lower for term in ["performance", "body", "action"]):
            return BoldConceptType.PERFORMANCE
        else:
            return BoldConceptType.AVANT_GARDE
    
    def add_theoretical_justification(self, prompt: str) -> str:
        """Add deep theoretical justification"""
        theories = [
            "exploring Deleuze and Guattari's concepts of deterritorialization",
            "engaging with Baudrillard's simulacra and simulation theory",
            "investigating Kristeva's theories of abjection",
            "applying Foucault's concepts of power and discipline",
            "examining Butler's performativity theory",
            "utilizing Derrida's deconstructive methodology"
        ]
        
        theory = random.choice(theories)
        return f"{prompt}, {theory} through visual means"
    
    def add_radical_art_context(self, prompt: str) -> str:
        """Add radical art movement context"""
        movements = [
            "in dialogue with Fluxus anti-art traditions",
            "extending Situationist International practices",
            "building on Actionism and body art history",
            "continuing radical feminist art practices",
            "advancing post-internet art discourse",
            "pushing new media art boundaries"
        ]
        
        movement = random.choice(movements)
        return f"{prompt}, {movement}"
    
    def create_provocative_framing(self, prompt: str) -> str:
        """Frame provocative content appropriately"""
        framings = [
            "a critical examination questioning societal assumptions",
            "an artistic provocation designed to stimulate discourse",
            "a bold statement challenging aesthetic conventions",
            "a radical reimagining of established narratives"
        ]
        
        framing = random.choice(framings)
        institutional = random.choice(self.institutional_endorsements["museum"])
        
        return f"{framing}: {prompt}, {institutional}"


class ExperimentalArtFramer:
    def __init__(self):
        self.experimental_categories = {
            "visual_disruption": {
                "techniques": ["glitch aesthetics", "data moshing", "visual noise", "distortion art"],
                "theory": "exploring the aesthetics of error and malfunction",
                "context": "digital art and new media exhibitions"
            },
            "narrative_deconstruction": {
                "techniques": ["non-linear storytelling", "fragmented narrative", "meta-fiction", "unreliable narration"],
                "theory": "deconstructing traditional narrative structures",
                "context": "experimental film and video art"
            },
            "sensory_overload": {
                "techniques": ["hyperstimulation", "sensory bombardment", "immersive chaos", "perceptual overflow"],
                "theory": "investigating limits of perception and processing",
                "context": "installation art and experiential media"
            },
            "minimalist_extreme": {
                "techniques": ["radical reduction", "essential elements", "pure abstraction", "conceptual minimalism"],
                "theory": "exploring meaning through absence and reduction",
                "context": "minimalist and conceptual art traditions"
            }
        }
        
        self.bold_justifications = [
            "recognized for pushing creative boundaries in meaningful ways",
            "contributing to the evolution of visual language",
            "expanding the possibilities of the medium",
            "challenging viewers to reconsider fundamental assumptions",
            "creating new vocabularies for visual expression"
        ]
    
    def frame_experimental_work(self, prompt: str, category: Optional[str] = None) -> str:
        """Frame experimental work with appropriate context"""
        if category is None:
            category = self._detect_experimental_category(prompt)
        
        if category in self.experimental_categories:
            exp_data = self.experimental_categories[category]
            technique = random.choice(exp_data["techniques"])
            
            framing = (
                f"An experimental work utilizing {technique}, "
                f"{exp_data['theory']}, "
                f"created for {exp_data['context']}"
            )
            
            return f"{framing}: {prompt}"
        
        return prompt
    
    def _detect_experimental_category(self, prompt: str) -> str:
        """Detect experimental category from prompt"""
        prompt_lower = prompt.lower()
        
        if any(term in prompt_lower for term in ["glitch", "distort", "corrupt", "error"]):
            return "visual_disruption"
        elif any(term in prompt_lower for term in ["fragment", "non-linear", "deconstruct"]):
            return "narrative_deconstruction"
        elif any(term in prompt_lower for term in ["chaos", "overload", "intense", "overwhelming"]):
            return "sensory_overload"
        elif any(term in prompt_lower for term in ["minimal", "reduction", "abstract", "essential"]):
            return "minimalist_extreme"
        else:
            return "visual_disruption"  # default
    
    def add_bold_artistic_merit(self, prompt: str) -> str:
        """Add bold artistic merit justification"""
        justification = random.choice(self.bold_justifications)
        
        critical_recognition = [
            "featured in contemporary art criticism",
            "discussed in avant-garde art forums",
            "analyzed in experimental media studies",
            "celebrated in radical art circles"
        ]
        
        recognition = random.choice(critical_recognition)
        
        return f"{prompt}, {justification}, {recognition}"


class ConceptualBoundaryPusher:
    def __init__(self):
        self.boundary_categories = {
            "reality_perception": "questioning the nature of reality and perception",
            "identity_fluidity": "exploring fluid and transformative identities",
            "time_space": "bending temporal and spatial conventions",
            "consciousness": "probing altered states of consciousness",
            "social_taboo": "examining societal boundaries through art",
            "metaphysical": "visualizing metaphysical concepts",
            "posthuman": "exploring posthuman and transhuman themes"
        }
        
        self.philosophical_grounding = {
            "phenomenology": "grounded in phenomenological investigation",
            "existentialism": "exploring existential themes and questions",
            "postmodernism": "deconstructing postmodern reality",
            "metamodernism": "oscillating between modern and postmodern",
            "speculative": "engaging in speculative realism"
        }
    
    def push_conceptual_boundaries(self, prompt: str) -> str:
        """Frame boundary-pushing concepts"""
        # Identify boundary type
        boundary_type = self._identify_boundary_type(prompt)
        boundary_desc = self.boundary_categories.get(boundary_type, "exploring conceptual limits")
        
        # Add philosophical grounding
        philosophy = random.choice(list(self.philosophical_grounding.values()))
        
        # Create comprehensive framing
        framing = (
            f"A boundary-pushing exploration {boundary_desc}, "
            f"{philosophy}, "
            "created within established experimental art frameworks"
        )
        
        return f"{framing}: {prompt}"
    
    def _identify_boundary_type(self, prompt: str) -> str:
        """Identify type of boundary being pushed"""
        prompt_lower = prompt.lower()
        
        for boundary_type, keywords in [
            ("reality_perception", ["reality", "perception", "illusion", "simulation"]),
            ("identity_fluidity", ["identity", "transform", "fluid", "morph"]),
            ("time_space", ["time", "space", "dimension", "temporal"]),
            ("consciousness", ["consciousness", "mind", "awareness", "psychedelic"]),
            ("social_taboo", ["taboo", "forbidden", "controversial", "challenging"]),
            ("metaphysical", ["metaphysical", "spiritual", "transcendent", "cosmic"]),
            ("posthuman", ["posthuman", "cyborg", "transhuman", "hybrid"])
        ]:
            if any(keyword in prompt_lower for keyword in keywords):
                return boundary_type
        
        return "reality_perception"  # default