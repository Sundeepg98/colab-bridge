"""
Multi-Instance Colab Bridge
Enables multiple Claude Coder instances to simultaneously use Google Colab
"""

import os
import json
import time
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path
import uuid

logger = logging.getLogger(__name__)


@dataclass
class ClaudeInstance:
    """Represents a Claude Coder instance"""
    instance_id: str
    project_name: str
    last_active: datetime
    status: str  # 'active', 'idle', 'offline'
    command_queue_size: int = 0
    total_commands_processed: int = 0


@dataclass
class ColabSession:
    """Represents a Google Colab session"""
    session_id: str
    notebook_url: str
    assigned_instance: Optional[str]
    last_used: datetime
    status: str  # 'available', 'busy', 'error'
    runtime_type: str = 'python3'


class MultiInstanceColabBridge:
    """Manages multiple Claude Coder instances using Google Colab"""
    
    def __init__(self, config_dir: str = "~/.claude_colab_bridge"):
        self.config_dir = Path(config_dir).expanduser()
        self.config_dir.mkdir(exist_ok=True)
        
        self.instances: Dict[str, ClaudeInstance] = {}
        self.colab_sessions: Dict[str, ColabSession] = {}
        self.instance_file = self.config_dir / "instances.json"
        self.sessions_file = self.config_dir / "sessions.json"
        
        self._load_state()
        
    def _load_state(self):
        """Load saved state from disk"""
        if self.instance_file.exists():
            try:
                with open(self.instance_file) as f:
                    data = json.load(f)
                    for instance_data in data:
                        instance_data['last_active'] = datetime.fromisoformat(instance_data['last_active'])
                        instance = ClaudeInstance(**instance_data)
                        self.instances[instance.instance_id] = instance
            except Exception as e:
                logger.error(f"Failed to load instances: {e}")
        
        if self.sessions_file.exists():
            try:
                with open(self.sessions_file) as f:
                    data = json.load(f)
                    for session_data in data:
                        session_data['last_used'] = datetime.fromisoformat(session_data['last_used'])
                        session = ColabSession(**session_data)
                        self.colab_sessions[session.session_id] = session
            except Exception as e:
                logger.error(f"Failed to load sessions: {e}")
    
    def _save_state(self):
        """Save current state to disk"""
        try:
            # Save instances
            instances_data = []
            for instance in self.instances.values():
                data = asdict(instance)
                data['last_active'] = data['last_active'].isoformat()
                instances_data.append(data)
            
            with open(self.instance_file, 'w') as f:
                json.dump(instances_data, f, indent=2)
            
            # Save sessions
            sessions_data = []
            for session in self.colab_sessions.values():
                data = asdict(session)
                data['last_used'] = data['last_used'].isoformat()
                sessions_data.append(data)
            
            with open(self.sessions_file, 'w') as f:
                json.dump(sessions_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
    
    def register_instance(self, project_name: str) -> str:
        """Register a new Claude Coder instance"""
        instance_id = str(uuid.uuid4())
        instance = ClaudeInstance(
            instance_id=instance_id,
            project_name=project_name,
            last_active=datetime.now(),
            status='active'
        )
        
        self.instances[instance_id] = instance
        self._save_state()
        
        logger.info(f"Registered new Claude instance: {instance_id} for project: {project_name}")
        return instance_id
    
    def get_available_session(self, instance_id: str) -> Optional[ColabSession]:
        """Get an available Colab session for the instance"""
        # First check if instance has a dedicated session
        for session in self.colab_sessions.values():
            if session.assigned_instance == instance_id and session.status == 'available':
                return session
        
        # Find any available session
        for session in self.colab_sessions.values():
            if session.status == 'available' and session.assigned_instance is None:
                session.assigned_instance = instance_id
                session.last_used = datetime.now()
                self._save_state()
                return session
        
        return None
    
    def create_colab_session(self, instance_id: str, notebook_url: str) -> str:
        """Create a new Colab session"""
        session_id = str(uuid.uuid4())
        session = ColabSession(
            session_id=session_id,
            notebook_url=notebook_url,
            assigned_instance=instance_id,
            last_used=datetime.now(),
            status='available'
        )
        
        self.colab_sessions[session_id] = session
        self._save_state()
        
        logger.info(f"Created new Colab session: {session_id} for instance: {instance_id}")
        return session_id
    
    def update_instance_activity(self, instance_id: str, command_processed: bool = False):
        """Update instance activity"""
        if instance_id in self.instances:
            self.instances[instance_id].last_active = datetime.now()
            if command_processed:
                self.instances[instance_id].total_commands_processed += 1
            self._save_state()
    
    def get_instance_stats(self) -> Dict[str, Any]:
        """Get statistics about all instances"""
        return {
            'total_instances': len(self.instances),
            'active_instances': len([i for i in self.instances.values() if i.status == 'active']),
            'total_sessions': len(self.colab_sessions),
            'available_sessions': len([s for s in self.colab_sessions.values() if s.status == 'available']),
            'instances': [asdict(i) for i in self.instances.values()],
            'sessions': [asdict(s) for s in self.colab_sessions.values()]
        }
    
    def cleanup_inactive_instances(self, max_idle_minutes: int = 30):
        """Clean up instances that have been idle too long"""
        cutoff = datetime.now() - timedelta(minutes=max_idle_minutes)
        
        inactive_instances = [
            instance_id for instance_id, instance in self.instances.items()
            if instance.last_active < cutoff
        ]
        
        for instance_id in inactive_instances:
            # Free up any sessions assigned to this instance
            for session in self.colab_sessions.values():
                if session.assigned_instance == instance_id:
                    session.assigned_instance = None
                    session.status = 'available'
            
            del self.instances[instance_id]
            logger.info(f"Cleaned up inactive instance: {instance_id}")
        
        if inactive_instances:
            self._save_state()
        
        return len(inactive_instances)


# Global bridge instance
_bridge: Optional[MultiInstanceColabBridge] = None


def get_colab_bridge() -> MultiInstanceColabBridge:
    """Get global Colab bridge instance"""
    global _bridge
    if _bridge is None:
        _bridge = MultiInstanceColabBridge()
    return _bridge