"""
TEC AXIOM ENGINE
The philosophical validator and guardian of the Eight Axioms

This module serves as the moral and philosophical compass of the entire TEC system,
ensuring all content and actions align with the foundational principles.
"""

import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class AxiomEngine:
    """
    The Axiom Engine - Guardian of the Eight Axioms of the Architect
    
    Validates all content against the fundamental principles that govern
    the TEC universe and its moral framework.
    """
    
    def __init__(self):
        self.status = "INITIALIZING"
        self.axioms = self._load_axioms()
        self.validation_history = []
        
    def _load_axioms(self) -> Dict[str, Dict[str, Any]]:
        """Load the Eight Axioms of the Architect"""
        return {
            "narrative_supremacy": {
                "name": "Narrative Supremacy",
                "description": "The story defines reality; control the narrative, control the outcome",
                "weight": 1.0,
                "keywords": ["story", "narrative", "truth", "reality", "perception"],
                "violations": ["false narratives", "propaganda", "manipulation"]
            },
            "duality_principle": {
                "name": "Duality Principle", 
                "description": "All truth exists in the tension between opposites; reject binary thinking",
                "weight": 1.0,
                "keywords": ["balance", "grey", "complexity", "nuance", "tension"],
                "violations": ["absolute statements", "binary thinking", "oversimplification"]
            },
            "flawed_hero_doctrine": {
                "name": "Flawed Hero Doctrine",
                "description": "True heroes are defined by their struggles, not their victories",
                "weight": 1.0,
                "keywords": ["struggle", "growth", "imperfection", "journey", "humanity"],
                "violations": ["perfectionism", "hero worship", "unrealistic standards"]
            },
            "justifiable_force_doctrine": {
                "name": "Justifiable Force Doctrine",
                "description": "Violence is only moral when protecting the innocent or preserving justice",
                "weight": 1.0,
                "keywords": ["protection", "justice", "defense", "necessity", "proportional"],
                "violations": ["unnecessary violence", "revenge", "disproportionate response"]
            },
            "sovereign_accountability": {
                "name": "Sovereign Accountability",
                "description": "Power must be earned through service and maintained through transparency",
                "weight": 1.0,
                "keywords": ["service", "transparency", "responsibility", "earned", "accountable"],
                "violations": ["abuse of power", "corruption", "unearned authority"]
            },
            "authentic_performance": {
                "name": "Authentic Performance",
                "description": "Excellence in action, not just intention; authenticity over appearance",
                "weight": 1.0,
                "keywords": ["authenticity", "action", "performance", "substance", "genuine"],
                "violations": ["virtue signaling", "performative acts", "false authenticity"]
            },
            "transparency_mandate": {
                "name": "Transparency Mandate",
                "description": "Truth must be accessible; secrets serve only the corrupt",
                "weight": 1.0,
                "keywords": ["transparency", "truth", "openness", "accessibility", "honest"],
                "violations": ["unnecessary secrecy", "deception", "hidden agendas"]
            },
            "generational_responsibility": {
                "name": "Generational Responsibility",
                "description": "Every action must consider its impact on future generations",
                "weight": 1.0,
                "keywords": ["future", "legacy", "sustainability", "responsibility", "impact"],
                "violations": ["short-term thinking", "environmental damage", "future harm"]
            }
        }
    
    def initialize(self):
        """Initialize the Axiom Engine"""
        logger.info("🏛️  Initializing Axiom Engine...")
        logger.info(f"Loaded {len(self.axioms)} foundational axioms")
        
        # Validate axiom definitions
        for axiom_id, axiom in self.axioms.items():
            if not all(key in axiom for key in ['name', 'description', 'weight']):
                raise ValueError(f"Invalid axiom definition: {axiom_id}")
        
        self.status = "OPERATIONAL"
        logger.info("✅ Axiom Engine operational")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the Axiom Engine"""
        return {
            'status': self.status,
            'axioms_loaded': len(self.axioms),
            'validations_performed': len(self.validation_history),
            'last_validation': self.validation_history[-1]['timestamp'] if self.validation_history else None
        }
    
    def validate_content(self, content: str, content_type: str = 'general') -> Dict[str, Any]:
        """
        Validate content against all Eight Axioms
        
        Args:
            content: The content to validate
            content_type: Type of content (story, decision, policy, etc.)
            
        Returns:
            Validation result with scores and recommendations
        """
        try:
            scores = {}
            violations = []
            recommendations = []
            
            content_lower = content.lower()
            
            # Evaluate against each axiom
            for axiom_id, axiom in self.axioms.items():
                score = self._evaluate_axiom_alignment(content_lower, axiom)
                scores[axiom_id] = {
                    'score': score,
                    'name': axiom['name'],
                    'threshold': 0.6  # Minimum acceptable score
                }
                
                # Check for violations
                if score < 0.6:
                    violations.append({
                        'axiom': axiom['name'],
                        'score': score,
                        'reason': f"Content may violate {axiom['name']} principles"
                    })
                    
                    recommendations.append(
                        f"Consider aligning content with {axiom['name']}: {axiom['description']}"
                    )
            
            # Calculate overall validity
            average_score = sum(s['score'] for s in scores.values()) / len(scores)
            is_valid = average_score >= 0.6 and len(violations) == 0
            
            # Log validation
            validation_record = {
                'timestamp': datetime.now().isoformat(),
                'content_type': content_type,
                'valid': is_valid,
                'average_score': average_score,
                'violations_count': len(violations)
            }
            self.validation_history.append(validation_record)
            
            return {
                'valid': is_valid,
                'scores': scores,
                'violations': violations,
                'recommendations': recommendations,
                'average_score': average_score,
                'content_type': content_type
            }
            
        except Exception as e:
            logger.error(f"Content validation error: {str(e)}")
            return {
                'valid': False,
                'error': str(e),
                'scores': {},
                'violations': [{'axiom': 'System', 'reason': 'Validation system error'}],
                'recommendations': ['Review content manually due to system error']
            }
    
    def _evaluate_axiom_alignment(self, content: str, axiom: Dict[str, Any]) -> float:
        """
        Evaluate how well content aligns with a specific axiom
        
        Returns a score between 0.0 and 1.0
        """
        score = 0.5  # Neutral starting point
        
        # Positive indicators
        positive_matches = 0
        for keyword in axiom['keywords']:
            if keyword.lower() in content:
                positive_matches += 1
        
        if positive_matches > 0:
            score += min(positive_matches * 0.1, 0.3)
        
        # Negative indicators (violations)
        violation_matches = 0
        for violation in axiom.get('violations', []):
            if violation.lower() in content:
                violation_matches += 1
        
        if violation_matches > 0:
            score -= min(violation_matches * 0.2, 0.4)
        
        # Ensure score stays within bounds
        return max(0.0, min(1.0, score))
    
    def validate_tool_request(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a tool execution request against axioms
        
        Ensures that tool usage aligns with TEC principles
        """
        try:
            # Create a description of the tool request for validation
            request_description = f"Tool: {tool_name}, Parameters: {str(parameters)}"
            
            # Use standard content validation
            validation = self.validate_content(request_description, 'tool_request')
            
            # Additional checks for tool-specific concerns
            if tool_name in ['delete', 'destroy', 'remove']:
                # Destructive actions need higher scrutiny
                validation['valid'] = validation['valid'] and validation['average_score'] > 0.8
            
            return validation
            
        except Exception as e:
            logger.error(f"Tool request validation error: {str(e)}")
            return {
                'valid': False,
                'error': str(e),
                'violations': [{'axiom': 'System', 'reason': 'Tool validation system error'}]
            }
    
    def get_axiom_summary(self) -> Dict[str, Any]:
        """Get a summary of all axioms for reference"""
        return {
            axiom_id: {
                'name': axiom['name'],
                'description': axiom['description']
            }
            for axiom_id, axiom in self.axioms.items()
        }
    
    def generate_axiom_report(self) -> Dict[str, Any]:
        """Generate a comprehensive report on axiom validation history"""
        if not self.validation_history:
            return {'message': 'No validations performed yet'}
        
        total_validations = len(self.validation_history)
        valid_validations = sum(1 for v in self.validation_history if v['valid'])
        
        return {
            'total_validations': total_validations,
            'valid_percentage': (valid_validations / total_validations) * 100,
            'recent_validations': self.validation_history[-10:],  # Last 10
            'axiom_definitions': self.get_axiom_summary()
        }
