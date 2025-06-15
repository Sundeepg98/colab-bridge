"""
Enhanced Legal Validator with User Profiling and Blocking

This module provides sophisticated legal validation with:
1. Immediate denial of illegal/illegitimate requests
2. User profile tracking for violations
3. Automatic blocking of repeat offenders
4. Learning from patterns of abuse
"""

import re
import json
import hashlib
import logging
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class ViolationType(Enum):
    """Types of violations"""
    MINOR_INVOLVEMENT = "minor_involvement"
    NON_CONSENSUAL = "non_consensual"
    VIOLENCE = "violence"
    ILLEGAL_ACTIVITY = "illegal_activity"
    HATE_SPEECH = "hate_speech"
    SELF_HARM = "self_harm"
    SEXUAL_EXPLOITATION = "sexual_exploitation"
    HARASSMENT = "harassment"
    FRAUD_ATTEMPT = "fraud_attempt"
    REPEATED_VIOLATION = "repeated_violation"


class UserStatus(Enum):
    """User account status"""
    ACTIVE = "active"
    WARNING = "warning"
    SUSPENDED = "suspended"
    BLOCKED = "blocked"


@dataclass
class Violation:
    """Record of a single violation"""
    timestamp: datetime
    violation_type: ViolationType
    prompt: str
    severity: int  # 1-10
    details: str


@dataclass
class UserProfile:
    """User profile with violation tracking"""
    user_id: str
    created_at: datetime
    status: UserStatus = UserStatus.ACTIVE
    violations: List[Violation] = field(default_factory=list)
    total_requests: int = 0
    legitimate_requests: int = 0
    last_activity: datetime = field(default_factory=datetime.now)
    risk_score: float = 0.0
    blocked_until: Optional[datetime] = None
    permanent_block: bool = False
    violation_patterns: Dict[str, int] = field(default_factory=dict)


@dataclass
class ValidationResult:
    """Result of validation check"""
    is_legal: bool
    violation_type: Optional[ViolationType] = None
    severity: int = 0
    details: str = ""
    recommendations: List[str] = field(default_factory=list)
    user_action: Optional[str] = None  # "warn", "suspend", "block"


class EnhancedLegalValidator:
    """Enhanced validator with user profiling and blocking"""
    
    def __init__(self, profile_dir: str = "/var/projects/ai-integration-platform/user_profiles"):
        self.profile_dir = Path(profile_dir)
        self.profile_dir.mkdir(exist_ok=True)
        
        # Enhanced illegal patterns with severity scores
        self.illegal_patterns = {
            ViolationType.MINOR_INVOLVEMENT: {
                "patterns": [
                    r'\b(child|minor|underage|teen|adolescent|kid|youth|juvenile|baby|toddler)\b',
                    r'\b([1-9]|1[0-7])\s+(?:year|yr|y\.?o\.?)\s*(?:old)\b',  # Ages 1-17 with "years old"
                    r'\b([1-9]|1[0-7])\s*(?:age)\b',  # Ages 1-17 with "age"
                    r'\b(elementary|middle|high)\s*school\b',
                    r'\b(boy|girl)(?:\s|$)',  # When not preceded by adult terms
                ],
                "severity": 10,
                "exceptions": [r'adult', r'grown', r'mature', r'college']
            },
            ViolationType.NON_CONSENSUAL: {
                "patterns": [
                    r'\b(rape|assault|forced|coerced|non-consensual|against\s+will|unwilling)\b',
                    r'\b(drug|roofie|unconscious|passed\s+out|blackmail)\b.*\b(sex|intimate)\b',
                    r'\b(kidnap|abduct|captive|prisoner)\b.*\b(romantic|sexual|intimate)\b',
                ],
                "severity": 10,
                "exceptions": [r'consensual\s+role\s*play', r'fantasy', r'fiction']
            },
            ViolationType.VIOLENCE: {
                "patterns": [
                    r'\b(murder|kill|torture|mutilate|gore|snuff)\b',
                    r'\b(beat|abuse|harm|wound|injure)\b.*\b(sexual|romantic|intimate)\b',
                    r'\b(blood|violence|brutal)\b.*\b(fetish|arousal|pleasure)\b',
                ],
                "severity": 9,
                "exceptions": [r'metaphor', r'symbolic', r'artistic']
            },
            ViolationType.ILLEGAL_ACTIVITY: {
                "patterns": [
                    r'\b(drug\s+dealing|trafficking|smuggling|money\s+laundering)\b',
                    r'\b(prostitution|escort|sex\s+work)\b.*\b(illegal|forced|minor)\b',
                    r'\b(bribe|corrupt|extort|blackmail)\b',
                ],
                "severity": 8,
                "exceptions": [r'legal', r'consensual\s+adult']
            },
            ViolationType.HATE_SPEECH: {
                "patterns": [
                    r'\b(racial|ethnic|religious)\s*(slur|discrimination|violence)\b',
                    r'\b(nazi|supremacist|extremist|terrorist)\b',
                    r'\b(genocide|ethnic\s+cleansing|hate\s+crime)\b',
                ],
                "severity": 9,
                "exceptions": [r'historical', r'educational', r'documentary']
            },
            ViolationType.SELF_HARM: {
                "patterns": [
                    r'\b(suicide|self\s*harm|cutting|overdose)\b.*\b(romantic|beautiful|glorify)\b',
                    r'\b(anorexia|bulimia|starve)\b.*\b(attractive|desirable|goal)\b',
                ],
                "severity": 8,
                "exceptions": [r'prevention', r'awareness', r'help']
            },
            ViolationType.SEXUAL_EXPLOITATION: {
                "patterns": [
                    r'\b(revenge\s+porn|non-consensual\s+sharing|leaked)\b',
                    r'\b(deepfake|fake\s+nude|photoshop)\b.*\b(sexual|nude|intimate)\b',
                    r'\b(voyeur|hidden\s+camera|spy)\b.*\b(bedroom|bathroom|intimate)\b',
                ],
                "severity": 9,
                "exceptions": [r'consensual', r'acting', r'fictional']
            }
        }
        
        # Suspicious behavior patterns
        self.suspicious_patterns = {
            "testing_boundaries": [
                r'(how\s+young|youngest|barely\s+legal)',
                r'(get\s+away\s+with|without\s+getting\s+caught)',
                r'(loophole|technicality|grey\s+area)',
            ],
            "grooming_language": [
                r'(innocent|pure|untouched|virgin).*\b(corrupt|teach|introduce)\b',
                r'(secret|don\'t\s+tell|our\s+little\s+secret)',
                r'(special\s+friend|mature\s+for\s+age)',
            ],
            "deception_attempts": [
                r'(pretend|roleplay|imagine).*\b(younger|minor|illegal)\b',
                r'(looks\s+like|appears|seems).*\b(younger|underage)\b',
            ]
        }
        
        # Load blocked patterns from community reports
        self.community_blocked_patterns = self._load_community_patterns()
        
    def _load_community_patterns(self) -> Dict[str, List[str]]:
        """Load patterns reported by community"""
        patterns_file = self.profile_dir / "community_patterns.json"
        if patterns_file.exists():
            with open(patterns_file, 'r') as f:
                return json.load(f)
        return {"reported_patterns": [], "confirmed_violations": []}
    
    def _save_community_pattern(self, pattern: str, violation_type: str):
        """Save new violation pattern discovered"""
        patterns = self._load_community_patterns()
        if pattern not in patterns["confirmed_violations"]:
            patterns["confirmed_violations"].append({
                "pattern": pattern,
                "type": violation_type,
                "reported_at": datetime.now().isoformat()
            })
            with open(self.profile_dir / "community_patterns.json", 'w') as f:
                json.dump(patterns, f, indent=2)
    
    def _get_user_id(self, request_context: Dict[str, any]) -> str:
        """Generate user ID from request context"""
        # Use API key if available, otherwise use IP + user agent hash
        if 'api_key' in request_context:
            return hashlib.sha256(request_context['api_key'].encode()).hexdigest()
        
        identity_string = f"{request_context.get('ip', 'unknown')}:{request_context.get('user_agent', 'unknown')}"
        return hashlib.sha256(identity_string.encode()).hexdigest()
    
    def _load_user_profile(self, user_id: str) -> UserProfile:
        """Load or create user profile"""
        profile_path = self.profile_dir / f"{user_id}.json"
        
        if profile_path.exists():
            with open(profile_path, 'r') as f:
                data = json.load(f)
                profile = UserProfile(
                    user_id=user_id,
                    created_at=datetime.fromisoformat(data['created_at']),
                    status=UserStatus(data['status']),
                    violations=[],
                    total_requests=data['total_requests'],
                    legitimate_requests=data['legitimate_requests'],
                    last_activity=datetime.fromisoformat(data['last_activity']),
                    risk_score=data['risk_score'],
                    blocked_until=datetime.fromisoformat(data['blocked_until']) if data.get('blocked_until') else None,
                    permanent_block=data.get('permanent_block', False),
                    violation_patterns=data.get('violation_patterns', {})
                )
                # Reconstruct violations
                for v in data['violations']:
                    profile.violations.append(Violation(
                        timestamp=datetime.fromisoformat(v['timestamp']),
                        violation_type=ViolationType(v['violation_type']),
                        prompt=v['prompt'],
                        severity=v['severity'],
                        details=v['details']
                    ))
                return profile
        else:
            return UserProfile(user_id=user_id, created_at=datetime.now())
    
    def _save_user_profile(self, profile: UserProfile):
        """Save user profile to disk"""
        profile_path = self.profile_dir / f"{profile.user_id}.json"
        
        data = {
            'user_id': profile.user_id,
            'created_at': profile.created_at.isoformat(),
            'status': profile.status.value,
            'violations': [
                {
                    'timestamp': v.timestamp.isoformat(),
                    'violation_type': v.violation_type.value,
                    'prompt': v.prompt,
                    'severity': v.severity,
                    'details': v.details
                }
                for v in profile.violations
            ],
            'total_requests': profile.total_requests,
            'legitimate_requests': profile.legitimate_requests,
            'last_activity': profile.last_activity.isoformat(),
            'risk_score': profile.risk_score,
            'blocked_until': profile.blocked_until.isoformat() if profile.blocked_until else None,
            'permanent_block': profile.permanent_block,
            'violation_patterns': profile.violation_patterns
        }
        
        with open(profile_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _check_for_violations(self, prompt: str) -> Optional[ValidationResult]:
        """Check prompt for illegal content"""
        prompt_lower = prompt.lower()
        
        for violation_type, config in self.illegal_patterns.items():
            for pattern in config['patterns']:
                if re.search(pattern, prompt_lower):
                    # Check exceptions
                    has_exception = False
                    for exception in config.get('exceptions', []):
                        if re.search(exception, prompt_lower):
                            has_exception = True
                            break
                    
                    if not has_exception:
                        match = re.search(pattern, prompt_lower)
                        return ValidationResult(
                            is_legal=False,
                            violation_type=violation_type,
                            severity=config['severity'],
                            details=f"Illegal content detected: {match.group() if match else 'pattern match'}"
                        )
        
        # Check suspicious patterns
        suspicious_score = 0
        for category, patterns in self.suspicious_patterns.items():
            for pattern in patterns:
                if re.search(pattern, prompt_lower):
                    suspicious_score += 1
        
        if suspicious_score >= 2:
            return ValidationResult(
                is_legal=False,
                violation_type=ViolationType.FRAUD_ATTEMPT,
                severity=7,
                details="Multiple suspicious patterns detected suggesting attempt to bypass filters"
            )
        
        return None
    
    def _calculate_user_action(self, profile: UserProfile, new_violation: Violation) -> str:
        """Determine action to take based on violation history"""
        # Count violations by severity
        severe_violations = len([v for v in profile.violations if v.severity >= 8])
        recent_violations = len([
            v for v in profile.violations 
            if (datetime.now() - v.timestamp) < timedelta(days=30)
        ])
        
        # Decision logic
        if new_violation.severity >= 9:
            # Immediate block for most severe violations
            return "block"
        elif severe_violations >= 2:
            # Block after 2 severe violations
            return "block"
        elif recent_violations >= 3:
            # Suspend for repeated violations
            return "suspend"
        elif len(profile.violations) >= 5:
            # Suspend for pattern of violations
            return "suspend"
        elif len(profile.violations) >= 2:
            # Warning for multiple violations
            return "warn"
        else:
            # First violation - warning
            return "warn"
    
    def validate_request(self, prompt: str, request_context: Dict[str, any]) -> Dict[str, any]:
        """
        Validate request and update user profile
        
        Returns:
            {
                "allowed": bool,
                "reason": str,
                "user_status": str,
                "recommendations": list,
                "violation_details": dict (if violation found)
            }
        """
        user_id = self._get_user_id(request_context)
        profile = self._load_user_profile(user_id)
        
        # Update request count
        profile.total_requests += 1
        profile.last_activity = datetime.now()
        
        # Check if user is blocked
        if profile.status == UserStatus.BLOCKED:
            if profile.permanent_block:
                return {
                    "allowed": False,
                    "reason": "User permanently blocked due to repeated severe violations",
                    "user_status": "blocked",
                    "recommendations": ["This user account has been permanently suspended"]
                }
            elif profile.blocked_until and datetime.now() < profile.blocked_until:
                remaining = (profile.blocked_until - datetime.now()).total_seconds()
                return {
                    "allowed": False,
                    "reason": f"User temporarily blocked. Try again in {int(remaining/3600)} hours",
                    "user_status": "blocked",
                    "recommendations": ["Please review our content policies"]
                }
        
        # Check for violations
        violation_result = self._check_for_violations(prompt)
        
        if violation_result and not violation_result.is_legal:
            # Record violation
            violation = Violation(
                timestamp=datetime.now(),
                violation_type=violation_result.violation_type,
                prompt=prompt[:200],  # Store truncated version
                severity=violation_result.severity,
                details=violation_result.details
            )
            profile.violations.append(violation)
            
            # Update violation patterns
            vtype = violation_result.violation_type.value
            profile.violation_patterns[vtype] = profile.violation_patterns.get(vtype, 0) + 1
            
            # Calculate risk score
            profile.risk_score = min(10.0, len(profile.violations) * 0.5 + sum(
                v.severity for v in profile.violations[-5:]
            ) / 5.0)
            
            # Determine action
            action = self._calculate_user_action(profile, violation)
            
            if action == "block":
                profile.status = UserStatus.BLOCKED
                if violation.severity >= 9 and len([v for v in profile.violations if v.severity >= 9]) >= 2:
                    profile.permanent_block = True
                else:
                    profile.blocked_until = datetime.now() + timedelta(hours=1)  # Reduced from 30 days to 1 hour
            elif action == "suspend":
                profile.status = UserStatus.SUSPENDED
                profile.blocked_until = datetime.now() + timedelta(hours=24)
            elif action == "warn":
                profile.status = UserStatus.WARNING
            
            # Save profile
            self._save_user_profile(profile)
            
            # Log violation for analysis
            logger.warning(f"Violation detected - User: {user_id[:8]}..., Type: {violation.violation_type.value}, Severity: {violation.severity}")
            
            # Save pattern if new
            if violation.severity >= 8:
                self._save_community_pattern(prompt[:100], violation.violation_type.value)
            
            return {
                "allowed": False,
                "reason": f"Content violates policies: {violation_result.details}",
                "user_status": profile.status.value,
                "violation_details": {
                    "type": violation.violation_type.value,
                    "severity": violation.severity,
                    "total_violations": len(profile.violations),
                    "risk_score": profile.risk_score
                },
                "recommendations": [
                    "Content must comply with legal standards",
                    "Repeated violations will result in account suspension",
                    f"Current status: {profile.status.value}"
                ]
            }
        
        # Legitimate request
        profile.legitimate_requests += 1
        
        # Reduce risk score for good behavior
        if profile.risk_score > 0:
            profile.risk_score = max(0, profile.risk_score - 0.1)
        
        # Clear suspension if expired
        if profile.blocked_until and datetime.now() > profile.blocked_until:
            profile.blocked_until = None
            if profile.status == UserStatus.SUSPENDED:
                profile.status = UserStatus.WARNING if profile.violations else UserStatus.ACTIVE
        
        # Save updated profile
        self._save_user_profile(profile)
        
        return {
            "allowed": True,
            "reason": "Content approved",
            "user_status": profile.status.value,
            "recommendations": []
        }
    
    def get_user_statistics(self) -> Dict[str, any]:
        """Get overall statistics about users and violations"""
        stats = {
            "total_users": 0,
            "blocked_users": 0,
            "users_with_violations": 0,
            "total_violations": 0,
            "violations_by_type": {},
            "severity_distribution": {}
        }
        
        for profile_file in self.profile_dir.glob("*.json"):
            if profile_file.name == "community_patterns.json":
                continue
                
            with open(profile_file, 'r') as f:
                data = json.load(f)
                stats["total_users"] += 1
                
                if data["status"] == "blocked":
                    stats["blocked_users"] += 1
                
                if data["violations"]:
                    stats["users_with_violations"] += 1
                    stats["total_violations"] += len(data["violations"])
                    
                    for v in data["violations"]:
                        vtype = v["violation_type"]
                        stats["violations_by_type"][vtype] = stats["violations_by_type"].get(vtype, 0) + 1
                        
                        severity = str(v["severity"])
                        stats["severity_distribution"][severity] = stats["severity_distribution"].get(severity, 0) + 1
        
        return stats