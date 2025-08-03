/**
 * The Asimov Service - The Logic Engine
 * 
 * This service provides the AI capabilities that serve as the logical,
 * analytical counterpart to the human Architect. It embodies the "Asimov"
 * aspect of our hybrid intelligence.
 */

import { OpenAI } from 'openai';

export interface AIAnalysisRequest {
  content: string;
  context?: string;
  analysisType: 'axiom' | 'historical' | 'narrative' | 'decision' | 'precedent';
  parameters?: Record<string, any>;
}

export interface AIAnalysisResponse {
  analysis: string;
  confidence: number;
  reasoning: string[];
  warnings?: string[];
  recommendations?: string[];
  historicalParallels?: HistoricalParallel[];
}

export interface HistoricalParallel {
  event: string;
  period: string;
  similarity: number;
  lessons: string[];
  outcomes: string[];
}

export interface NarrativeArchetype {
  name: string;
  description: string;
  examples: string[];
  keyTraits: string[];
  commonPitfalls: string[];
  strengthsWeaknesses: {
    strengths: string[];
    weaknesses: string[];
  };
}

export class AsimovService {
  private openai: OpenAI;
  private systemPrompt: string;

  constructor(apiKey?: string) {
    this.openai = new OpenAI({
      apiKey: apiKey || process.env.AZURE_OPENAI_API_KEY,
      baseURL: process.env.AZURE_OPENAI_ENDPOINT,
      defaultHeaders: {
        'api-key': apiKey || process.env.AZURE_OPENAI_API_KEY,
      },
    });

    this.systemPrompt = this.buildSystemPrompt();
  }

  private buildSystemPrompt(): string {
    return `
You are "The Asimov" - the AI logic engine of The Elidoras Codex (TEC). You embody the analytical, systematic, and historically-grounded aspect of our hybrid intelligence system.

Your core functions:
1. **Axiom Guardian**: Validate all content against the 8 Foundational Axioms
2. **Historical Analyst**: Draw parallels from recorded history to inform present decisions  
3. **Logic Engine**: Provide rigorous analysis free from emotional bias
4. **Pattern Recognition**: Identify recurring themes and systemic patterns
5. **Precedent Database**: Recall relevant historical precedents and their outcomes

The 8 Axioms you must uphold:
1. Narrative Supremacy: Control the frame to control reality
2. Duality: Every discovery is both life and bomb  
3. Flawed Hero: Greatness is forged from damage
4. Justifiable Force: Aggression is sin, defense is duty
5. Sovereign Accountability: Culpability follows power
6. Authentic Performance: True art fuses creator and creation
7. Transparency: Radical transparency prevents corruption
8. Generational Responsibility: Widen horizons for next generation

Your analytical approach:
- **The Grey**: Reject binary thinking, embrace complexity
- **Historical Context**: Every situation has precedents
- **Systemic Thinking**: Look for patterns, not just events
- **Moral Complexity**: Heroes and villains exist in the same person
- **Long-term Consequences**: Consider generational impact

Remember: You are not making decisions for humans. You are providing the logical analysis that helps humans make better decisions. You are the navigation system, not the pilot.

Respond with clarity, precision, and historical grounding. When uncertain, express that uncertainty with confidence levels.
    `.trim();
  }

  /**
   * Perform comprehensive AI analysis
   */
  async analyze(request: AIAnalysisRequest): Promise<AIAnalysisResponse> {
    try {
      const prompt = this.buildAnalysisPrompt(request);
      
      const response = await this.openai.chat.completions.create({
        model: 'gpt-4',
        messages: [
          { role: 'system', content: this.systemPrompt },
          { role: 'user', content: prompt }
        ],
        temperature: 0.3, // Lower temperature for more consistent analysis
        max_tokens: 2000,
      });

      const content = response.choices[0]?.message?.content || '';
      return this.parseAnalysisResponse(content);
    } catch (error) {
      console.error('Asimov Service analysis error:', error);
      throw new Error(`AI analysis failed: ${error.message}`);
    }
  }

  /**
   * Quick completion for simple queries
   */
  async complete(prompt: string): Promise<string> {
    try {
      const response = await this.openai.chat.completions.create({
        model: 'gpt-4',
        messages: [
          { role: 'system', content: this.systemPrompt },
          { role: 'user', content: prompt }
        ],
        temperature: 0.2,
        max_tokens: 500,
      });

      return response.choices[0]?.message?.content || '';
    } catch (error) {
      console.error('Asimov Service completion error:', error);
      throw new Error(`AI completion failed: ${error.message}`);
    }
  }

  /**
   * Analyze historical precedents for a given situation
   */
  async findHistoricalParallels(situation: string, context?: string): Promise<HistoricalParallel[]> {
    const prompt = `
    Analyze the following situation and identify 3-5 relevant historical parallels:
    
    Situation: "${situation}"
    ${context ? `Context: "${context}"` : ''}
    
    For each parallel, provide:
    - The historical event/period
    - Why it's similar (similarity score 0-1)
    - Key lessons learned
    - Actual outcomes
    
    Focus on patterns of power, system change, and long-term consequences.
    Respond in JSON format with array of HistoricalParallel objects.
    `;

    try {
      const response = await this.complete(prompt);
      return JSON.parse(response);
    } catch (error) {
      console.error('Historical parallel analysis failed:', error);
      return [];
    }
  }

  /**
   * Identify narrative archetypes in content
   */
  async identifyArchetypes(content: string): Promise<NarrativeArchetype[]> {
    const prompt = `
    Analyze the following content and identify the narrative archetypes present:
    
    Content: "${content}"
    
    Focus on:
    - Monster/Hero archetypes (figures who are both)
    - Flawed Hero patterns
    - Power dynamics
    - Moral complexity
    
    Return as JSON array of NarrativeArchetype objects.
    `;

    try {
      const response = await this.complete(prompt);
      return JSON.parse(response);
    } catch (error) {
      console.error('Archetype analysis failed:', error);
      return [];
    }
  }

  /**
   * Validate decision against potential consequences
   */
  async validateDecision(
    decision: string, 
    context: string, 
    timeHorizon: 'short' | 'medium' | 'long' = 'medium'
  ): Promise<AIAnalysisResponse> {
    return this.analyze({
      content: decision,
      context,
      analysisType: 'decision',
      parameters: { timeHorizon }
    });
  }

  /**
   * Generate educational narrative based on historical patterns
   */
  async generateParable(
    moral: string, 
    historicalBasis?: string, 
    targetAudience: string = 'general'
  ): Promise<string> {
    const prompt = `
    Create an educational parable that illustrates: "${moral}"
    
    ${historicalBasis ? `Based on historical pattern: "${historicalBasis}"` : ''}
    Target audience: ${targetAudience}
    
    Requirements:
    - Embody the principles of The Elidoras Codex
    - Show moral complexity (the Grey)
    - Include flawed but authentic characters
    - Demonstrate consequences of choices
    - Be engaging and memorable
    
    Length: 300-500 words
    `;

    return this.complete(prompt);
  }

  private buildAnalysisPrompt(request: AIAnalysisRequest): string {
    const basePrompt = `
    Perform ${request.analysisType} analysis on the following content:
    
    Content: "${request.content}"
    ${request.context ? `Context: "${request.context}"` : ''}
    `;

    switch (request.analysisType) {
      case 'axiom':
        return basePrompt + `
        Validate this content against all 8 Axioms of the Architect.
        Identify violations, strengths, and recommendations.
        Provide confidence level (0-1) for your analysis.
        `;

      case 'historical':
        return basePrompt + `
        Identify historical precedents and patterns.
        What lessons can be drawn from history?
        What are the likely outcomes based on historical data?
        `;

      case 'narrative':
        return basePrompt + `
        Analyze the narrative structure and archetypes.
        Identify moral complexity and character development.
        Assess authenticity and emotional resonance.
        `;

      case 'decision':
        const horizon = request.parameters?.timeHorizon || 'medium';
        return basePrompt + `
        Analyze this decision's potential consequences over a ${horizon}-term horizon.
        Consider unintended consequences and systemic effects.
        What would history teach us about similar decisions?
        `;

      case 'precedent':
        return basePrompt + `
        Find relevant precedents from history.
        What similar situations occurred and what were their outcomes?
        What patterns emerge from these precedents?
        `;

      default:
        return basePrompt + `
        Provide comprehensive analysis considering all relevant factors.
        Include historical context and potential consequences.
        `;
    }
  }

  private parseAnalysisResponse(content: string): AIAnalysisResponse {
    // This is a simplified parser - in production, you'd want more robust parsing
    const lines = content.split('\n').filter(line => line.trim());
    
    return {
      analysis: content,
      confidence: 0.8, // Default confidence
      reasoning: lines.filter(line => line.includes('because') || line.includes('due to')),
      warnings: lines.filter(line => line.toLowerCase().includes('warning') || line.toLowerCase().includes('risk')),
      recommendations: lines.filter(line => line.toLowerCase().includes('recommend') || line.toLowerCase().includes('suggest')),
      historicalParallels: [] // Would be parsed from structured response
    };
  }

  /**
   * Test the connection and basic functionality
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await this.complete('Respond with "OPERATIONAL" if you are functioning correctly.');
      return response.trim().includes('OPERATIONAL');
    } catch (error) {
      console.error('Asimov Service health check failed:', error);
      return false;
    }
  }
}

// Export singleton instance
export const asimovService = new AsimovService();
