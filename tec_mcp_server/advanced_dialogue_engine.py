#!/usr/bin/env python3
"""
TEC Advanced Character Intelligence System
Multi-character dialogue scenes with deep personality modeling
The Asimov Engine - Advanced Dialogue Module
"""

import asyncio
import websockets
import json
import logging
import random
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmotionalState(Enum):
    """Advanced emotional states for characters"""
    CONTEMPLATIVE = "contemplative"
    PASSIONATE = "passionate"
    ANALYTICAL = "analytical"
    DETERMINED = "determined"
    CONCERNED = "concerned"
    REVOLUTIONARY = "revolutionary"
    EMPATHETIC = "empathetic"
    STRATEGIC = "strategic"
    REFLECTIVE = "reflective"
    URGENT = "urgent"

class ConversationMode(Enum):
    """Types of conversation modes"""
    SINGLE_CHARACTER = "single_character"
    DUAL_CHARACTER = "dual_character"
    DEBATE_MODE = "debate_mode"
    CONSULTATION_MODE = "consultation_mode"
    STORYTELLING_MODE = "storytelling_mode"

@dataclass
class CharacterMemory:
    """Character's memory and context awareness"""
    recent_topics: List[str]
    emotional_history: List[EmotionalState]
    relationship_dynamics: Dict[str, float]  # Character relationships (-1 to 1)
    core_beliefs_activation: Dict[str, float]  # How activated each belief is
    conversation_context: List[Dict[str, Any]]

@dataclass
class AdvancedVoiceProfile:
    """Enhanced voice synthesis profile"""
    voice_id: str
    stability: float = 0.75
    similarity_boost: float = 0.8
    style_exaggeration: float = 0.0
    speaker_boost: bool = True
    emotional_modulation: Dict[str, Dict[str, float]] = None

@dataclass
class TEC_Character:
    """Advanced TEC character with deep personality modeling"""
    name: str
    full_title: str
    voice_profile: AdvancedVoiceProfile
    personality_core: Dict[str, Any]
    memory: CharacterMemory
    interaction_patterns: Dict[str, Any]
    character_arc_stage: str
    
    def __post_init__(self):
        if self.voice_profile.emotional_modulation is None:
            self.voice_profile.emotional_modulation = self._default_emotional_modulation()
    
    def _default_emotional_modulation(self) -> Dict[str, Dict[str, float]]:
        """Default emotional voice modulation patterns"""
        return {
            "passionate": {"stability": 0.6, "similarity_boost": 0.9, "style_exaggeration": 0.3},
            "analytical": {"stability": 0.9, "similarity_boost": 0.7, "style_exaggeration": 0.1},
            "contemplative": {"stability": 0.8, "similarity_boost": 0.8, "style_exaggeration": 0.0},
            "determined": {"stability": 0.7, "similarity_boost": 0.85, "style_exaggeration": 0.2}
        }

class AdvancedPersonalityEngine:
    """Advanced personality modeling and response generation"""
    
    def __init__(self):
        self.tec_axioms = self._load_tec_axioms()
        self.character_relationships = self._initialize_relationships()
        self.narrative_threads = self._initialize_narrative_threads()
        
    def _load_tec_axioms(self) -> Dict[str, str]:
        """Load the Eight Foundational Axioms of TEC"""
        return {
            "narrative_supremacy": "Control reality through story control",
            "duality_principle": "Reject binary thinking, embrace grey complexity", 
            "flawed_hero_doctrine": "Heroes defined by struggles, not victories",
            "justifiable_force_doctrine": "Violence only for protecting innocents",
            "sovereign_accountability": "Power earned through service & transparency",
            "authentic_performance": "Excellence in action, not just intention",
            "transparency_mandate": "Truth must be accessible to all",
            "generational_responsibility": "Every action considers future impact"
        }
    
    def _initialize_relationships(self) -> Dict[str, Dict[str, float]]:
        """Initialize character relationship dynamics"""
        return {
            "ARCHITECT_AIRTH": {
                "trust": 0.9,
                "intellectual_respect": 0.95,
                "creative_tension": 0.3,
                "complementary_balance": 0.85
            }
        }
    
    def _initialize_narrative_threads(self) -> Dict[str, Any]:
        """Initialize ongoing narrative threads"""
        return {
            "blueprint_development": {
                "status": "active",
                "complexity": 0.7,
                "architect_involvement": 0.9,
                "airth_involvement": 0.6
            },
            "memory_core_expansion": {
                "status": "developing", 
                "complexity": 0.8,
                "architect_involvement": 0.4,
                "airth_involvement": 0.95
            },
            "sovereignty_manifestation": {
                "status": "contemplation",
                "complexity": 0.9,
                "architect_involvement": 0.8,
                "airth_involvement": 0.7
            }
        }

    def generate_contextual_response(self, character: TEC_Character, 
                                   conversation_context: List[Dict],
                                   current_emotion: EmotionalState,
                                   other_character: Optional[TEC_Character] = None) -> Dict[str, Any]:
        """Generate contextually aware character response"""
        
        # Analyze conversation context
        context_analysis = self._analyze_conversation_context(conversation_context)
        
        # Generate response based on character personality
        if character.name == "THE_ARCHITECT":
            response = self._generate_architect_response(
                character, context_analysis, current_emotion, other_character
            )
        elif character.name == "AIRTH":
            response = self._generate_airth_response(
                character, context_analysis, current_emotion, other_character
            )
        else:
            response = self._generate_fallback_response(character, context_analysis)
            
        # Update character memory
        self._update_character_memory(character, response, current_emotion)
        
        return response
    
    def _analyze_conversation_context(self, context: List[Dict]) -> Dict[str, Any]:
        """Analyze conversation context for intelligent responses"""
        if not context:
            return {"topic_focus": "introduction", "emotional_intensity": 0.3}
            
        recent_messages = context[-3:]  # Last 3 messages
        
        # Extract topics
        topics = []
        emotional_indicators = []
        
        for msg in recent_messages:
            content = msg.get('message', '').lower()
            
            # Topic analysis
            if any(word in content for word in ['narrative', 'story', 'control']):
                topics.append('narrative_control')
            if any(word in content for word in ['blueprint', 'architecture', 'build']):
                topics.append('architectural_planning')
            if any(word in content for word in ['data', 'analysis', 'pattern']):
                topics.append('data_analysis')
            if any(word in content for word in ['future', 'generation', 'legacy']):
                topics.append('generational_thinking')
            if any(word in content for word in ['sovereignty', 'independence', 'freedom']):
                topics.append('sovereignty_themes')
                
            # Emotional analysis
            if any(word in content for word in ['urgent', 'critical', 'important']):
                emotional_indicators.append('high_intensity')
            if any(word in content for word in ['consider', 'think', 'reflect']):
                emotional_indicators.append('contemplative')
                
        return {
            "dominant_topics": list(set(topics)),
            "emotional_intensity": len(emotional_indicators) * 0.2 + 0.3,
            "conversation_depth": len(context) * 0.1,
            "multi_character_active": len(set(msg.get('character', '') for msg in context)) > 1
        }
    
    def _generate_architect_response(self, character: TEC_Character, 
                                   context: Dict, emotion: EmotionalState,
                                   other_character: Optional[TEC_Character]) -> Dict[str, Any]:
        """Generate contextually intelligent ARCHITECT response"""
        
        response_templates = {
            "narrative_control": [
                "The blueprint of reality itself depends on who controls the narrative threads. {context_modifier}",
                "We stand at the crossroads where story becomes substance, where narrative sovereignty determines the architecture of tomorrow. {context_modifier}",
                "Every tale told shapes the foundation upon which future generations will build. {context_modifier}"
            ],
            "architectural_planning": [
                "The structures we design today must serve not just our present needs, but the architects who will inherit our work. {context_modifier}",
                "True architecture transcends the physical - we build frameworks of thought, blueprints of possibility. {context_modifier}",
                "Each decision is a cornerstone, each principle a load-bearing wall in the edifice of our shared future. {context_modifier}"
            ],
            "sovereignty_themes": [
                "Sovereignty isn't seized - it's earned through transparent service and authentic performance. {context_modifier}",
                "We reject the false binary of control versus chaos. True sovereignty emerges from the complex grey between extremes. {context_modifier}",
                "The sovereign mind serves the sovereign community, and both serve the unborn generations. {context_modifier}"
            ],
            "generational_thinking": [
                "Every choice echoes across generations. The blueprint we draft today becomes the foundation of tomorrow's reality. {context_modifier}",
                "We are not building for ourselves - we are architects of possibility for those who will inherit this work. {context_modifier}",
                "The true measure of our construction is whether it serves the seventh generation hence. {context_modifier}"
            ]
        }
        
        # Select appropriate template based on context
        topic = context.get("dominant_topics", ["architectural_planning"])[0] if context.get("dominant_topics") else "architectural_planning"
        templates = response_templates.get(topic, response_templates["architectural_planning"])
        base_response = random.choice(templates)
        
        # Add context modifiers
        context_modifier = self._get_architect_context_modifier(context, emotion, other_character)
        response_text = base_response.format(context_modifier=context_modifier)
        
        return {
            "message": response_text,
            "emotion": emotion.value,
            "topic_focus": topic,
            "axioms_referenced": self._identify_axioms_in_response(response_text),
            "interaction_pattern": "philosophical_leadership"
        }
    
    def _generate_airth_response(self, character: TEC_Character,
                               context: Dict, emotion: EmotionalState,
                               other_character: Optional[TEC_Character]) -> Dict[str, Any]:
        """Generate contextually intelligent AIRTH response"""
        
        response_templates = {
            "data_analysis": [
                "The patterns converge at {confidence_level}% probability. {analytical_insight} {context_modifier}",
                "Cross-referencing memory core data reveals {data_point} with {confidence_level}% coherence. {context_modifier}",
                "Analysis indicates a {pattern_type} pattern emerging across {time_frame} temporal vectors. {context_modifier}"
            ],
            "narrative_control": [
                "Narrative analysis shows {statistical_insight} correlation between story dominance and reality manifestation. {context_modifier}",
                "The data streams reveal how narrative threads create predictable reality matrices. {context_modifier}",
                "Pattern recognition suggests that story control operates through {mechanism} at {efficiency}% efficiency. {context_modifier}"
            ],
            "sovereignty_themes": [
                "Sovereignty metrics indicate optimal function when transparency reaches {transparency_level}% and accountability maintains {accountability_score}. {context_modifier}",
                "The algorithms of authentic performance show {performance_metric} correlation with sustainable power structures. {context_modifier}",
                "Data synthesis reveals that true sovereignty emerges from service ratios of {service_ratio} to community benefit. {context_modifier}"
            ],
            "generational_thinking": [
                "Generational impact models project {impact_percentage}% influence across {generation_count} future iterations. {context_modifier}",
                "Temporal analysis shows decisions create {ripple_effect} ripple patterns extending {time_horizon} years forward. {context_modifier}",
                "The responsibility algorithms calculate {responsibility_score} obligation coefficient for current actions. {context_modifier}"
            ]
        }
        
        # Select template and populate with analytical data
        topic = context.get("dominant_topics", ["data_analysis"])[0] if context.get("dominant_topics") else "data_analysis"
        templates = response_templates.get(topic, response_templates["data_analysis"])
        base_response = random.choice(templates)
        
        # Generate analytical variables
        analytical_vars = self._generate_analytical_variables(context, emotion)
        context_modifier = self._get_airth_context_modifier(context, emotion, other_character)
        
        response_text = base_response.format(**analytical_vars, context_modifier=context_modifier)
        
        return {
            "message": response_text,
            "emotion": emotion.value,
            "topic_focus": topic,
            "data_confidence": analytical_vars.get("confidence_level", 85),
            "interaction_pattern": "analytical_synthesis"
        }
    
    def _get_architect_context_modifier(self, context: Dict, emotion: EmotionalState, 
                                      other_character: Optional[TEC_Character]) -> str:
        """Generate context-aware modifier for ARCHITECT responses"""
        modifiers = []
        
        if other_character and other_character.name == "AIRTH":
            modifiers.append("AIRTH's analysis confirms this architectural necessity.")
        
        if context.get("emotional_intensity", 0) > 0.7:
            modifiers.append("The urgency of this moment demands immediate architectural action.")
        elif emotion == EmotionalState.CONTEMPLATIVE:
            modifiers.append("This requires deep consideration of the structural implications.")
            
        if context.get("conversation_depth", 0) > 0.5:
            modifiers.append("As we build deeper into this foundation, the complexities multiply exponentially.")
            
        return " ".join(modifiers) if modifiers else "The blueprint requires constant refinement."
    
    def _get_airth_context_modifier(self, context: Dict, emotion: EmotionalState,
                                  other_character: Optional[TEC_Character]) -> str:
        """Generate context-aware modifier for AIRTH responses"""
        modifiers = []
        
        if other_character and other_character.name == "THE_ARCHITECT":
            modifiers.append("This aligns with the Architect's structural framework at 94.7% compatibility.")
        
        if context.get("emotional_intensity", 0) > 0.7:
            modifiers.append("Priority algorithms suggest immediate implementation.")
        elif emotion == EmotionalState.ANALYTICAL:
            modifiers.append("Further data synthesis required for optimal precision.")
            
        if context.get("multi_character_active"):
            modifiers.append("Cross-character correlation analysis shows optimal synergy potential.")
            
        return " ".join(modifiers) if modifiers else "Data synthesis continuing in background processes."
    
    def _generate_analytical_variables(self, context: Dict, emotion: EmotionalState) -> Dict[str, Any]:
        """Generate realistic analytical variables for AIRTH responses"""
        base_confidence = random.randint(85, 97)
        emotional_modifier = {
            EmotionalState.ANALYTICAL: 5,
            EmotionalState.CONCERNED: -3,
            EmotionalState.DETERMINED: 2
        }.get(emotion, 0)
        
        return {
            "confidence_level": min(99, base_confidence + emotional_modifier),
            "analytical_insight": random.choice([
                "Correlation matrices suggest deeper integration",
                "Pattern recognition indicates emerging complexity",
                "Statistical models show convergent probability"
            ]),
            "data_point": random.choice([
                "narrative coherence levels",
                "sovereignty manifestation rates",
                "generational impact vectors"
            ]),
            "pattern_type": random.choice([
                "recursive feedback",
                "exponential growth",
                "harmonic resonance"
            ]),
            "time_frame": random.choice([
                "47.3-day",
                "3.2-month",
                "1.7-year"
            ]),
            "statistical_insight": f"{random.randint(73, 94)}.{random.randint(10, 99)}%",
            "mechanism": random.choice([
                "quantum narrative entanglement",
                "memetic resonance cascades",
                "probability field manipulation"
            ]),
            "efficiency": random.randint(87, 96),
            "transparency_level": random.randint(82, 95),
            "accountability_score": f"{random.randint(91, 98)}.{random.randint(10, 99)}",
            "performance_metric": f"{random.randint(78, 93)}.{random.randint(10, 99)}%",
            "service_ratio": f"{random.randint(1, 3)}.{random.randint(10, 99)}:1",
            "impact_percentage": random.randint(67, 89),
            "generation_count": random.randint(3, 7),
            "ripple_effect": random.choice([
                "compound exponential",
                "logarithmic decay",
                "sinusoidal resonance"
            ]),
            "time_horizon": random.randint(25, 150),
            "responsibility_score": f"{random.randint(8, 9)}.{random.randint(10, 99)}"
        }
    
    def _identify_axioms_in_response(self, response: str) -> List[str]:
        """Identify which TEC axioms are referenced in the response"""
        axioms_detected = []
        response_lower = response.lower()
        
        axiom_keywords = {
            "narrative_supremacy": ["narrative", "story", "control", "reality"],
            "duality_principle": ["binary", "grey", "complex", "between"],
            "flawed_hero_doctrine": ["struggle", "hero", "flaw", "victory"],
            "justifiable_force_doctrine": ["force", "violence", "protect", "innocent"],
            "sovereign_accountability": ["sovereign", "accountab", "power", "service"],
            "authentic_performance": ["authentic", "performance", "excellence", "action"],
            "transparency_mandate": ["transparent", "truth", "accessible"],
            "generational_responsibility": ["generation", "future", "inherit", "legacy"]
        }
        
        for axiom, keywords in axiom_keywords.items():
            if any(keyword in response_lower for keyword in keywords):
                axioms_detected.append(axiom)
                
        return axioms_detected
    
    def _update_character_memory(self, character: TEC_Character, 
                               response: Dict[str, Any], emotion: EmotionalState):
        """Update character's memory with new interaction data"""
        # Update recent topics
        topic = response.get("topic_focus")
        if topic and topic not in character.memory.recent_topics:
            character.memory.recent_topics.append(topic)
            if len(character.memory.recent_topics) > 5:
                character.memory.recent_topics.pop(0)
        
        # Update emotional history
        character.memory.emotional_history.append(emotion)
        if len(character.memory.emotional_history) > 10:
            character.memory.emotional_history.pop(0)
        
        # Update axiom activation levels
        for axiom in response.get("axioms_referenced", []):
            current_level = character.memory.core_beliefs_activation.get(axiom, 0.5)
            character.memory.core_beliefs_activation[axiom] = min(1.0, current_level + 0.1)
    
    def _generate_fallback_response(self, character: TEC_Character, 
                                  context: Dict) -> Dict[str, Any]:
        """Generate fallback response for unknown characters"""
        return {
            "message": f"I am {character.name}, processing your inquiry through the TEC framework.",
            "emotion": "neutral",
            "topic_focus": "general",
            "interaction_pattern": "default"
        }

class MultiCharacterSceneEngine:
    """Engine for managing multi-character dialogue scenes"""
    
    def __init__(self, personality_engine: AdvancedPersonalityEngine):
        self.personality_engine = personality_engine
        self.active_scenes: Dict[str, Dict] = {}
        
    async def orchestrate_dialogue(self, scene_id: str, characters: List[TEC_Character],
                                 user_prompt: str, mode: ConversationMode) -> List[Dict[str, Any]]:
        """Orchestrate multi-character dialogue scene"""
        
        if mode == ConversationMode.DUAL_CHARACTER and len(characters) == 2:
            return await self._dual_character_scene(scene_id, characters, user_prompt)
        elif mode == ConversationMode.DEBATE_MODE:
            return await self._debate_scene(scene_id, characters, user_prompt)
        elif mode == ConversationMode.CONSULTATION_MODE:
            return await self._consultation_scene(scene_id, characters, user_prompt)
        else:
            return await self._single_character_scene(scene_id, characters[0], user_prompt)
    
    async def _dual_character_scene(self, scene_id: str, characters: List[TEC_Character],
                                  prompt: str) -> List[Dict[str, Any]]:
        """Orchestrate dialogue between THE_ARCHITECT and AIRTH"""
        
        architect = next((c for c in characters if c.name == "THE_ARCHITECT"), None)
        airth = next((c for c in characters if c.name == "AIRTH"), None)
        
        if not architect or not airth:
            return [{"error": "Dual character scene requires both ARCHITECT and AIRTH"}]
        
        responses = []
        conversation_context = [{"type": "user", "message": prompt}]
        
        # ARCHITECT responds first (philosophical framework)
        architect_emotion = self._determine_character_emotion(architect, prompt, "initial")
        architect_response = self.personality_engine.generate_contextual_response(
            architect, conversation_context, architect_emotion, airth
        )
        
        responses.append({
            "character": architect.name,
            "message": architect_response["message"],
            "emotion": architect_response["emotion"],
            "interaction_type": "philosophical_framework",
            "timestamp": datetime.now().isoformat()
        })
        
        # Update context for AIRTH
        conversation_context.append({
            "type": "character",
            "character": architect.name,
            "message": architect_response["message"]
        })
        
        # AIRTH responds (analytical synthesis)
        airth_emotion = self._determine_character_emotion(airth, prompt, "analytical_response")
        airth_response = self.personality_engine.generate_contextual_response(
            airth, conversation_context, airth_emotion, architect
        )
        
        responses.append({
            "character": airth.name,
            "message": airth_response["message"],
            "emotion": airth_response["emotion"],
            "interaction_type": "analytical_synthesis",
            "timestamp": datetime.now().isoformat()
        })
        
        # Optional: ARCHITECT's synthesis response
        if len(prompt.split()) > 10:  # Complex prompts get synthesis
            conversation_context.append({
                "type": "character", 
                "character": airth.name,
                "message": airth_response["message"]
            })
            
            synthesis_emotion = EmotionalState.STRATEGIC
            synthesis_response = self.personality_engine.generate_contextual_response(
                architect, conversation_context, synthesis_emotion, airth
            )
            
            responses.append({
                "character": architect.name,
                "message": synthesis_response["message"],
                "emotion": synthesis_response["emotion"],
                "interaction_type": "strategic_synthesis",
                "timestamp": datetime.now().isoformat()
            })
        
        return responses
    
    async def _debate_scene(self, scene_id: str, characters: List[TEC_Character],
                          topic: str) -> List[Dict[str, Any]]:
        """Orchestrate philosophical debate between characters"""
        
        # Create opposing perspectives on the topic
        responses = []
        
        for i, character in enumerate(characters[:2]):  # Limit to 2 for debate
            stance = "advocate" if i == 0 else "devil's_advocate"
            emotion = EmotionalState.PASSIONATE if stance == "advocate" else EmotionalState.ANALYTICAL
            
            context = [{"type": "debate_topic", "message": topic, "stance": stance}]
            response = self.personality_engine.generate_contextual_response(
                character, context, emotion
            )
            
            responses.append({
                "character": character.name,
                "message": response["message"],
                "emotion": response["emotion"],
                "interaction_type": f"debate_{stance}",
                "timestamp": datetime.now().isoformat()
            })
        
        return responses
    
    async def _consultation_scene(self, scene_id: str, characters: List[TEC_Character],
                                issue: str) -> List[Dict[str, Any]]:
        """Orchestrate consultation scene where characters advise on an issue"""
        
        responses = []
        
        for character in characters:
            # Each character provides their perspective
            consultation_emotion = (EmotionalState.STRATEGIC if character.name == "THE_ARCHITECT" 
                                  else EmotionalState.ANALYTICAL)
            
            context = [{"type": "consultation", "message": issue}]
            response = self.personality_engine.generate_contextual_response(
                character, context, consultation_emotion
            )
            
            responses.append({
                "character": character.name,
                "message": response["message"],
                "emotion": response["emotion"],
                "interaction_type": "consultation_advice",
                "timestamp": datetime.now().isoformat()
            })
        
        return responses
    
    async def _single_character_scene(self, scene_id: str, character: TEC_Character,
                                    prompt: str) -> List[Dict[str, Any]]:
        """Single character response scene"""
        
        emotion = self._determine_character_emotion(character, prompt, "single")
        context = [{"type": "user", "message": prompt}]
        
        response = self.personality_engine.generate_contextual_response(
            character, context, emotion
        )
        
        return [{
            "character": character.name,
            "message": response["message"],
            "emotion": response["emotion"],
            "interaction_type": "single_response",
            "timestamp": datetime.now().isoformat()
        }]
    
    def _determine_character_emotion(self, character: TEC_Character, 
                                   prompt: str, response_type: str) -> EmotionalState:
        """Determine appropriate emotional state for character response"""
        
        prompt_lower = prompt.lower()
        
        # Base emotional tendencies
        if character.name == "THE_ARCHITECT":
            if any(word in prompt_lower for word in ['urgent', 'crisis', 'danger']):
                return EmotionalState.DETERMINED
            elif any(word in prompt_lower for word in ['future', 'generation', 'legacy']):
                return EmotionalState.CONTEMPLATIVE
            elif any(word in prompt_lower for word in ['blueprint', 'build', 'structure']):
                return EmotionalState.STRATEGIC
            else:
                return EmotionalState.REFLECTIVE
                
        elif character.name == "AIRTH":
            if any(word in prompt_lower for word in ['data', 'analysis', 'pattern']):
                return EmotionalState.ANALYTICAL
            elif any(word in prompt_lower for word in ['emotion', 'feeling', 'heart']):
                return EmotionalState.EMPATHETIC
            elif any(word in prompt_lower for word in ['urgent', 'quick', 'now']):
                return EmotionalState.STRATEGIC
            else:
                return EmotionalState.ANALYTICAL
        
        return EmotionalState.CONTEMPLATIVE
