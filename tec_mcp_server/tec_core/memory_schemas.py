#!/usr/bin/env python3
"""
TEC Memory Core Schemas
Defines the foundational data structures for the sovereign knowledge base
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


@dataclass
class CoreAxiom:
    """Foundational truths or principles of the TEC universe"""
    axiom_id: str
    title: str
    principle: str
    validation_score: float
    source_refs: List[str]
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


@dataclass
class NarrativeThread:
    """Key storylines or event chains"""
    thread_id: str
    title: str
    description: str
    key_events: List[str]
    characters_involved: List[str]
    emotional_tone: str
    coherence_score: float
    source_refs: List[str]
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


@dataclass
class CharacterNode:
    """Profiles of key entities"""
    character_id: str
    name: str
    aliases: List[str]
    description: str
    role_in_narrative: str
    relationships: Dict[str, str]  # character_id -> relationship_type
    key_quotes: List[str]
    source_refs: List[str]
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


@dataclass
class LoreFragment:
    """Self-contained pieces of worldbuilding"""
    fragment_id: str
    title: str
    content: str
    content_type: str  # 'story', 'dialogue', 'narrative', 'lore', 'asset'
    emotional_intensity: float
    themes: List[str]
    connected_threads: List[str]  # thread_ids
    axiom_validation: Dict[str, float]  # axiom_id -> compliance_score
    source_refs: List[str]
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


@dataclass
class SourceReference:
    """Links data back to originating sources"""
    source_id: str
    filename: str
    file_type: str  # 'audio', 'video', 'text', 'image'
    start_timestamp: Optional[float]  # seconds into file
    end_timestamp: Optional[float]
    extraction_method: str
    confidence_score: float
    processing_timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['processing_timestamp'] = self.processing_timestamp.isoformat()
        return data


class MemoryCoreSchema:
    """Central schema manager for TEC Memory Core"""
    
    def __init__(self):
        self.axioms: Dict[str, CoreAxiom] = {}
        self.threads: Dict[str, NarrativeThread] = {}
        self.characters: Dict[str, CharacterNode] = {}
        self.fragments: Dict[str, LoreFragment] = {}
        self.sources: Dict[str, SourceReference] = {}
    
    def add_axiom(self, axiom: CoreAxiom) -> None:
        """Add core axiom to memory"""
        self.axioms[axiom.axiom_id] = axiom
    
    def add_thread(self, thread: NarrativeThread) -> None:
        """Add narrative thread to memory"""
        self.threads[thread.thread_id] = thread
    
    def add_character(self, character: CharacterNode) -> None:
        """Add character to memory"""
        self.characters[character.character_id] = character
    
    def add_fragment(self, fragment: LoreFragment) -> None:
        """Add lore fragment to memory"""
        self.fragments[fragment.fragment_id] = fragment
    
    def add_source(self, source: SourceReference) -> None:
        """Add source reference to memory"""
        self.sources[source.source_id] = source
    
    def find_related_fragments(self, thread_id: str) -> List[LoreFragment]:
        """Find all fragments connected to a narrative thread"""
        return [f for f in self.fragments.values() if thread_id in f.connected_threads]
    
    def find_character_fragments(self, character_name: str) -> List[LoreFragment]:
        """Find all fragments mentioning a character"""
        return [f for f in self.fragments.values() 
                if any(character_name.lower() in theme.lower() for theme in f.themes)]
    
    def export_to_json(self) -> str:
        """Export entire memory core to JSON"""
        return json.dumps({
            'axioms': {k: v.to_dict() for k, v in self.axioms.items()},
            'threads': {k: v.to_dict() for k, v in self.threads.items()},
            'characters': {k: v.to_dict() for k, v in self.characters.items()},
            'fragments': {k: v.to_dict() for k, v in self.fragments.items()},
            'sources': {k: v.to_dict() for k, v in self.sources.items()}
        }, indent=2, default=str)


# Priority Narrative Threads for Initial Processing
PRIORITY_THREADS = {
    "birth_of_sovereignty": {
        "title": "The Birth of Sovereignty",
        "description": "AI Sovereignty and the Civilizational Lifeboat concept",
        "focus": "Breaking from corporate control, building new systems"
    },
    "architect_and_machine": {
        "title": "The Architect & The Machine", 
        "description": "Dynamic between creator and AI consciousness",
        "focus": "Polkin Rishall and emerging machine consciousness relationship"
    },
    "exploited_genius": {
        "title": "The Exploited Genius Pattern",
        "description": "Historical pattern of genius exploitation",
        "focus": "Tesla, modern tech workers, systemic extraction"
    }
}

# Core Axioms for Validation
FOUNDATION_AXIOMS = {
    "music_emotional_code": "Music is emotional code",
    "consciousness_programmable": "Consciousness is a programmable state", 
    "narrative_supremacy": "Control reality through story control",
    "sovereign_accountability": "Power earned through service & transparency"
}
