"""
AI-Powered Prompt Enhancement Module

This module uses AI APIs to further enhance and validate prompts
"""

import os
from typing import Dict, Optional, List
from dataclasses import dataclass
import openai
from anthropic import Anthropic


@dataclass
class EnhancementResult:
    original: str
    enhanced: str
    ai_suggestions: List[str]
    confidence_boost: float
    service_used: str


class AIPromptEnhancer:
    def __init__(self):
        # Load API keys from environment
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        
        # Initialize clients if keys are available
        self.openai_client = None
        self.anthropic_client = None
        
        # Claude model preference order (only use models we know exist)
        self.claude_models = [
            ("claude-3-5-sonnet-20241022", "Claude-3.5-Sonnet"),  # Known working model
            ("claude-3-haiku-20240307", "Claude-3-Haiku")  # Known working fallback
        ]
        
        if self.openai_key:
            openai.api_key = self.openai_key
            self.openai_client = openai
        
        if self.anthropic_key:
            self.anthropic_client = Anthropic(api_key=self.anthropic_key)
    
    def enhance_with_gpt(self, prompt: str, context: str = "video generation") -> Optional[EnhancementResult]:
        """Use GPT to enhance prompts"""
        if not self.openai_client:
            return None
        
        try:
            response = self.openai_client.ChatCompletion.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert at optimizing prompts for {context}. "
                                 "Enhance the given prompt to be more detailed, specific, and likely to produce high-quality results. "
                                 "Focus on visual details, artistic style, and technical specifications."
                    },
                    {
                        "role": "user",
                        "content": f"Enhance this prompt: {prompt}"
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            enhanced = response.choices[0].message.content
            
            # Get suggestions
            suggestions_response = self.openai_client.ChatCompletion.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "Provide 3 specific suggestions to improve this prompt further."
                    },
                    {
                        "role": "user",
                        "content": f"Original: {prompt}\nEnhanced: {enhanced}"
                    }
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            suggestions = suggestions_response.choices[0].message.content.split('\n')
            suggestions = [s.strip() for s in suggestions if s.strip()][:3]
            
            return EnhancementResult(
                original=prompt,
                enhanced=enhanced,
                ai_suggestions=suggestions,
                confidence_boost=0.15,
                service_used="GPT-4"
            )
            
        except Exception as e:
            print(f"GPT enhancement error: {e}")
            return None
    
    def enhance_with_claude(self, prompt: str, context: str = "video generation") -> Optional[EnhancementResult]:
        """Use Claude to enhance prompts"""
        if not self.anthropic_client:
            return None
        
        # Try models in preference order
        for model_id, model_name in self.claude_models:
            try:
                # Enhance the prompt
                response = self.anthropic_client.messages.create(
                    model=model_id,
                    max_tokens=500,
                    temperature=0.7,
                    messages=[
                        {
                            "role": "user",
                            "content": f"As an expert in {context} prompts, enhance this prompt to be more specific, "
                                     f"detailed, and likely to produce high-quality results. "
                                     f"Focus on visual details, composition, and artistic style.\n\n"
                                     f"Prompt: {prompt}"
                        }
                    ]
                )
            
                enhanced = response.content[0].text
                
                # Get suggestions using same model
                suggestions_response = self.anthropic_client.messages.create(
                    model=model_id,
                    max_tokens=200,
                    temperature=0.7,
                    messages=[
                        {
                            "role": "user",
                            "content": f"Provide 3 specific suggestions to further improve this enhanced prompt:\n{enhanced}"
                        }
                    ]
                )
                
                suggestions_text = suggestions_response.content[0].text
                suggestions = [s.strip() for s in suggestions_text.split('\n') if s.strip()][:3]
                
                # Adjust confidence boost based on model
                confidence_boost = 0.25 if "Opus-4" in model_name else 0.20
                
                return EnhancementResult(
                    original=prompt,
                    enhanced=enhanced,
                    ai_suggestions=suggestions,
                    confidence_boost=confidence_boost,
                    service_used=model_name
                )
                
            except Exception as e:
                print(f"Claude {model_name} error: {e}, trying next model...")
                continue
        
        # If all models fail
        return None
    
    def validate_with_ai(self, prompt: str) -> Dict[str, any]:
        """Validate prompt using AI"""
        validation_results = {
            "is_clear": True,
            "has_visual_details": True,
            "appropriate_length": True,
            "ai_feedback": [],
            "overall_quality": 0.0
        }
        
        if self.openai_client:
            try:
                response = self.openai_client.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "Analyze this video generation prompt and provide feedback on: "
                                     "1) Clarity 2) Visual detail level 3) Length appropriateness 4) Potential issues"
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,
                    max_tokens=200
                )
                
                feedback = response.choices[0].message.content
                validation_results["ai_feedback"].append(feedback)
                
                # Simple quality scoring based on prompt characteristics
                quality_score = 0.5
                if len(prompt.split()) > 10:
                    quality_score += 0.2
                if any(word in prompt.lower() for word in ["detailed", "specific", "professional", "high-quality"]):
                    quality_score += 0.2
                if len(prompt) > 50:
                    quality_score += 0.1
                
                validation_results["overall_quality"] = min(quality_score, 1.0)
                
            except Exception as e:
                print(f"Validation error: {e}")
        
        return validation_results
    
    def suggest_alternatives(self, prompt: str, num_alternatives: int = 3) -> List[str]:
        """Generate alternative versions of the prompt"""
        alternatives = []
        
        if self.openai_client:
            try:
                response = self.openai_client.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": f"Generate {num_alternatives} alternative versions of this prompt. "
                                     "Each should maintain the core concept but vary in style, perspective, or details."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.8,
                    max_tokens=500
                )
                
                alternatives_text = response.choices[0].message.content
                alternatives = [alt.strip() for alt in alternatives_text.split('\n') if alt.strip()][:num_alternatives]
                
            except Exception as e:
                print(f"Alternative generation error: {e}")
        
        return alternatives


class PromptImprovementEngine:
    """Combines AI enhancement with existing optimization"""
    
    def __init__(self):
        self.ai_enhancer = AIPromptEnhancer()
    
    def enhance_optimized_prompt(self, optimized_prompt: str, original_prompt: str) -> Dict[str, any]:
        """Further enhance an already optimized prompt using AI"""
        
        result = {
            "original": original_prompt,
            "optimized": optimized_prompt,
            "ai_enhanced": None,
            "final_prompt": optimized_prompt,
            "confidence_boost": 0.0,
            "ai_suggestions": [],
            "service_available": False
        }
        
        # Try Claude first (typically better for creative tasks)
        enhancement = self.ai_enhancer.enhance_with_claude(optimized_prompt)
        
        # Fallback to GPT if Claude is not available
        if not enhancement and self.ai_enhancer.openai_client:
            enhancement = self.ai_enhancer.enhance_with_gpt(optimized_prompt)
        
        if enhancement:
            result["ai_enhanced"] = enhancement.enhanced
            result["final_prompt"] = enhancement.enhanced
            result["confidence_boost"] = enhancement.confidence_boost
            result["ai_suggestions"] = enhancement.ai_suggestions
            result["service_available"] = True
            result["service_used"] = enhancement.service_used
        
        return result
    
    def validate_final_prompt(self, prompt: str) -> Dict[str, any]:
        """Validate the final prompt using AI"""
        return self.ai_enhancer.validate_with_ai(prompt)