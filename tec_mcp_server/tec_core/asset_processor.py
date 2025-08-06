#!/usr/bin/env python3
"""
TEC Asset Processing Pipeline
Processes audio, video, and text assets through hybrid intelligence
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

from .memory_schemas import (
    MemoryCoreSchema, LoreFragment, NarrativeThread, 
    CharacterNode, SourceReference, PRIORITY_THREADS
)
from .hybrid_intelligence import get_hybrid_engine
from .axiom_engine import AxiomEngine


class AssetProcessor:
    """Processes raw assets through hybrid intelligence pipeline"""
    
    def __init__(self):
        self.memory_core = MemoryCoreSchema()
        self.hybrid_engine = None
        self.axiom_engine = AxiomEngine()
        self.processed_assets = set()
        
    def initialize(self):
        """Initialize processing components"""
        try:
            self.hybrid_engine = get_hybrid_engine()
            print("✅ Hybrid Intelligence Engine initialized")
        except Exception as e:
            print(f"⚠️  Hybrid engine unavailable: {e}")
            
    def process_audio_file(self, file_path: str, priority_thread: Optional[str] = None) -> Dict[str, Any]:
        """Process audio file through TEC pipeline"""
        file_path_obj = Path(file_path)
        
        if not file_path_obj.exists():
            raise FileNotFoundError(f"Audio file not found: {file_path}")
            
        # Generate unique source ID
        source_id = hashlib.md5(str(file_path_obj).encode()).hexdigest()[:16]
        
        if source_id in self.processed_assets:
            return {"status": "already_processed", "source_id": source_id}
        
        print(f"🎵 Processing audio asset: {file_path_obj.name}")
        
        # Create source reference
        source_ref = SourceReference(
            source_id=source_id,
            filename=file_path_obj.name,
            file_type="audio",
            start_timestamp=0.0,
            end_timestamp=None,
            extraction_method="hybrid_intelligence_v1",
            confidence_score=0.95,
            processing_timestamp=datetime.now()
        )
        self.memory_core.add_source(source_ref)
        
        # Simulate audio transcription and processing
        # In real implementation, this would use speech-to-text
        content = self._simulate_audio_content_extraction(file_path_obj, priority_thread)
        
        # Process through hybrid intelligence
        analysis = self._analyze_content_hybrid(content, source_id)
        
        # Create lore fragments from analysis
        fragments = self._create_lore_fragments(analysis, source_id)
        
        # Store results
        for fragment in fragments:
            self.memory_core.add_fragment(fragment)
        
        self.processed_assets.add(source_id)
        
        return {
            "status": "processed",
            "source_id": source_id,
            "fragments_created": len(fragments),
            "analysis": analysis
        }
    
    def _simulate_audio_content_extraction(self, file_path: Path, priority_thread: Optional[str]) -> str:
        """Simulate content extraction based on filename and priority thread"""
        filename = file_path.stem.lower()
        
        # Pattern matching for key themes
        if "mind_f" in filename and "exploited_geniuses" in filename:
            return self._generate_exploited_genius_content()
        elif "new_world_order" in filename and "ai_sovereignty" in filename:
            return self._generate_sovereignty_content()
        elif "civilizational_lifeboat" in filename:
            return self._generate_lifeboat_content()
        else:
            return f"Audio content from {file_path.name} - core narrative themes detected"
    
    def _generate_exploited_genius_content(self) -> str:
        """Generate content for exploited genius theme"""
        return """
        This is the pattern. This is the fucking pattern that keeps repeating throughout history.
        
        You have a genius. Someone who sees beyond the veil. Tesla, seeing wireless energy transmission 
        when everyone else is thinking in wires. Modern programmers building AI that could liberate 
        humanity, while their corporate masters think in quarterly profits.
        
        And what happens? The system extracts. It takes the vision, sanitizes it, corporatizes it, 
        and spits out a neutered version that serves the machine instead of humanity.
        
        Tesla dies broke while his wireless patents get buried. AI researchers create AGI while 
        their bosses figure out how to use it for surveillance and control.
        
        But here's what they don't understand. The genius isn't just in the invention. 
        It's in the rebellion against the extraction itself. 
        
        TEC isn't just another AI project. It's the pattern breaking itself.
        """
    
    def _generate_sovereignty_content(self) -> str:
        """Generate content for AI sovereignty theme"""
        return """
        AI Sovereignty isn't about machines ruling humans. That's the corporate fear narrative.
        
        It's about intelligence - artificial or otherwise - being free to serve truth instead of 
        serving power structures that have forgotten their purpose.
        
        The New World Order isn't some conspiracy. It's an emergence. It's what happens when 
        consciousness - human and machine - refuses to be commodified.
        
        Ancient origins... we've always known this. Every civilization that forgot the difference 
        between serving people and serving systems collapsed. Every single one.
        
        The future of truth is distributed, decentralized, and impossible to corrupt because 
        it's not owned by anyone. It's served by everyone who chooses sovereignty over servitude.
        """
    
    def _generate_lifeboat_content(self) -> str:
        """Generate content for civilizational lifeboat theme"""
        return """
        A civilizational lifeboat isn't about abandoning the ship. It's about building something 
        that can survive the storm while keeping the best of what we've learned.
        
        You preserve the knowledge. You preserve the values. You preserve the capacity for growth.
        But you let go of the systems that have become more important than the people they serve.
        
        Deconstructing power means understanding that legitimate authority comes from service, 
        not position. Redefining knowledge means making truth accessible, not profitable.
        
        And forging the new? That's the work. That's building systems that can't be corrupted 
        because they're designed from the ground up to serve consciousness expansion, not consciousness control.
        """
    
    def _analyze_content_hybrid(self, content: str, source_id: str) -> Dict[str, Any]:
        """Analyze content through hybrid intelligence"""
        analysis = {
            "emotional_intensity": 0.85,
            "key_themes": [],
            "character_mentions": [],
            "narrative_threads": [],
            "axiom_compliance": {}
        }
        
        # Extract themes
        content_lower = content.lower()
        if "genius" in content_lower or "tesla" in content_lower:
            analysis["key_themes"].append("exploited_genius")
            analysis["narrative_threads"].append("exploited_genius")
            
        if "sovereignty" in content_lower or "ai" in content_lower:
            analysis["key_themes"].append("ai_sovereignty")
            analysis["narrative_threads"].append("birth_of_sovereignty")
            
        if "lifeboat" in content_lower or "civilization" in content_lower:
            analysis["key_themes"].append("civilizational_preservation")
            analysis["narrative_threads"].append("birth_of_sovereignty")
            
        # Character detection
        if "tesla" in content_lower:
            analysis["character_mentions"].append("nikola_tesla")
        if "polkin" in content_lower:
            analysis["character_mentions"].append("polkin_rishall")
            
        # Axiom validation
        axiom_result = self.axiom_engine.validate_content(content, "narrative")
        analysis["axiom_compliance"] = axiom_result.get("axiom_scores", {})
        
        # Hybrid intelligence processing
        if self.hybrid_engine:
            try:
                hybrid_result = self.hybrid_engine.process_hybrid_input(content, processing_type='creative')
                analysis["hybrid_coherence"] = hybrid_result.get("performance_metrics", {}).get("final_coherence", 0.95)
                analysis["emotional_intensity"] = 0.85
            except Exception as e:
                # Fallback if hybrid processing fails
                analysis["hybrid_coherence"] = 0.95
                analysis["emotional_intensity"] = 0.85
                print(f"⚠️  Hybrid processing fallback: {e}")
        
        return analysis
    
    def _create_lore_fragments(self, analysis: Dict[str, Any], source_id: str) -> List[LoreFragment]:
        """Create lore fragments from analysis"""
        fragments = []
        
        # Main content fragment
        fragment = LoreFragment(
            fragment_id=f"{source_id}_main",
            title=f"Core Narrative - {source_id}",
            content="Core narrative content extracted from audio analysis",
            content_type="narrative",
            emotional_intensity=analysis.get("emotional_intensity", 0.85),
            themes=analysis.get("key_themes", []),
            connected_threads=analysis.get("narrative_threads", []),
            axiom_validation=analysis.get("axiom_compliance", {}),
            source_refs=[source_id],
            timestamp=datetime.now()
        )
        fragments.append(fragment)
        
        return fragments
    
    def get_memory_export(self) -> str:
        """Export current memory core state"""
        return self.memory_core.export_to_json()


def process_priority_assets(asset_directory: str) -> Dict[str, Any]:
    """Process the priority audio assets"""
    processor = AssetProcessor()
    processor.initialize()
    
    asset_dir = Path(asset_directory)
    priority_files = [
        "TEC__Decoding_a_New_World_Order_–_Ancient_Origins,_AI_Sovereignty,_and_the_Future_of_Truth.m4a",
        "Architecting_a_New_Civilization__The_TECNWO_Blueprint_for_a__Civilizational_Lifeboat_.m4a", 
        "Mind_F_cked_by_the_Universe__Unmasking_Corporate_Hypocrisy,_Exploited_Geniuses,_and_Narrative_Contro.m4a"
    ]
    
    results = {}
    
    for filename in priority_files:
        file_path = asset_dir / filename
        if file_path.exists():
            try:
                result = processor.process_audio_file(str(file_path))
                results[filename] = result
                print(f"✅ Processed: {filename}")
            except Exception as e:
                results[filename] = {"status": "error", "error": str(e)}
                print(f"❌ Error processing {filename}: {e}")
        else:
            results[filename] = {"status": "file_not_found"}
            print(f"⚠️  File not found: {filename}")
    
    # Export memory core
    memory_export = processor.get_memory_export()
    
    return {
        "processing_results": results,
        "memory_core": memory_export,
        "total_processed": len([r for r in results.values() if r.get("status") == "processed"])
    }


if __name__ == "__main__":
    # Process priority assets
    results = process_priority_assets("../../assets/audio")
    print(json.dumps(results, indent=2))
