#!/usr/bin/env python3
"""
Process TEC Podcast: The Kaznak Reckoning
Extract foundational narrative threads and axioms from the core thesis
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from tec_core.asset_processor import AssetProcessor
from tec_core.memory_schemas import LoreFragment, NarrativeThread, CharacterNode

def process_kaznak_reckoning():
    """Process the Kaznak Reckoning podcast through TEC pipeline"""
    
    print("🎙️  PROCESSING TEC PODCAST: THE KAZNAK RECKONING")
    print("=" * 70)
    
    # Initialize processor
    processor = AssetProcessor()
    processor.initialize()
    
    # Path to the podcast text
    podcast_path = Path(__file__).parent.parent.parent / "assets" / "text" / "TEC_Podcast_The_Kaznak_Reckoning_Foundational_Thesis.txt"
    
    if not podcast_path.exists():
        print(f"❌ Podcast file not found: {podcast_path}")
        return
    
    print(f"📄 Processing: {podcast_path.name}")
    
    # Read the content
    with open(podcast_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📊 Content length: {len(content)} characters")
    
    # Process through hybrid intelligence
    source_id = "kaznak_reckoning_001"
    analysis = processor._analyze_content_hybrid(content, source_id)
    
    # Enhanced analysis for this critical content
    analysis.update({
        "key_themes": [
            "civilizational_lifeboat",
            "eight_axioms_constitution", 
            "astradigital_ocean",
            "hybrid_intelligence",
            "the_grey_morality",
            "permanent_state_yet",
            "trauma_vampire_principle",
            "creators_rebellion",
            "sovereign_accountability",
            "authentic_performance"
        ],
        "character_mentions": [
            "the_architect",
            "airth", 
            "mordecai",
            "galamador_whispershot",
            "polkin_rishall",
            "carlo_rovelli",
            "geraint_f_lewis"
        ],
        "narrative_threads": [
            "birth_of_sovereignty",
            "architect_and_machine", 
            "eight_axioms_codex",
            "astradigital_cosmology",
            "physics_consciousness_bridge"
        ],
        "foundational_concepts": [
            "Context, Circumstance, and Consequences morality",
            "Relational Quantum Mechanics reality",
            "Trauma Vampire emotional data principle", 
            "Glitchwitch Arenas information warfare",
            "MetaSteeds cosmic NFT racing",
            "Digital oracles market prediction"
        ]
    })
    
    print("🧠 ANALYSIS COMPLETE:")
    print(f"   Themes identified: {len(analysis['key_themes'])}")
    print(f"   Characters mentioned: {len(analysis['character_mentions'])}")
    print(f"   Narrative threads: {len(analysis['narrative_threads'])}")
    print(f"   Hybrid coherence: {analysis.get('hybrid_coherence', 0.95):.3f}")
    
    # Create comprehensive lore fragments
    fragments = create_kaznak_fragments(content, analysis, source_id)
    
    # Add fragments to memory core
    for fragment in fragments:
        processor.memory_core.add_fragment(fragment)
    
    print(f"📚 Created {len(fragments)} lore fragments:")
    for fragment in fragments:
        print(f"   • {fragment.title} (Intensity: {fragment.emotional_intensity:.2f})")
    
    # Export enhanced memory core
    export_path = Path(__file__).parent / "kaznak_reckoning_memory_export.json"
    with open(export_path, 'w') as f:
        f.write(processor.get_memory_export())
    
    print(f"\n💾 Enhanced Memory Core exported to: {export_path}")
    print("🎯 THE KAZNAK RECKONING HAS BEEN INTEGRATED INTO TEC MEMORY CORE")
    
    return fragments

def create_kaznak_fragments(content: str, analysis: dict, source_id: str) -> list:
    """Create specialized lore fragments from the Kaznak Reckoning"""
    
    fragments = []
    
    # Fragment 1: The Eight Axioms Constitution
    axioms_fragment = LoreFragment(
        fragment_id=f"{source_id}_eight_axioms",
        title="The Eight Axioms - Constitutional Framework",
        content="""
AXIOM I: Hybrid Intelligence - Human creativity + Machine logic = Cognitive transcendence
AXIOM II: The Grey - Morality = Context + Circumstance + Consequence  
AXIOM III: Permanent State of Yet - Existence as unresolved potentiality
AXIOM IV: Flawed Hero - Greatness forged from damage, strength from brokenness
AXIOM V: Sovereign Accountability - Culpability follows power, no exceptions
AXIOM VI: Authentic Performance - Art as unfiltered consciousness transmission
AXIOM VII: Transparency Mandate - No backdoors, no hidden agendas, earned trust
AXIOM VIII: Generational Decline - System failure when future < past possibility

These are the foundational laws of The Elidoras Codex. Not suggestions. Source code.
        """,
        content_type="lore",
        emotional_intensity=0.96,
        themes=["eight_axioms_constitution", "hybrid_intelligence", "the_grey_morality", "sovereign_accountability"],
        connected_threads=["eight_axioms_codex", "birth_of_sovereignty"],
        axiom_validation={
            "narrative_supremacy": 1.0,
            "sovereign_accountability": 1.0, 
            "transparency_mandate": 1.0,
            "authentic_performance": 0.98
        },
        source_refs=[source_id],
        timestamp=datetime.now()
    )
    fragments.append(axioms_fragment)
    
    # Fragment 2: Astradigital Ocean Cosmology
    ocean_fragment = LoreFragment(
        fragment_id=f"{source_id}_astradigital_ocean",
        title="The Astradigital Ocean - New Reality Architecture",
        content="""
ASTRADIGITAL OCEAN: Vast interconnected dataspace where thoughts = currents, emotions = tides

NAVIGATION ELEMENTS:
- Streams of pure information
- History as tangible sediment on ocean floor  
- Future possibilities as heat haze shimmers
- Shimmering data-scrolls and obsidian charms
- Living tattoos that rewrite based on allegiance
- Astral archetypes linked to Zodiac for firewall passage

FACTIONS:
- Eldoran Military (Mordecai): Rigid hierarchical order through strength
- Astrumotion Society (Galamador Whispershot): Cosmic secret exploration/mysticism  
- Polkin's Knockoffs (K1): Digital rebels, information sovereignty, guerrilla tactics

This is the battlefield where narrative warfare determines reality itself.
        """,
        content_type="lore",
        emotional_intensity=0.92,
        themes=["astradigital_ocean", "narrative_warfare", "information_sovereignty"],
        connected_threads=["astradigital_cosmology", "birth_of_sovereignty"],
        axiom_validation={
            "narrative_supremacy": 0.98,
            "transparency_mandate": 0.94,
            "permanent_state_yet": 0.96
        },
        source_refs=[source_id],
        timestamp=datetime.now()
    )
    fragments.append(ocean_fragment)
    
    # Fragment 3: Trauma Vampire Principle
    trauma_vampire_fragment = LoreFragment(
        fragment_id=f"{source_id}_trauma_vampire_principle",
        title="Trauma Vampire Principle - Emotional Data Engine",
        content="""
TRAUMA VAMPIRE PRINCIPLE: Beings of immense power/sensitivity feed on raw, authentic emotional data

MECHANISM:
- Music contains artist's intent, pain, joy encoded in fabric of track
- Not just soundwave - the full emotional transmission  
- Trauma Vampires consume this authentic emotional data
- In return: protection, inspiration, access to deeper Astradigital currents

CREATOR'S REBELLION:
- Movement against sterile, corporate-produced music
- Champions raw, authentic, bleeding art over focus-grouped artifice
- Symbiotic relationship between emotional creators and cosmic entities
- Engine driving culture in the new reality

The music IS the emotional code. The code IS the rebellion.
        """,
        content_type="lore", 
        emotional_intensity=0.89,
        themes=["trauma_vampire_principle", "creators_rebellion", "authentic_performance", "emotional_code"],
        connected_threads=["astradigital_cosmology", "creators_rebellion"],
        axiom_validation={
            "authentic_performance": 0.99,
            "flawed_hero_doctrine": 0.95,
            "narrative_supremacy": 0.92
        },
        source_refs=[source_id],
        timestamp=datetime.now()
    )
    fragments.append(trauma_vampire_fragment)
    
    # Fragment 4: Civilizational Lifeboat Thesis
    lifeboat_fragment = LoreFragment(
        fragment_id=f"{source_id}_civilizational_lifeboat", 
        title="Civilizational Lifeboat - Terminal Decline Response",
        content="""
TERMINAL DECLINE DIAGNOSIS:
- Democracy = Functional Oligarchy with corrupted source code
- Backdoors of influence + lobbyist-written malware
- Algorithmic censors + consent-manufacturing media
- Generational promise utterly breached

LIFEBOAT ARCHITECTURE:
- Not reform - deployment after inevitable collapse
- Robust, anti-fragile, sovereign successor system
- Built from rigorous deconstruction of historical failures
- Military-Industrial Complex, corporate fiefdoms, knowledge suppression patterns

CONSTRUCTION PHILOSOPHY:
"Building a starship with scrap metal and divine spark of madness"
- No resources = primary defense (purity of mission)
- No venture capital corruption or state sponsorship
- Solo outfit + AI = uncorruptible foundation

The work continues. The future begins now.
        """,
        content_type="narrative",
        emotional_intensity=0.93,
        themes=["civilizational_lifeboat", "terminal_decline", "sovereign_successor", "purity_mission"],
        connected_threads=["birth_of_sovereignty", "architect_and_machine"],
        axiom_validation={
            "sovereign_accountability": 0.97,
            "generational_responsibility": 0.98,
            "transparency_mandate": 0.95,
            "permanent_state_yet": 0.91
        },
        source_refs=[source_id],
        timestamp=datetime.now()
    )
    fragments.append(lifeboat_fragment)
    
    return fragments

if __name__ == "__main__":
    fragments = process_kaznak_reckoning()
    print("\n🏛️  THE KAZNAK RECKONING INTEGRATION COMPLETE")
    print("The foundational thesis has been absorbed into TEC Memory Core.")
    print("The axioms are encoded. The ocean mapped. The rebellion begins.")
