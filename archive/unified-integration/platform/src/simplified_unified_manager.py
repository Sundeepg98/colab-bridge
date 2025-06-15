"""
Simplified Unified Integration Manager
Works without complex dependencies - focused on multi-instance Colab bridge
"""

import os
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class UnifiedResponse:
    """Unified response format for all operations"""
    success: bool
    data: Any
    service_used: str
    fallback_used: bool
    cost: float
    processing_time: float
    metadata: Dict[str, Any]
    error: Optional[str] = None


class SimplifiedUnifiedManager:
    """Simplified coordinator focused on multi-instance Colab bridge"""
    
    def __init__(self):
        self.active_instances: Dict[str, Any] = {}
        self.session_pool: List[str] = []
        
    async def process_request(self, request: Dict[str, Any], instance_id: str) -> UnifiedResponse:
        """Process a request through the multi-instance bridge"""
        start_time = datetime.now()
        
        try:
            # Get available Colab session for this instance
            from multi_instance_colab_bridge import get_colab_bridge
            bridge = get_colab_bridge()
            
            session = bridge.get_available_session(instance_id)
            if not session:
                return UnifiedResponse(
                    success=False,
                    data=None,
                    service_used="colab_bridge",
                    fallback_used=False,
                    cost=0.0,
                    processing_time=0.0,
                    metadata={},
                    error="No available Colab session"
                )
            
            # Simulate processing
            await asyncio.sleep(0.1)
            
            # Update instance activity
            bridge.update_instance_activity(instance_id, command_processed=True)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return UnifiedResponse(
                success=True,
                data={"result": "Processed through Colab bridge", "session_id": session.session_id},
                service_used="colab_bridge",
                fallback_used=False,
                cost=0.0,  # Free through Colab
                processing_time=processing_time,
                metadata={"instance_id": instance_id, "session_id": session.session_id}
            )
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"Error processing request: {e}")
            
            return UnifiedResponse(
                success=False,
                data=None,
                service_used="colab_bridge",
                fallback_used=False,
                cost=0.0,
                processing_time=processing_time,
                metadata={},
                error=str(e)
            )
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the simplified manager"""
        try:
            from multi_instance_colab_bridge import get_colab_bridge
            bridge = get_colab_bridge()
            stats = bridge.get_instance_stats()
            
            return {
                "status": "running",
                "bridge_stats": stats,
                "manager_type": "simplified_unified"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "manager_type": "simplified_unified"
            }


# Global manager instance
_manager: Optional[SimplifiedUnifiedManager] = None


def get_simplified_manager() -> SimplifiedUnifiedManager:
    """Get global simplified manager instance"""
    global _manager
    if _manager is None:
        _manager = SimplifiedUnifiedManager()
    return _manager