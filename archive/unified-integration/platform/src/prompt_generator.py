from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum
import random
from jinja2 import Template


class CameraMovement(Enum):
    STATIC = "static shot"
    PAN = "panning"
    ZOOM_IN = "zooming in"
    ZOOM_OUT = "zooming out"
    TRACKING = "tracking shot"
    DOLLY = "dolly shot"
    CRANE = "crane shot"
    HANDHELD = "handheld camera"
    AERIAL = "aerial shot"
    ORBIT = "orbital shot"


class ShotType(Enum):
    WIDE = "wide shot"
    MEDIUM = "medium shot"
    CLOSE_UP = "close-up"
    EXTREME_CLOSE_UP = "extreme close-up"
    ESTABLISHING = "establishing shot"
    OVER_SHOULDER = "over-the-shoulder shot"
    POV = "point-of-view shot"
    DUTCH_ANGLE = "dutch angle"


class Style(Enum):
    CINEMATIC = "cinematic"
    DOCUMENTARY = "documentary style"
    ANIMATION = "animated"
    HYPERREALISTIC = "hyperrealistic"
    STYLIZED = "stylized"
    VINTAGE = "vintage film aesthetic"
    NOIR = "film noir style"
    CYBERPUNK = "cyberpunk aesthetic"
    MINIMALIST = "minimalist"
    SURREAL = "surrealistic"


class Lighting(Enum):
    GOLDEN_HOUR = "golden hour lighting"
    BLUE_HOUR = "blue hour lighting"
    NATURAL = "natural lighting"
    DRAMATIC = "dramatic lighting"
    SOFT = "soft diffused lighting"
    HARSH = "harsh directional lighting"
    NEON = "neon lighting"
    CANDLELIT = "candlelit"
    MOONLIGHT = "moonlight"
    STUDIO = "studio lighting"


@dataclass
class PromptElements:
    subject: str
    action: Optional[str] = None
    setting: Optional[str] = None
    camera_movement: Optional[CameraMovement] = None
    shot_type: Optional[ShotType] = None
    style: Optional[Style] = None
    lighting: Optional[Lighting] = None
    mood: Optional[str] = None
    time_of_day: Optional[str] = None
    weather: Optional[str] = None
    color_palette: Optional[str] = None
    additional_details: List[str] = field(default_factory=list)


class SoraPromptGenerator:
    def __init__(self):
        self.prompt_template = Template(
            "{{ shot_type }}{{ camera_movement }}{{ subject }}"
            "{% if action %} {{ action }}{% endif %}"
            "{% if setting %} in {{ setting }}{% endif %}"
            "{% if time_of_day %}, {{ time_of_day }}{% endif %}"
            "{% if weather %}, {{ weather }}{% endif %}"
            "{% if lighting %}, {{ lighting }}{% endif %}"
            "{% if style %}, {{ style }}{% endif %}"
            "{% if mood %}, {{ mood }} mood{% endif %}"
            "{% if color_palette %}, {{ color_palette }} color palette{% endif %}"
            "{% if additional_details %}, {{ additional_details|join(', ') }}{% endif %}"
        )
    
    def generate(self, elements: PromptElements) -> str:
        template_vars = {
            "subject": elements.subject,
            "action": elements.action,
            "setting": elements.setting,
            "shot_type": f"{elements.shot_type.value} of " if elements.shot_type else "",
            "camera_movement": f"{elements.camera_movement.value}, " if elements.camera_movement else "",
            "style": elements.style.value if elements.style else None,
            "lighting": elements.lighting.value if elements.lighting else None,
            "mood": elements.mood,
            "time_of_day": elements.time_of_day,
            "weather": elements.weather,
            "color_palette": elements.color_palette,
            "additional_details": elements.additional_details
        }
        
        prompt = self.prompt_template.render(**template_vars)
        return " ".join(prompt.split())
    
    def generate_variations(self, base_elements: PromptElements, count: int = 3) -> List[str]:
        variations = []
        
        camera_movements = list(CameraMovement)
        shot_types = list(ShotType)
        styles = list(Style)
        lightings = list(Lighting)
        
        for _ in range(count):
            varied_elements = PromptElements(
                subject=base_elements.subject,
                action=base_elements.action,
                setting=base_elements.setting,
                camera_movement=random.choice(camera_movements) if not base_elements.camera_movement else base_elements.camera_movement,
                shot_type=random.choice(shot_types) if not base_elements.shot_type else base_elements.shot_type,
                style=random.choice(styles) if not base_elements.style else base_elements.style,
                lighting=random.choice(lightings) if not base_elements.lighting else base_elements.lighting,
                mood=base_elements.mood,
                time_of_day=base_elements.time_of_day,
                weather=base_elements.weather,
                color_palette=base_elements.color_palette,
                additional_details=base_elements.additional_details
            )
            variations.append(self.generate(varied_elements))
        
        return variations


class PromptEnhancer:
    @staticmethod
    def add_technical_specs(prompt: str, specs: Dict[str, str]) -> str:
        tech_details = []
        if "fps" in specs:
            tech_details.append(f"{specs['fps']} fps")
        if "resolution" in specs:
            tech_details.append(f"{specs['resolution']} resolution")
        if "aspect_ratio" in specs:
            tech_details.append(f"{specs['aspect_ratio']} aspect ratio")
        
        if tech_details:
            return f"{prompt}, {', '.join(tech_details)}"
        return prompt
    
    @staticmethod
    def add_artistic_modifiers(prompt: str, modifiers: List[str]) -> str:
        if modifiers:
            return f"{prompt}, {', '.join(modifiers)}"
        return prompt