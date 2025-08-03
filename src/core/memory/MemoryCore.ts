/**
 * The Memory Core - Historical Precedent Analysis System
 * 
 * This system stores, indexes, and retrieves historical precedents,
 * patterns, and lessons. It serves as the institutional memory that
 * prevents us from repeating the mistakes of the past.
 */

export interface HistoricalEvent {
  id: string;
  title: string;
  period: string;
  startDate: Date;
  endDate?: Date;
  location: string;
  category: 'political' | 'economic' | 'technological' | 'social' | 'military' | 'cultural';
  description: string;
  keyFigures: HistoricalFigure[];
  causes: string[];
  outcomes: string[];
  lessons: string[];
  patterns: string[];
  modernRelevance: string[];
  sources: string[];
  tags: string[];
  embedding?: number[]; // Vector embedding for semantic search
}

export interface HistoricalFigure {
  name: string;
  role: string;
  archetype: 'hero' | 'villain' | 'monster_hero' | 'tragic_genius' | 'necessary_tyrant' | 'flawed_leader';
  keyActions: string[];
  motivations: string[];
  flaws: string[];
  strengths: string[];
  legacy: string;
  lessons: string[];
}

export interface Pattern {
  id: string;
  name: string;
  description: string;
  occurrences: string[]; // Event IDs where this pattern appears
  stages: string[];
  commonCauses: string[];
  typicalOutcomes: string[];
  warningSigns: string[];
  preventionStrategies: string[];
  examples: HistoricalExample[];
}

export interface HistoricalExample {
  eventId: string;
  title: string;
  period: string;
  relevance: number; // 0-1
  keyLessons: string[];
}

export interface PrecedentQuery {
  situation: string;
  context?: string;
  timeframe?: string;
  categories?: string[];
  minRelevance?: number;
  maxResults?: number;
}

export interface PrecedentResult {
  events: HistoricalEvent[];
  patterns: Pattern[];
  warnings: string[];
  recommendations: string[];
  confidence: number;
}

export class MemoryCore {
  private events: Map<string, HistoricalEvent> = new Map();
  private patterns: Map<string, Pattern> = new Map();
  private figures: Map<string, HistoricalFigure> = new Map();
  private tagIndex: Map<string, Set<string>> = new Map();
  
  constructor() {
    this.initializeCorePrecedents();
  }

  /**
   * Initialize with core historical precedents that are fundamental to TEC
   */
  private initializeCorePrecedents(): void {
    // The Fall of Rome - Pattern of Imperial Decline
    this.addEvent({
      id: 'fall_of_rome',
      title: 'Fall of the Western Roman Empire',
      period: '3rd-5th Century CE',
      startDate: new Date(235, 0, 1),
      endDate: new Date(476, 0, 1),
      location: 'Roman Empire',
      category: 'political',
      description: 'The gradual decline and fall of the Western Roman Empire due to overextension, corruption, economic collapse, and external pressures.',
      keyFigures: [
        {
          name: 'Marcus Aurelius',
          role: 'Last of the Five Good Emperors',
          archetype: 'tragic_genius',
          keyActions: ['Meditations on Stoicism', 'Military campaigns', 'Administrative reforms'],
          motivations: ['Duty to empire', 'Philosophical principles', 'Justice'],
          flaws: ['Chose incompetent successor (Commodus)', 'Failed to address systemic issues'],
          strengths: ['Philosophical wisdom', 'Personal integrity', 'Military competence'],
          legacy: 'Embodied the ideal of philosopher-king but could not prevent imperial decline',
          lessons: ['Personal virtue insufficient without systemic reform', 'Succession planning critical']
        }
      ],
      causes: [
        'Military overextension',
        'Economic collapse and debasement of currency',
        'Political instability and civil wars',
        'Barbarian invasions',
        'Loss of civic virtue',
        'Administrative corruption'
      ],
      outcomes: [
        'End of Western Roman Empire',
        'Rise of feudalism',
        'Dark Ages in Western Europe',
        'Preservation of knowledge in Byzantine Empire',
        'Rise of Christianity as dominant force'
      ],
      lessons: [
        'Overextension leads to collapse',
        'Economic policy affects everything',
        'Corruption destroys from within',
        'External threats exploit internal weakness',
        'Cultural values matter as much as military might'
      ],
      patterns: ['imperial_overstretch', 'currency_debasement', 'elite_corruption'],
      modernRelevance: [
        'American military overextension',
        'Currency manipulation and debt',
        'Political polarization and dysfunction',
        'Immigration and cultural change',
        'Loss of shared values'
      ],
      sources: ['Gibbon - Decline and Fall', 'Tacitus', 'Archaeological evidence'],
      tags: ['empire', 'decline', 'corruption', 'overextension', 'precedent']
    });

    // The Manhattan Project - Dual Use Technology
    this.addEvent({
      id: 'manhattan_project',
      title: 'The Manhattan Project',
      period: '1939-1946',
      startDate: new Date(1939, 7, 2),
      endDate: new Date(1946, 0, 1),
      location: 'United States',
      category: 'technological',
      description: 'Secret U.S. project to develop nuclear weapons during WWII, representing the ultimate dual-use technology.',
      keyFigures: [
        {
          name: 'J. Robert Oppenheimer',
          role: 'Scientific Director',
          archetype: 'monster_hero',
          keyActions: ['Led Los Alamos Laboratory', 'Coordinated scientific effort', 'Witnessed Trinity test'],
          motivations: ['Defeat Nazi Germany', 'Scientific curiosity', 'National duty'],
          flaws: ['Hubris', 'Political naivety', 'Moral blindness to consequences'],
          strengths: ['Scientific brilliance', 'Leadership ability', 'Later moral awakening'],
          legacy: '"I am become Death, destroyer of worlds" - embodiment of scientific responsibility',
          lessons: ['Scientists must consider consequences', 'Knowledge cannot be uninvented', 'Power corrupts even the well-intentioned']
        }
      ],
      causes: [
        'Fear of Nazi nuclear program',
        'Scientific breakthroughs in nuclear physics',
        'Industrial capacity of United States',
        'Wartime urgency and resources'
      ],
      outcomes: [
        'Nuclear weapons created',
        'End of WWII',
        'Beginning of nuclear age',
        'Cold War arms race',
        'Permanent existential threat'
      ],
      lessons: [
        'Scientific breakthroughs have unpredictable consequences',
        'Military applications often drive technology development',
        'Ethical considerations lag behind technical capability',
        'Knowledge proliferation is inevitable',
        'Power and responsibility are inseparable'
      ],
      patterns: ['dual_use_technology', 'scientific_hubris', 'unintended_consequences'],
      modernRelevance: [
        'AI development and risks',
        'Biotechnology and bioweapons',
        'Cyber warfare tools',
        'CRISPR and genetic engineering'
      ],
      sources: ['Manhattan Project documents', 'Oppenheimer interviews', 'Declassified files'],
      tags: ['technology', 'duality', 'consequences', 'science', 'ethics']
    });

    // Standard Oil Trust - Corporate Power and Oligarchy
    this.addEvent({
      id: 'standard_oil_monopoly',
      title: 'Standard Oil Trust and Monopoly',
      period: '1870-1911',
      startDate: new Date(1870, 0, 10),
      endDate: new Date(1911, 4, 15),
      location: 'United States',
      category: 'economic',
      description: 'John D. Rockefeller\'s Standard Oil Company achieved near-total monopoly of US oil industry, demonstrating the rise of corporate oligarchy.',
      keyFigures: [
        {
          name: 'John D. Rockefeller',
          role: 'Founder and Controller',
          archetype: 'necessary_tyrant',
          keyActions: ['Created horizontal integration', 'Eliminated competition', 'Built infrastructure empire'],
          motivations: ['Efficiency and order', 'Elimination of waste', 'Personal wealth and power'],
          flaws: ['Ruthless business practices', 'Predatory pricing', 'Bribery and corruption'],
          strengths: ['Organizational genius', 'Long-term vision', 'Systematic approach'],
          legacy: 'Built modern corporate structure but demonstrated dangers of unchecked power',
          lessons: ['Efficiency can justify tyranny', 'Monopoly power corrupts', 'System-builders become system-rulers']
        }
      ],
      causes: [
        'Chaotic early oil industry',
        'Lack of regulatory framework',
        'Rockefeller\'s systematic approach',
        'Control of transportation (railroads)',
        'Predatory business practices'
      ],
      outcomes: [
        'Near-total oil monopoly',
        'Supreme Court breakup (1911)',
        'Creation of multiple oil companies',
        'Antitrust legislation',
        'Template for modern corporations'
      ],
      lessons: [
        'Monopolies stifle innovation and competition',
        'Economic power translates to political power',
        'Breaking up monopolies can increase overall value',
        'Regulatory capture is constant threat',
        'Infrastructure control equals system control'
      ],
      patterns: ['monopoly_formation', 'regulatory_capture', 'elite_accumulation'],
      modernRelevance: [
        'Big Tech monopolies',
        'Amazon marketplace dominance',
        'Google search monopoly',
        'Apple app store control',
        'Meta social media dominance'
      ],
      sources: ['Supreme Court documents', 'Ida Tarbell investigations', 'Rockefeller archives'],
      tags: ['monopoly', 'oligarchy', 'corporate power', 'regulation', 'precedent']
    });

    // Add core patterns
    this.addPattern({
      id: 'imperial_overstretch',
      name: 'Imperial Overstretch',
      description: 'When empires expand beyond their capacity to maintain control, leading to inevitable collapse.',
      occurrences: ['fall_of_rome', 'british_empire_decline', 'soviet_collapse'],
      stages: [
        'Rapid expansion phase',
        'Peak power and confidence',
        'Overcommitment of resources',
        'Internal strain and resistance',
        'External challenges multiply',
        'Retreat and collapse'
      ],
      commonCauses: [
        'Military overextension',
        'Economic drain of maintaining control',
        'Administrative complexity',
        'Local resistance and nationalism',
        'Competitor nations rising'
      ],
      typicalOutcomes: [
        'Loss of peripheral territories first',
        'Economic crisis',
        'Political instability',
        'Social unrest',
        'Complete systemic collapse'
      ],
      warningSigns: [
        'Military commitments exceed resources',
        'Increasing cost of empire maintenance',
        'Rising local resistance movements',
        'Economic indicators deteriorating',
        'Political discourse becomes militaristic'
      ],
      preventionStrategies: [
        'Regular strategic review of commitments',
        'Focus on core vital interests',
        'Diplomatic solutions over military',
        'Economic sustainability analysis',
        'Gradual, voluntary devolution of power'
      ],
      examples: [
        {
          eventId: 'fall_of_rome',
          title: 'Roman Imperial Overstretch',
          period: '3rd-5th Century CE',
          relevance: 0.95,
          keyLessons: ['Barbarian frontier became unmanageable', 'Military costs bankrupted empire']
        }
      ]
    });
  }

  /**
   * Add a historical event to the memory core
   */
  addEvent(event: HistoricalEvent): void {
    this.events.set(event.id, event);
    
    // Update tag index
    event.tags.forEach(tag => {
      if (!this.tagIndex.has(tag)) {
        this.tagIndex.set(tag, new Set());
      }
      this.tagIndex.get(tag)!.add(event.id);
    });

    // Index key figures
    event.keyFigures.forEach(figure => {
      this.figures.set(`${event.id}_${figure.name}`, figure);
    });
  }

  /**
   * Add a pattern to the memory core
   */
  addPattern(pattern: Pattern): void {
    this.patterns.set(pattern.id, pattern);
  }

  /**
   * Find relevant precedents for a given situation
   */
  async findPrecedents(query: PrecedentQuery): Promise<PrecedentResult> {
    const relevantEvents: HistoricalEvent[] = [];
    const relevantPatterns: Pattern[] = [];
    const warnings: string[] = [];
    const recommendations: string[] = [];

    // Simple keyword matching (in production, would use vector similarity)
    const queryWords = query.situation.toLowerCase().split(' ');
    
    // Find matching events
    for (const event of this.events.values()) {
      let relevance = 0;
      
      // Check description match
      const descWords = event.description.toLowerCase();
      queryWords.forEach(word => {
        if (descWords.includes(word)) relevance += 0.1;
      });

      // Check tags match
      event.tags.forEach(tag => {
        if (queryWords.some(word => tag.includes(word) || word.includes(tag))) {
          relevance += 0.2;
        }
      });

      // Check modern relevance
      event.modernRelevance.forEach(modern => {
        if (queryWords.some(word => modern.toLowerCase().includes(word))) {
          relevance += 0.3;
        }
      });

      if (relevance >= (query.minRelevance || 0.2)) {
        relevantEvents.push(event);
      }
    }

    // Find matching patterns
    for (const pattern of this.patterns.values()) {
      let relevance = 0;
      
      const patternText = (pattern.name + ' ' + pattern.description).toLowerCase();
      queryWords.forEach(word => {
        if (patternText.includes(word)) relevance += 0.1;
      });

      if (relevance >= (query.minRelevance || 0.2)) {
        relevantPatterns.push(pattern);
        
        // Add pattern-based warnings
        warnings.push(...pattern.warningSigns.map(sign => 
          `Historical pattern "${pattern.name}" suggests watching for: ${sign}`
        ));
        
        // Add pattern-based recommendations
        recommendations.push(...pattern.preventionStrategies.map(strategy =>
          `Based on "${pattern.name}" pattern: ${strategy}`
        ));
      }
    }

    // Sort by relevance and limit results
    const maxResults = query.maxResults || 10;
    const sortedEvents = relevantEvents.slice(0, maxResults);
    const sortedPatterns = relevantPatterns.slice(0, 5);

    return {
      events: sortedEvents,
      patterns: sortedPatterns,
      warnings: [...new Set(warnings)],
      recommendations: [...new Set(recommendations)],
      confidence: relevantEvents.length > 0 ? 0.8 : 0.3
    };
  }

  /**
   * Get event by ID
   */
  getEvent(id: string): HistoricalEvent | undefined {
    return this.events.get(id);
  }

  /**
   * Get pattern by ID
   */
  getPattern(id: string): Pattern | undefined {
    return this.patterns.get(id);
  }

  /**
   * Search events by tags
   */
  searchByTags(tags: string[]): HistoricalEvent[] {
    const eventIds = new Set<string>();
    
    tags.forEach(tag => {
      const tagEvents = this.tagIndex.get(tag);
      if (tagEvents) {
        tagEvents.forEach(id => eventIds.add(id));
      }
    });

    return Array.from(eventIds).map(id => this.events.get(id)!).filter(Boolean);
  }

  /**
   * Get all events in a category
   */
  getEventsByCategory(category: string): HistoricalEvent[] {
    return Array.from(this.events.values()).filter(event => event.category === category);
  }

  /**
   * Get statistics about the memory core
   */
  getStats(): {
    totalEvents: number;
    totalPatterns: number;
    totalFigures: number;
    categoryCounts: Record<string, number>;
    tagCounts: Record<string, number>;
  } {
    const categoryCounts: Record<string, number> = {};
    const tagCounts: Record<string, number> = {};

    for (const event of this.events.values()) {
      categoryCounts[event.category] = (categoryCounts[event.category] || 0) + 1;
      
      event.tags.forEach(tag => {
        tagCounts[tag] = (tagCounts[tag] || 0) + 1;
      });
    }

    return {
      totalEvents: this.events.size,
      totalPatterns: this.patterns.size,
      totalFigures: this.figures.size,
      categoryCounts,
      tagCounts
    };
  }
}

// Export singleton instance
export const memoryCore = new MemoryCore();
