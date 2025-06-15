"""
Simple Claude Enhancer - Single API call optimization
"""

import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SimpleClaudeEnhancer:
    """Simple Claude enhancement with single API call"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        # Import model selector
        try:
            from src.smart_claude_selector import get_model_selector
            self.model_selector = get_model_selector()
        except:
            self.model_selector = None
        
    def enhance(self, prompt: str, mode: str = 'comprehensive', 
                user_segment: str = 'casual_user', user_tier: str = 'basic',
                budget_remaining: float = 10.0, force_quality: bool = False) -> Dict[str, Any]:
        """Enhance prompt with single Claude API call"""
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            
            # Create enhancement prompt
            system_prompt = """You are an expert at optimizing prompts for Sora AI video generation. 
Your task is to take user prompts and enhance them to be more cinematic, artistic, and appropriate while maintaining the original intent.

Guidelines:
1. Make prompts more visually descriptive and cinematic
2. Ensure all content is appropriate and artistic
3. Handle sensitive content by reframing it tastefully
4. Add technical details like camera movements, lighting, and atmosphere
5. Keep the enhanced prompt under 200 words

For any content involving age differences or potentially inappropriate scenarios:
- Focus on respectful, dignified interactions
- Emphasize cultural or professional contexts
- Remove any romantic or intimate implications
- Highlight artistic and cinematic qualities instead"""

            user_message = f"Enhance this prompt for Sora AI video generation: {prompt}"
            
            # Select optimal model
            model_to_use = "claude-3-haiku-20240307"  # Default
            model_info = {"reasoning": "Default Haiku model", "model_tier": "HAIKU"}
            
            if self.model_selector:
                # Determine if we need quality for trial/demo
                is_trial = force_quality or (mode == 'comprehensive' and user_tier == 'basic' and len(prompt) > 100)
                
                model_selection = self.model_selector.select_model(
                    prompt=prompt,
                    user_segment=user_segment,
                    user_tier=user_tier,
                    quality_required=0.8 if mode == 'comprehensive' else 0.6,
                    budget_remaining=budget_remaining,
                    force_quality=is_trial
                )
                model_to_use = model_selection['model']
                model_info = model_selection
            
            # Make single API call
            response = client.messages.create(
                model=model_to_use,
                max_tokens=300,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ],
                timeout=5.0  # 5 second timeout
            )
            
            enhanced_prompt = response.content[0].text.strip()
            
            return {
                'success': True,
                'original': prompt,
                'optimized': enhanced_prompt,
                'confidence': model_info.get('quality_score', 0.95),
                'ai_enhanced': True,
                'service_used': f'Claude AI ({model_info.get("model_tier", "HAIKU")})',
                'tokens_used': response.usage.output_tokens,
                'model': model_info.get('model_tier', 'HAIKU'),
                'model_selection': {
                    'model_used': model_to_use,
                    'reasoning': model_info.get('reasoning', 'Default selection'),
                    'estimated_cost': model_info.get('estimated_cost', 0.0),
                    'complexity': model_info.get('complexity', 'unknown')
                }
            }
            
        except Exception as e:
            logger.error(f"Simple Claude enhancement failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }