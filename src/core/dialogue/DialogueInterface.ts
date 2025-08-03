/**
 * The Dialogue Interface - Human-AI Collaboration Engine
 * 
 * This system facilitates the "Ellison/Asimov" synthesis - the real-time
 * collaboration between human creativity and AI logic that forms the
 * core of The Elidoras Codex hybrid intelligence.
 */

import { AsimovService } from '../ai/AsimovService';
import { AxiomEngine, AxiomValidationResult } from '../axioms/AxiomEngine';
import { MemoryCore, PrecedentResult } from '../memory/MemoryCore';

export interface DialogueContext {
  sessionId: string;
  userId: string;
  topic: string;
  phase: 'exploration' | 'analysis' | 'synthesis' | 'validation' | 'implementation';
  priority: 'low' | 'medium' | 'high' | 'critical';
  tags: string[];
  metadata: Record<string, any>;
}

export interface HumanInput {
  content: string;
  type: 'question' | 'statement' | 'proposal' | 'decision' | 'story' | 'axiom_test';
  emotion?: 'neutral' | 'concerned' | 'excited' | 'frustrated' | 'determined';
  confidence: number; // 0-1
  context?: string;
  requestedAnalysis?: ('axiom' | 'historical' | 'narrative' | 'consequences')[];
}

export interface AIResponse {
  content: string;
  analysisType: 'validation' | 'precedent' | 'synthesis' | 'recommendation' | 'challenge';
  confidence: number;
  reasoning: string[];
  warnings?: string[];
  historicalContext?: string[];
  axiomAlignment?: AxiomValidationResult;
  precedents?: PrecedentResult;
  nextQuestions?: string[];
  recommendations?: string[];
}

export interface DialogueExchange {
  id: string;
  timestamp: Date;
  human: HumanInput;
  ai: AIResponse;
  context: DialogueContext;
  synthesis?: SynthesisResult;
}

export interface SynthesisResult {
  conclusion: string;
  confidence: number;
  humanContribution: string[];
  aiContribution: string[];
  axiomCompliance: number; // 0-1
  historicalGrounding: number; // 0-1
  novelty: number; // 0-1
  actionItems?: string[];
  followUpQuestions?: string[];
}

export interface DialogueSession {
  id: string;
  userId: string;
  topic: string;
  startTime: Date;
  lastActivity: Date;
  exchanges: DialogueExchange[];
  currentContext: DialogueContext;
  cumulativeSynthesis: SynthesisResult[];
  status: 'active' | 'paused' | 'completed' | 'archived';
}

export class DialogueInterface {
  private asimov: AsimovService;
  private axiomEngine: AxiomEngine;
  private memoryCore: MemoryCore;
  private sessions: Map<string, DialogueSession> = new Map();

  constructor(
    asimov: AsimovService,
    axiomEngine: AxiomEngine,
    memoryCore: MemoryCore
  ) {
    this.asimov = asimov;
    this.axiomEngine = axiomEngine;
    this.memoryCore = memoryCore;
  }

  /**
   * Start a new dialogue session
   */
  async startSession(
    userId: string,
    topic: string,
    initialContext?: Partial<DialogueContext>
  ): Promise<DialogueSession> {
    const sessionId = this.generateSessionId();
    
    const context: DialogueContext = {
      sessionId,
      userId,
      topic,
      phase: 'exploration',
      priority: 'medium',
      tags: [],
      metadata: {},
      ...initialContext
    };

    const session: DialogueSession = {
      id: sessionId,
      userId,
      topic,
      startTime: new Date(),
      lastActivity: new Date(),
      exchanges: [],
      currentContext: context,
      cumulativeSynthesis: [],
      status: 'active'
    };

    this.sessions.set(sessionId, session);
    return session;
  }

  /**
   * Process human input and generate AI response
   */
  async processInput(
    sessionId: string,
    humanInput: HumanInput
  ): Promise<DialogueExchange> {
    const session = this.sessions.get(sessionId);
    if (!session) {
      throw new Error(`Session ${sessionId} not found`);
    }

    // Update session activity
    session.lastActivity = new Date();

    // Generate AI response
    const aiResponse = await this.generateAIResponse(humanInput, session.currentContext);

    // Create exchange
    const exchange: DialogueExchange = {
      id: this.generateExchangeId(),
      timestamp: new Date(),
      human: humanInput,
      ai: aiResponse,
      context: { ...session.currentContext },
      synthesis: await this.generateSynthesis(humanInput, aiResponse, session)
    };

    // Add to session
    session.exchanges.push(exchange);

    // Update context based on exchange
    await this.updateContext(session, exchange);

    return exchange;
  }

  /**
   * Generate AI response based on human input and context
   */
  private async generateAIResponse(
    humanInput: HumanInput,
    context: DialogueContext
  ): Promise<AIResponse> {
    const responses: Partial<AIResponse> = {
      reasoning: [],
      warnings: [],
      historicalContext: [],
      nextQuestions: [],
      recommendations: []
    };

    // Default analysis based on input type
    const analysisTypes = humanInput.requestedAnalysis || this.getDefaultAnalysisTypes(humanInput.type);

    // Axiom validation if requested or if proposing something
    if (analysisTypes.includes('axiom') || humanInput.type === 'proposal') {
      try {
        const axiomResult = await this.axiomEngine.validateContent({
          content: humanInput.content,
          contentType: humanInput.type === 'story' ? 'story' : 'general'
        });
        responses.axiomAlignment = axiomResult;
        
        if (!axiomResult.isValid) {
          responses.warnings!.push('Axiom violations detected');
        }
      } catch (error) {
        responses.warnings!.push('Axiom validation failed');
      }
    }

    // Historical precedent analysis if requested
    if (analysisTypes.includes('historical')) {
      try {
        const precedents = await this.memoryCore.findPrecedents({
          situation: humanInput.content,
          context: humanInput.context,
          minRelevance: 0.3
        });
        responses.precedents = precedents;
        responses.historicalContext = precedents.events.map(e => 
          `${e.title} (${e.period}): ${e.lessons.join(', ')}`
        );
      } catch (error) {
        responses.warnings!.push('Historical analysis failed');
      }
    }

    // Generate AI analysis and recommendations
    try {
      const aiAnalysis = await this.asimov.analyze({
        content: humanInput.content,
        context: this.buildContextString(context, humanInput),
        analysisType: this.mapToAIAnalysisType(humanInput.type),
        parameters: { 
          emotion: humanInput.emotion,
          confidence: humanInput.confidence,
          phase: context.phase
        }
      });

      responses.content = aiAnalysis.analysis;
      responses.confidence = aiAnalysis.confidence;
      responses.reasoning = aiAnalysis.reasoning || [];
      responses.warnings = [...(responses.warnings || []), ...(aiAnalysis.warnings || [])];
      responses.recommendations = aiAnalysis.recommendations || [];

    } catch (error) {
      // Fallback response if AI analysis fails
      responses.content = this.generateFallbackResponse(humanInput, context);
      responses.confidence = 0.5;
      responses.reasoning = ['AI analysis unavailable, using fallback logic'];
    }

    // Generate appropriate analysis type
    responses.analysisType = this.determineAnalysisType(humanInput, responses as AIResponse);

    // Generate next questions to continue dialogue
    responses.nextQuestions = this.generateNextQuestions(humanInput, context, responses as AIResponse);

    return responses as AIResponse;
  }

  /**
   * Generate synthesis between human and AI contributions
   */
  private async generateSynthesis(
    humanInput: HumanInput,
    aiResponse: AIResponse,
    session: DialogueSession
  ): Promise<SynthesisResult> {
    // Calculate metrics
    const axiomCompliance = aiResponse.axiomAlignment?.score || 0.5;
    const historicalGrounding = aiResponse.precedents?.confidence || 0.5;
    
    // Determine novelty (how much this adds to existing session)
    const novelty = this.calculateNovelty(humanInput, session);

    // Extract contributions
    const humanContribution = [
      'Creative insight and vision',
      'Emotional context and intuition',
      'Personal experience and perspective'
    ];

    const aiContribution = [
      'Historical precedent analysis',
      'Axiom compliance validation',
      'Systematic reasoning and logic',
      'Pattern recognition across time'
    ];

    // Generate conclusion
    const conclusion = await this.generateSynthesisConclusion(humanInput, aiResponse, session);

    return {
      conclusion,
      confidence: (humanInput.confidence + aiResponse.confidence + axiomCompliance) / 3,
      humanContribution,
      aiContribution,
      axiomCompliance,
      historicalGrounding,
      novelty,
      actionItems: this.extractActionItems(humanInput, aiResponse),
      followUpQuestions: aiResponse.nextQuestions
    };
  }

  /**
   * Update dialogue context based on exchange
   */
  private async updateContext(session: DialogueSession, exchange: DialogueExchange): Promise<void> {
    const context = session.currentContext;
    
    // Update phase based on content progression
    if (exchange.human.type === 'decision' && context.phase === 'analysis') {
      context.phase = 'validation';
    } else if (exchange.ai.analysisType === 'recommendation' && context.phase === 'synthesis') {
      context.phase = 'implementation';
    }

    // Update priority based on warnings or critical issues
    if (exchange.ai.warnings && exchange.ai.warnings.length > 0) {
      context.priority = 'high';
    }

    // Add tags based on content
    const contentTags = this.extractTags(exchange.human.content);
    context.tags = [...new Set([...context.tags, ...contentTags])];

    // Update metadata
    context.metadata.lastAnalysisType = exchange.ai.analysisType;
    context.metadata.totalExchanges = session.exchanges.length;
  }

  // Helper methods

  private getDefaultAnalysisTypes(inputType: string): ('axiom' | 'historical' | 'narrative' | 'consequences')[] {
    switch (inputType) {
      case 'proposal':
      case 'decision':
        return ['axiom', 'historical', 'consequences'];
      case 'story':
        return ['axiom', 'narrative'];
      case 'question':
        return ['historical'];
      default:
        return ['axiom'];
    }
  }

  private mapToAIAnalysisType(inputType: string): 'axiom' | 'historical' | 'narrative' | 'decision' | 'precedent' {
    switch (inputType) {
      case 'decision':
      case 'proposal':
        return 'decision';
      case 'story':
        return 'narrative';
      case 'question':
        return 'precedent';
      default:
        return 'axiom';
    }
  }

  private buildContextString(context: DialogueContext, humanInput: HumanInput): string {
    return [
      `Session Topic: ${context.topic}`,
      `Current Phase: ${context.phase}`,
      `Priority: ${context.priority}`,
      `Tags: ${context.tags.join(', ')}`,
      humanInput.context ? `Additional Context: ${humanInput.context}` : ''
    ].filter(Boolean).join('\n');
  }

  private generateFallbackResponse(humanInput: HumanInput, context: DialogueContext): string {
    return `I acknowledge your ${humanInput.type}: "${humanInput.content.substring(0, 100)}..." 
    
    In the context of ${context.topic}, this relates to our current ${context.phase} phase. 
    While I cannot provide full AI analysis at this moment, I can offer that this appears to align with 
    the core TEC principles of operating within the Grey and embracing complexity.
    
    Let me suggest we continue exploring this through the lens of historical precedent and axiom alignment.`;
  }

  private determineAnalysisType(humanInput: HumanInput, aiResponse: AIResponse): AIResponse['analysisType'] {
    if (aiResponse.axiomAlignment && !aiResponse.axiomAlignment.isValid) {
      return 'challenge';
    }
    if (aiResponse.precedents && aiResponse.precedents.warnings.length > 0) {
      return 'validation';
    }
    if (humanInput.type === 'proposal') {
      return 'recommendation';
    }
    if (aiResponse.precedents && aiResponse.precedents.events.length > 0) {
      return 'precedent';
    }
    return 'synthesis';
  }

  private generateNextQuestions(
    humanInput: HumanInput,
    context: DialogueContext,
    aiResponse: AIResponse
  ): string[] {
    const questions: string[] = [];
    
    if (context.phase === 'exploration') {
      questions.push('What specific aspects of this situation concern you most?');
      questions.push('How does this relate to your broader vision for the project?');
    }
    
    if (aiResponse.axiomAlignment && aiResponse.axiomAlignment.violations.length > 0) {
      questions.push('How might we modify this to better align with our core axioms?');
    }
    
    if (aiResponse.precedents && aiResponse.precedents.events.length > 0) {
      questions.push('Which historical precedent seems most relevant to our situation?');
      questions.push('What lessons from these precedents should guide our approach?');
    }

    return questions.slice(0, 3); // Limit to 3 questions
  }

  private calculateNovelty(humanInput: HumanInput, session: DialogueSession): number {
    // Simple novelty calculation based on content similarity to previous exchanges
    const previousContent = session.exchanges.map(e => e.human.content).join(' ');
    const currentContent = humanInput.content.toLowerCase();
    
    // Count unique words (simple approach)
    const previousWords = new Set(previousContent.toLowerCase().split(' '));
    const currentWords = currentContent.split(' ');
    const newWords = currentWords.filter(word => !previousWords.has(word));
    
    return Math.min(1, newWords.length / currentWords.length);
  }

  private async generateSynthesisConclusion(
    humanInput: HumanInput,
    aiResponse: AIResponse,
    session: DialogueSession
  ): Promise<string> {
    try {
      const prompt = `
      Synthesize the following human-AI exchange into a coherent conclusion:
      
      Human Input (${humanInput.type}): "${humanInput.content}"
      Human Confidence: ${humanInput.confidence}
      
      AI Analysis: "${aiResponse.content}"
      AI Confidence: ${aiResponse.confidence}
      
      Context: ${session.topic} - ${session.currentContext.phase} phase
      
      Provide a synthesis that combines the human creativity with AI logic,
      acknowledging both strengths and creating a path forward.
      Maximum 200 words.
      `;
      
      return await this.asimov.complete(prompt);
    } catch (error) {
      return `Synthesis of human insight (${humanInput.type}) and AI analysis suggests a balanced approach that honors both creative vision and logical validation. The combination of human intuition and systematic analysis provides a stronger foundation for decision-making than either alone.`;
    }
  }

  private extractActionItems(humanInput: HumanInput, aiResponse: AIResponse): string[] {
    const items: string[] = [];
    
    if (humanInput.type === 'proposal' || humanInput.type === 'decision') {
      items.push('Document decision rationale');
      items.push('Monitor outcomes and adjust as needed');
    }
    
    if (aiResponse.recommendations) {
      items.push(...aiResponse.recommendations.slice(0, 3));
    }
    
    return items;
  }

  private extractTags(content: string): string[] {
    // Simple tag extraction based on common TEC themes
    const tagPatterns = {
      'power': /power|control|authority|dominance/i,
      'oligarchy': /oligarch|elite|ruling class|establishment/i,
      'duality': /dual|both|two sides|paradox/i,
      'historical': /history|past|precedent|ancient|previous/i,
      'technology': /tech|AI|digital|innovation|advancement/i,
      'ethics': /moral|ethical|right|wrong|values/i,
      'narrative': /story|narrative|frame|perspective/i
    };

    const tags: string[] = [];
    for (const [tag, pattern] of Object.entries(tagPatterns)) {
      if (pattern.test(content)) {
        tags.push(tag);
      }
    }
    
    return tags;
  }

  private generateSessionId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private generateExchangeId(): string {
    return `exchange_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Get session by ID
   */
  getSession(sessionId: string): DialogueSession | undefined {
    return this.sessions.get(sessionId);
  }

  /**
   * Get all sessions for a user
   */
  getUserSessions(userId: string): DialogueSession[] {
    return Array.from(this.sessions.values()).filter(session => session.userId === userId);
  }

  /**
   * Archive completed session
   */
  archiveSession(sessionId: string): boolean {
    const session = this.sessions.get(sessionId);
    if (session) {
      session.status = 'archived';
      return true;
    }
    return false;
  }
}

// Factory function to create configured dialogue interface
export function createDialogueInterface(
  asimov: AsimovService,
  axiomEngine: AxiomEngine,
  memoryCore: MemoryCore
): DialogueInterface {
  return new DialogueInterface(asimov, axiomEngine, memoryCore);
}
