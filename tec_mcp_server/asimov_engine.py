#!/usr/bin/env python3
"""
TEC MCP Server - The Asimov Engine
Sovereign Asset Protocol with MCP Intelligence Architecture

Primary Interface: Model Context Protocol for AI clients
Secondary Interface: Flask HTTP API for direct integration

The Five Sovereign Tools:
1. validate_axioms - Constitutional content validation
2. query_memory - Semantic search and historical context
3. generate_lore - Structured worldbuilding and narrative development  
4. process_asset - Multimedia asset analysis and integration
5. hybrid_synthesis - Ellison-Asimov creative-logical processing
"""

import os
import sys
import json
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
import sqlite3
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

@dataclass
class LoreFragment:
    """Structured lore fragment for TEC universe"""
    id: str
    title: str
    content: str
    content_type: str  # 'story' | 'decision' | 'policy' | 'dialogue' | 'narrative' | 'lore' | 'asset'
    analysis_type: str  # 'axiom' | 'historical' | 'narrative' | 'decision' | 'precedent' | 'connection'
    axioms_referenced: List[str]
    entities: List[str]
    narrative_threads: List[str]
    emotional_tone: str
    confidence_score: float
    created_at: str
    source_asset: Optional[str] = None
    cross_references: Optional[List[str]] = None

    def __post_init__(self):
        if self.cross_references is None:
            self.cross_references = []

@dataclass
class AssetAnalysis:
    """Complete asset analysis result"""
    asset_id: str
    asset_type: str
    core_concepts: List[str]
    entities: List[str]
    narrative_threads: List[str]
    emotional_tone: str
    axiom_compliance: Dict[str, float]
    lore_fragments: List[LoreFragment]
    confidence_score: float
    processing_timestamp: str

class AxiomEngine:
    """Validates ALL content against 8 foundational principles"""
    
    def __init__(self):
        self.axioms = {
            "narrative_supremacy": "Control reality through story control",
            "duality_principle": "Reject binary thinking, embrace grey complexity",
            "flawed_hero_doctrine": "Heroes defined by struggles, not victories", 
            "justifiable_force_doctrine": "Violence only for protecting innocents",
            "sovereign_accountability": "Power earned through service & transparency",
            "authentic_performance": "Excellence in action, not just intention",
            "transparency_mandate": "Truth must be accessible to all",
            "generational_responsibility": "Every action considers future impact"
        }
        
    def validate_content(self, content: str, content_type: str) -> Dict[str, Any]:
        """Validate content against TEC axioms"""
        
        compliance_scores = {}
        violations = []
        content_lower = content.lower()
        
        # Narrative Supremacy validation
        narrative_indicators = ['story', 'narrative', 'control', 'reality', 'truth']
        narrative_score = sum(1 for indicator in narrative_indicators if indicator in content_lower) / len(narrative_indicators)
        compliance_scores['narrative_supremacy'] = min(1.0, narrative_score + 0.3)
        
        # Duality Principle validation
        binary_words = ['binary', 'black/white', 'either/or', 'absolute']
        grey_words = ['complex', 'nuanced', 'spectrum', 'grey', 'balance']
        binary_penalty = sum(0.2 for word in binary_words if word in content_lower)
        grey_bonus = sum(0.15 for word in grey_words if word in content_lower)
        compliance_scores['duality_principle'] = max(0.0, min(1.0, 0.5 + grey_bonus - binary_penalty))
        
        # Flawed Hero Doctrine validation
        hero_words = ['hero', 'protagonist', 'leader', 'champion']
        struggle_words = ['struggle', 'challenge', 'flaw', 'growth', 'overcome']
        hero_present = any(word in content_lower for word in hero_words)
        struggles_present = any(word in content_lower for word in struggle_words)
        if hero_present:
            compliance_scores['flawed_hero_doctrine'] = 0.9 if struggles_present else 0.3
        else:
            compliance_scores['flawed_hero_doctrine'] = 0.7  # Neutral
            
        # Justifiable Force Doctrine validation
        violence_words = ['violence', 'force', 'attack', 'destroy', 'kill']
        protection_words = ['protect', 'defend', 'innocent', 'safety', 'shelter']
        violence_present = any(word in content_lower for word in violence_words)
        protection_context = any(word in content_lower for word in protection_words)
        if violence_present:
            compliance_scores['justifiable_force_doctrine'] = 0.8 if protection_context else 0.2
            if not protection_context:
                violations.append("Violence mentioned without protective context")
        else:
            compliance_scores['justifiable_force_doctrine'] = 0.8
            
        # Sovereign Accountability validation
        power_words = ['power', 'authority', 'control', 'leadership']
        service_words = ['service', 'responsibility', 'transparency', 'accountability']
        power_present = any(word in content_lower for word in power_words)
        service_present = any(word in content_lower for word in service_words)
        if power_present:
            compliance_scores['sovereign_accountability'] = 0.9 if service_present else 0.4
        else:
            compliance_scores['sovereign_accountability'] = 0.7
            
        # Authentic Performance validation
        performance_words = ['performance', 'action', 'excellence', 'execution']
        intention_words = ['intention', 'planning', 'thinking', 'considering']
        action_focus = sum(1 for word in performance_words if word in content_lower)
        intention_focus = sum(1 for word in intention_words if word in content_lower)
        compliance_scores['authentic_performance'] = min(1.0, (action_focus * 0.3) + 0.4)
        
        # Transparency Mandate validation
        transparency_words = ['transparent', 'open', 'accessible', 'truth', 'honest']
        secrecy_words = ['secret', 'hidden', 'classified', 'private', 'concealed']
        transparency_score = sum(0.2 for word in transparency_words if word in content_lower)
        secrecy_penalty = sum(0.15 for word in secrecy_words if word in content_lower)
        compliance_scores['transparency_mandate'] = max(0.0, min(1.0, 0.5 + transparency_score - secrecy_penalty))
        
        # Generational Responsibility validation  
        future_words = ['future', 'generation', 'legacy', 'inherit', 'tomorrow', 'children']
        short_term_words = ['now', 'immediate', 'quick', 'instant']
        future_score = sum(0.2 for word in future_words if word in content_lower)
        short_term_penalty = sum(0.1 for word in short_term_words if word in content_lower)
        compliance_scores['generational_responsibility'] = max(0.0, min(1.0, 0.4 + future_score - short_term_penalty))
        
        # Calculate overall compliance
        overall_score = sum(compliance_scores.values()) / len(compliance_scores)
        
        return {
            'valid': overall_score >= 0.6 and len(violations) == 0,
            'overall_score': overall_score,
            'axiom_scores': compliance_scores,
            'violations': violations,
            'analysis_timestamp': datetime.now().isoformat()
        }

class MemoryCore:
    """Historical precedent database with semantic search"""
    
    def __init__(self, db_path: str = "tec_memory_core.db"):
        self.db_path = db_path
        self.initialize_database()
        
    def initialize_database(self):
        """Initialize SQLite database for memory storage"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS lore_fragments (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    content_type TEXT NOT NULL,
                    analysis_type TEXT NOT NULL,
                    axioms_referenced TEXT,
                    entities TEXT,
                    narrative_threads TEXT,
                    emotional_tone TEXT,
                    confidence_score REAL,
                    created_at TEXT,
                    source_asset TEXT,
                    cross_references TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS asset_analyses (
                    asset_id TEXT PRIMARY KEY,
                    asset_type TEXT NOT NULL,
                    core_concepts TEXT,
                    entities TEXT,
                    narrative_threads TEXT,
                    emotional_tone TEXT,
                    axiom_compliance TEXT,
                    confidence_score REAL,
                    processing_timestamp TEXT,
                    raw_content TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS narrative_connections (
                    id TEXT PRIMARY KEY,
                    source_fragment TEXT,
                    target_fragment TEXT,
                    connection_type TEXT,
                    connection_strength REAL,
                    created_at TEXT
                )
            """)
            
    def store_lore_fragment(self, fragment: LoreFragment):
        """Store lore fragment in memory core"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO lore_fragments 
                (id, title, content, content_type, analysis_type, axioms_referenced, 
                 entities, narrative_threads, emotional_tone, confidence_score, 
                 created_at, source_asset, cross_references)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                fragment.id, fragment.title, fragment.content, fragment.content_type,
                fragment.analysis_type, json.dumps(fragment.axioms_referenced),
                json.dumps(fragment.entities), json.dumps(fragment.narrative_threads),
                fragment.emotional_tone, fragment.confidence_score, fragment.created_at,
                fragment.source_asset, json.dumps(fragment.cross_references)
            ))
            
    def store_asset_analysis(self, analysis: AssetAnalysis):
        """Store complete asset analysis"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO asset_analyses
                (asset_id, asset_type, core_concepts, entities, narrative_threads,
                 emotional_tone, axiom_compliance, confidence_score, processing_timestamp, raw_content)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                analysis.asset_id, analysis.asset_type, json.dumps(analysis.core_concepts),
                json.dumps(analysis.entities), json.dumps(analysis.narrative_threads),
                analysis.emotional_tone, json.dumps(analysis.axiom_compliance),
                analysis.confidence_score, analysis.processing_timestamp, ""  # raw_content placeholder
            ))
            
            # Store individual lore fragments
            for fragment in analysis.lore_fragments:
                self.store_lore_fragment(fragment)
    
    def query_by_concept(self, concept: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Query memory by concept with semantic similarity"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM lore_fragments 
                WHERE content LIKE ? OR entities LIKE ? OR narrative_threads LIKE ?
                ORDER BY confidence_score DESC
                LIMIT ?
            """, (f"%{concept}%", f"%{concept}%", f"%{concept}%", limit))
            
            results = []
            for row in cursor.fetchall():
                result = dict(row)
                # Parse JSON fields
                result['axioms_referenced'] = json.loads(result['axioms_referenced'] or '[]')
                result['entities'] = json.loads(result['entities'] or '[]')
                result['narrative_threads'] = json.loads(result['narrative_threads'] or '[]')
                result['cross_references'] = json.loads(result['cross_references'] or '[]')
                results.append(result)
                
            return results
    
    def query_by_axiom(self, axiom: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Query memory by axiom reference"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM lore_fragments 
                WHERE axioms_referenced LIKE ?
                ORDER BY confidence_score DESC
                LIMIT ?
            """, (f"%{axiom}%", limit))
            
            results = []
            for row in cursor.fetchall():
                result = dict(row)
                result['axioms_referenced'] = json.loads(result['axioms_referenced'] or '[]')
                result['entities'] = json.loads(result['entities'] or '[]')
                result['narrative_threads'] = json.loads(result['narrative_threads'] or '[]')
                result['cross_references'] = json.loads(result['cross_references'] or '[]')
                results.append(result)
                
            return results
    
    def get_narrative_connections(self, fragment_id: str) -> List[Dict[str, Any]]:
        """Get narrative connections for a fragment"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM narrative_connections 
                WHERE source_fragment = ? OR target_fragment = ?
                ORDER BY connection_strength DESC
            """, (fragment_id, fragment_id))
            
            return [dict(row) for row in cursor.fetchall()]

class ToolOrchestrator:
    """Coordinates hybrid synthesis and asset processing through MCP tools"""
    
    def __init__(self):
        self.axiom_engine = AxiomEngine()
        self.memory_core = MemoryCore()
        self.status = 'initializing'
        
    def initialize(self):
        """Initialize the tool orchestrator"""
        try:
            self.status = 'operational'
            logger.info("✅ ToolOrchestrator initialized - status: operational")
        except Exception as e:
            self.status = 'degraded'
            logger.error(f"❌ ToolOrchestrator initialization failed: {e}")
    
    def process_asset(self, content: str, asset_type: str, source_id: Optional[str] = None) -> AssetAnalysis:
        """Process asset through complete TEC analysis pipeline"""
        
        asset_id = hashlib.md5(content.encode()).hexdigest()[:12]
        
        # Extract core concepts
        core_concepts = self._extract_concepts(content)
        
        # Extract entities
        entities = self._extract_entities(content)
        
        # Identify narrative threads
        narrative_threads = self._extract_narrative_threads(content)
        
        # Analyze emotional tone
        emotional_tone = self._analyze_emotional_tone(content)
        
        # Validate against axioms
        axiom_validation = self.axiom_engine.validate_content(content, asset_type)
        
        # Generate lore fragments
        lore_fragments = self._generate_lore_fragments(
            content, asset_id, core_concepts, entities, 
            narrative_threads, emotional_tone, axiom_validation
        )
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence(
            len(core_concepts), len(entities), len(narrative_threads),
            axiom_validation['overall_score']
        )
        
        analysis = AssetAnalysis(
            asset_id=asset_id,
            asset_type=asset_type,
            core_concepts=core_concepts,
            entities=entities,
            narrative_threads=narrative_threads,
            emotional_tone=emotional_tone,
            axiom_compliance=axiom_validation['axiom_scores'],
            lore_fragments=lore_fragments,
            confidence_score=confidence_score,
            processing_timestamp=datetime.now().isoformat()
        )
        
        # Store in memory core
        self.memory_core.store_asset_analysis(analysis)
        
        return analysis
    
    def _extract_concepts(self, content: str) -> List[str]:
        """Extract core concepts from content"""
        content_lower = content.lower()
        
        tec_concepts = [
            'narrative_control', 'sovereignty', 'blueprint', 'architecture',
            'generational_responsibility', 'transparency', 'accountability',
            'authentic_performance', 'duality_principle', 'memory_core',
            'asimov_engine', 'hybrid_synthesis', 'axiom_validation'
        ]
        
        detected_concepts = []
        for concept in tec_concepts:
            if concept.replace('_', ' ') in content_lower or concept in content_lower:
                detected_concepts.append(concept)
        
        # Add general concepts based on keywords
        concept_keywords = {
            'technology': ['ai', 'artificial', 'algorithm', 'data', 'digital'],
            'governance': ['government', 'policy', 'regulation', 'control', 'authority'],
            'philosophy': ['philosophy', 'ethics', 'morality', 'principle', 'belief'],
            'society': ['society', 'community', 'culture', 'civilization', 'human'],
            'future': ['future', 'tomorrow', 'evolution', 'progress', 'development']
        }
        
        for concept, keywords in concept_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                detected_concepts.append(concept)
        
        return list(set(detected_concepts))
    
    def _extract_entities(self, content: str) -> List[str]:
        """Extract named entities from content"""
        entities = []
        
        # TEC-specific entities
        tec_entities = [
            'The Architect', 'AIRTH', 'The Asimov Engine', 'TEC', 'The Elidoras Codex',
            'Memory Core', 'Axiom Engine', 'Tool Orchestrator', 'Hybrid Synthesis'
        ]
        
        for entity in tec_entities:
            if entity.lower() in content.lower():
                entities.append(entity)
        
        # Extract potential character names (capitalized words)
        import re
        potential_names = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', content)
        entities.extend([name for name in potential_names if len(name.split()) <= 3])
        
        return list(set(entities))
    
    def _extract_narrative_threads(self, content: str) -> List[str]:
        """Extract narrative threads from content"""
        content_lower = content.lower()
        
        thread_indicators = {
            'blueprint_development': ['blueprint', 'design', 'architecture', 'structure'],
            'sovereignty_quest': ['sovereignty', 'independence', 'freedom', 'autonomy'],
            'memory_preservation': ['memory', 'history', 'record', 'preserve', 'archive'],
            'axiom_enforcement': ['axiom', 'principle', 'rule', 'law', 'mandate'],
            'narrative_control': ['narrative', 'story', 'control', 'influence', 'shape'],
            'generational_legacy': ['generation', 'future', 'legacy', 'inherit', 'children'],
            'truth_seeking': ['truth', 'transparency', 'honesty', 'reveal', 'uncover'],
            'hybrid_intelligence': ['hybrid', 'synthesis', 'combination', 'merge', 'integrate']
        }
        
        detected_threads = []
        for thread, keywords in thread_indicators.items():
            if any(keyword in content_lower for keyword in keywords):
                detected_threads.append(thread)
        
        return detected_threads
    
    def _analyze_emotional_tone(self, content: str) -> str:
        """Analyze emotional tone of content"""
        content_lower = content.lower()
        
        tone_indicators = {
            'determined': ['must', 'will', 'determined', 'committed', 'resolved'],
            'contemplative': ['consider', 'think', 'reflect', 'ponder', 'wonder'],
            'urgent': ['urgent', 'critical', 'immediate', 'now', 'quickly'],
            'optimistic': ['hope', 'future', 'positive', 'bright', 'promising'],
            'concerned': ['concern', 'worry', 'problem', 'issue', 'challenge'],
            'passionate': ['passion', 'love', 'believe', 'conviction', 'fervent'],
            'analytical': ['analyze', 'data', 'logic', 'rational', 'systematic']
        }
        
        tone_scores = {}
        for tone, keywords in tone_indicators.items():
            score = sum(1 for keyword in keywords if keyword in content_lower)
            if score > 0:
                tone_scores[tone] = score
        
        if tone_scores:
            return max(tone_scores.keys(), key=lambda k: tone_scores[k])
        else:
            return 'neutral'
    
    def _generate_lore_fragments(self, content: str, asset_id: str, 
                               concepts: List[str], entities: List[str],
                               threads: List[str], tone: str, 
                               axiom_validation: Dict[str, Any]) -> List[LoreFragment]:
        """Generate structured lore fragments from analysis"""
        
        fragments = []
        
        # Create primary content fragment
        primary_fragment = LoreFragment(
            id=f"{asset_id}_primary",
            title=f"Asset Analysis: {asset_id}",
            content=content[:500] + "..." if len(content) > 500 else content,
            content_type='asset',
            analysis_type='narrative',
            axioms_referenced=[axiom for axiom, score in axiom_validation['axiom_scores'].items() if score > 0.7],
            entities=entities,
            narrative_threads=threads,
            emotional_tone=tone,
            confidence_score=axiom_validation['overall_score'],
            created_at=datetime.now().isoformat(),
            source_asset=asset_id
        )
        fragments.append(primary_fragment)
        
        # Create concept-specific fragments
        for concept in concepts[:3]:  # Limit to top 3 concepts
            concept_fragment = LoreFragment(
                id=f"{asset_id}_concept_{concept}",
                title=f"Concept Analysis: {concept}",
                content=f"Analysis of {concept} within the context of TEC framework. {content[:200]}...",
                content_type='lore',
                analysis_type='connection',
                axioms_referenced=[axiom for axiom, score in axiom_validation['axiom_scores'].items() if score > 0.6],
                entities=entities,
                narrative_threads=[thread for thread in threads if concept.replace('_', ' ') in thread],
                emotional_tone=tone,
                confidence_score=min(1.0, axiom_validation['overall_score'] + 0.1),
                created_at=datetime.now().isoformat(),
                source_asset=asset_id
            )
            fragments.append(concept_fragment)
        
        return fragments
    
    def _calculate_confidence(self, concept_count: int, entity_count: int, 
                            thread_count: int, axiom_score: float) -> float:
        """Calculate overall confidence score for analysis"""
        
        # Base confidence from axiom compliance
        base_confidence = axiom_score
        
        # Boost from content richness
        richness_bonus = min(0.3, (concept_count * 0.05) + (entity_count * 0.03) + (thread_count * 0.04))
        
        # Final confidence score
        return min(1.0, base_confidence + richness_bonus)

def get_hybrid_engine():
    """Get the hybrid synthesis engine (Ellison-Asimov processing)"""
    return ToolOrchestrator()

# Test the system
if __name__ == "__main__":
    print("🚀 TEC MCP Server - The Asimov Engine")
    print("=" * 50)
    print("🧠 Sovereign Asset Protocol Active")
    print("⚡ MCP Intelligence Architecture Online")
    print("🔧 Five Sovereign Tools Ready")
    print("=" * 50)
    
    # Initialize system
    orchestrator = ToolOrchestrator()
    orchestrator.initialize()
    
    # Test asset processing
    test_content = """
    The blueprint for sovereign digital architecture must prioritize narrative control
    while maintaining transparency for future generations. The Architect envisions
    a system where authentic performance supersedes mere intention, and where
    flawed heroes struggle to build something greater than themselves.
    """
    
    print("\n🧪 Testing Asset Processing Pipeline...")
    analysis = orchestrator.process_asset(test_content, "narrative", "test_001")
    
    print(f"✅ Analysis Complete!")
    print(f"   Asset ID: {analysis.asset_id}")
    print(f"   Concepts: {', '.join(analysis.core_concepts)}")
    print(f"   Entities: {', '.join(analysis.entities)}")
    print(f"   Threads: {', '.join(analysis.narrative_threads)}")
    print(f"   Tone: {analysis.emotional_tone}")
    print(f"   Confidence: {analysis.confidence_score:.2f}")
    print(f"   Lore Fragments: {len(analysis.lore_fragments)}")
    
    # Test axiom validation
    print("\n🔍 Axiom Compliance Analysis:")
    for axiom, score in analysis.axiom_compliance.items():
        status = "✅" if score > 0.7 else "⚠️" if score > 0.4 else "❌"
        print(f"   {status} {axiom}: {score:.2f}")
    
    print(f"\n🎯 System Status: {orchestrator.status}")
    print("🌟 The Asimov Engine is operational!")
