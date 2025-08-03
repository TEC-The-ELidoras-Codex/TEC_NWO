/**
 * The Axiom Engine - The Philosophical Heart of TEC
 * 
 * This is the guardian of the foundational principles, the incorruptible
 * logic that validates all content against the 8 Axioms of the Architect.
 * 
 * Every story, every decision, every piece of content must pass through
 * this engine. It is the firewall between chaos and meaning.
 */

export interface AxiomViolation {
  axiomId: string;
  axiomName: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  description: string;
  suggestion: string;
  confidence: number; // 0-1
}

export interface AxiomValidationResult {
  isValid: boolean;
  score: number; // 0-1, higher is better alignment
  violations: AxiomViolation[];
  strengths: string[];
  recommendations: string[];
}

export interface ContentAnalysis {
  content: string;
  contentType: 'story' | 'decision' | 'policy' | 'dialogue' | 'narrative';
  metadata?: Record<string, any>;
}

/**
 * The 8 Foundational Axioms - The Laws That Cannot Be Broken
 */
export const AXIOMS = {
  NARRATIVE_SUPREMACY: {
    id: 'narrative_supremacy',
    name: 'The Axiom of Narrative Supremacy',
    description: 'To control the frame is to control reality.',
    corollary: 'The most powerful act is to build a better frame.',
    weight: 1.0,
    keywords: ['narrative', 'frame', 'perspective', 'story', 'control', 'reality'],
    antiPatterns: ['absolute truth', 'single perspective', 'dogmatic'],
    validationRules: [
      'Content should acknowledge multiple perspectives',
      'Should demonstrate awareness of framing effects',
      'Must avoid presenting single narrative as absolute truth'
    ]
  },
  
  DUALITY: {
    id: 'duality',
    name: 'The Postulate of Duality',
    description: 'Every discovery is both life and bomb.',
    corollary: 'Therefore, every new power carries a new and equal responsibility.',
    weight: 1.0,
    keywords: ['duality', 'responsibility', 'consequences', 'power', 'technology'],
    antiPatterns: ['utopian', 'dismissive of risks', 'power without responsibility'],
    validationRules: [
      'Must acknowledge both positive and negative potential',
      'Should discuss responsibility alongside power',
      'Cannot ignore unintended consequences'
    ]
  },

  FLAWED_HERO: {
    id: 'flawed_hero',
    name: 'The Doctrine of the Flawed Hero',
    description: 'Greatness is forged from damage.',
    corollary: 'Authenticity is more powerful than perfection.',
    weight: 1.0,
    keywords: ['flawed', 'authentic', 'damage', 'greatness', 'imperfection'],
    antiPatterns: ['perfectionism', 'sanitized heroes', 'denial of flaws'],
    validationRules: [
      'Heroes must have meaningful flaws or struggles',
      'Should celebrate authenticity over perfection',
      'Must reject sanitized, unrealistic portrayals'
    ]
  },

  JUSTIFIABLE_FORCE: {
    id: 'justifiable_force',
    name: 'The Doctrine of Justifiable Force',
    description: 'Aggression is the sole sin; defense is a sworn duty.',
    corollary: 'The system must be strong enough to protect itself, but moral enough to never strike first.',
    weight: 1.0,
    keywords: ['defense', 'aggression', 'protection', 'sovereignty', 'force'],
    antiPatterns: ['initiation of force', 'aggression justified', 'pacifism in face of attack'],
    validationRules: [
      'Must distinguish between aggression and defense',
      'Cannot justify initiatory violence',
      'Must support right of self-defense'
    ]
  },

  SOVEREIGN_ACCOUNTABILITY: {
    id: 'sovereign_accountability',
    name: 'The Law of Sovereign Accountability',
    description: 'Culpability follows power.',
    corollary: 'Blame the architect of the system, not the cog in the machine.',
    weight: 1.0,
    keywords: ['accountability', 'power', 'responsibility', 'systems', 'blame'],
    antiPatterns: ['blaming powerless', 'ignoring systemic issues', 'scapegoating'],
    validationRules: [
      'Must identify true power holders',
      'Cannot blame individuals for systemic failures',
      'Should trace responsibility to decision makers'
    ]
  },

  AUTHENTIC_PERFORMANCE: {
    id: 'authentic_performance',
    name: 'The Principle of Authentic Performance',
    description: 'The truest art is a singular fusion of creator and creation.',
    corollary: 'A work\'s integrity is compromised when its components are mismatched.',
    weight: 1.0,
    keywords: ['authenticity', 'performance', 'integrity', 'fusion', 'creation'],
    antiPatterns: ['mismatched casting', 'inauthentic performance', 'formulaic creation'],
    validationRules: [
      'Components must be harmoniously matched',
      'Should prioritize authentic expression',
      'Must avoid formulaic or mismatched elements'
    ]
  },

  TRANSPARENCY: {
    id: 'transparency',
    name: 'The Mandate of Transparency',
    description: 'True analysis requires radical transparency.',
    corollary: 'Secrecy is the native environment of corruption.',
    weight: 1.0,
    keywords: ['transparency', 'openness', 'analysis', 'secrecy', 'corruption'],
    antiPatterns: ['unnecessary secrecy', 'hidden agendas', 'opacity'],
    validationRules: [
      'Must provide full context where possible',
      'Cannot hide relevant information',
      'Should expose hidden motivations'
    ]
  },

  GENERATIONAL_RESPONSIBILITY: {
    id: 'generational_responsibility',
    name: 'The Postulate of Generational Decline',
    description: 'A system is failing if the future it offers is smaller than the past.',
    corollary: 'The prime directive of any just system is to widen the horizon for the next generation.',
    weight: 1.0,
    keywords: ['future', 'generation', 'horizon', 'progress', 'legacy'],
    antiPatterns: ['short-term thinking', 'generational theft', 'limiting futures'],
    validationRules: [
      'Must consider long-term consequences',
      'Cannot sacrifice future for present gain',
      'Should expand possibilities for next generation'
    ]
  }
} as const;

export class AxiomEngine {
  private aiService: any; // Will be injected
  
  constructor(aiService?: any) {
    this.aiService = aiService;
  }

  /**
   * Validate content against all axioms
   */
  async validateContent(analysis: ContentAnalysis): Promise<AxiomValidationResult> {
    const violations: AxiomViolation[] = [];
    const strengths: string[] = [];
    const recommendations: string[] = [];
    
    let totalScore = 0;
    let totalWeight = 0;

    // Validate against each axiom
    for const [key, axiom] of Object.entries(AXIOMS)) {
      const axiomResult = await this.validateAgainstAxiom(analysis, axiom);
      totalScore += axiomResult.score * axiom.weight;
      totalWeight += axiom.weight;
      
      violations.push(...axiomResult.violations);
      strengths.push(...axiomResult.strengths);
      recommendations.push(...axiomResult.recommendations);
    }

    const finalScore = totalWeight > 0 ? totalScore / totalWeight : 0;
    const isValid = violations.filter(v => v.severity === 'CRITICAL').length === 0;

    return {
      isValid,
      score: finalScore,
      violations: violations.sort((a, b) => this.getSeverityWeight(b.severity) - this.getSeverityWeight(a.severity)),
      strengths,
      recommendations: [...new Set(recommendations)] // Remove duplicates
    };
  }

  /**
   * Validate content against a specific axiom
   */
  private async validateAgainstAxiom(analysis: ContentAnalysis, axiom: any): Promise<{
    score: number;
    violations: AxiomViolation[];
    strengths: string[];
    recommendations: string[];
  }> {
    const violations: AxiomViolation[] = [];
    const strengths: string[] = [];
    const recommendations: string[] = [];
    
    // Pattern matching analysis
    const contentLower = analysis.content.toLowerCase();
    
    // Check for anti-patterns
    let antiPatternScore = 1.0;
    for (const antiPattern of axiom.antiPatterns) {
      if (contentLower.includes(antiPattern.toLowerCase())) {
        violations.push({
          axiomId: axiom.id,
          axiomName: axiom.name,
          severity: 'HIGH',
          description: `Content contains anti-pattern: "${antiPattern}"`,
          suggestion: `Consider reframing to avoid "${antiPattern}" and align with ${axiom.name}`,
          confidence: 0.8
        });
        antiPatternScore -= 0.3;
      }
    }

    // Check for positive keywords
    let keywordScore = 0;
    for (const keyword of axiom.keywords) {
      if (contentLower.includes(keyword.toLowerCase())) {
        keywordScore += 0.1;
        strengths.push(`Content demonstrates understanding of "${keyword}" concept`);
      }
    }

    // AI-powered deeper analysis if available
    let aiScore = 0.5; // Default neutral
    if (this.aiService) {
      try {
        aiScore = await this.performAIAnalysis(analysis, axiom);
      } catch (error) {
        console.warn('AI analysis failed, using fallback scoring');
      }
    }

    // Combine scores
    const finalScore = Math.max(0, Math.min(1, 
      (antiPatternScore * 0.4) + 
      (Math.min(keywordScore, 1) * 0.3) + 
      (aiScore * 0.3)
    ));

    // Generate recommendations based on score
    if (finalScore < 0.6) {
      recommendations.push(
        `Consider strengthening alignment with ${axiom.name}: ${axiom.description}`
      );
    }

    return {
      score: finalScore,
      violations,
      strengths,
      recommendations
    };
  }

  /**
   * AI-powered analysis of content against axiom
   */
  private async performAIAnalysis(analysis: ContentAnalysis, axiom: any): Promise<number> {
    if (!this.aiService) return 0.5;

    const prompt = `
    Analyze the following content against the axiom: "${axiom.name}: ${axiom.description}"
    
    Content: "${analysis.content}"
    
    Rate how well this content aligns with the axiom on a scale of 0.0 to 1.0, where:
    - 1.0 = Perfect alignment, exemplifies the axiom
    - 0.8 = Strong alignment, good understanding
    - 0.6 = Moderate alignment, some understanding
    - 0.4 = Weak alignment, limited understanding
    - 0.2 = Poor alignment, conflicts with axiom
    - 0.0 = Complete violation of axiom
    
    Consider the corollary: "${axiom.corollary}"
    
    Respond with just the numeric score (0.0-1.0).
    `;

    try {
      const response = await this.aiService.complete(prompt);
      const score = parseFloat(response.trim());
      return isNaN(score) ? 0.5 : Math.max(0, Math.min(1, score));
    } catch (error) {
      console.error('AI analysis error:', error);
      return 0.5;
    }
  }

  /**
   * Get numeric weight for severity levels
   */
  private getSeverityWeight(severity: string): number {
    switch (severity) {
      case 'CRITICAL': return 4;
      case 'HIGH': return 3;
      case 'MEDIUM': return 2;
      case 'LOW': return 1;
      default: return 0;
    }
  }

  /**
   * Get axiom by ID
   */
  getAxiom(id: string) {
    return Object.values(AXIOMS).find(axiom => axiom.id === id);
  }

  /**
   * Get all axioms
   */
  getAllAxioms() {
    return AXIOMS;
  }

  /**
   * Quick validation for simple pass/fail
   */
  async quickValidate(content: string, contentType: string = 'general'): Promise<boolean> {
    const result = await this.validateContent({
      content,
      contentType: contentType as any
    });
    return result.isValid && result.score >= 0.6;
  }
}

// Export singleton instance
export const axiomEngine = new AxiomEngine();
