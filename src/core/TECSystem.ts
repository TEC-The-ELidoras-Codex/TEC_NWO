/**
 * The Elidoras Codex (TEC) System - Main Integration Hub
 * 
 * This is the central nervous system that orchestrates all components
 * of TEC into a unified platform for the new constitutional framework.
 */

import { AsimovService } from './ai/AsimovService';
import { AxiomEngine } from './axioms/AxiomEngine';
import { MemoryCore } from './memory/MemoryCore';
import { DialogueInterface, createDialogueInterface } from './dialogue/DialogueInterface';

export interface TECConfig {
  azureOpenAI?: {
    apiKey: string;
    endpoint: string;
    model?: string;
  };
  database?: {
    connectionString: string;
  };
  security?: {
    encryptionKey: string;
    jwtSecret: string;
  };
  features?: {
    enableCommunityPlatform?: boolean;
    enableNarrativeGenerator?: boolean;
    enableAdvancedAnalytics?: boolean;
  };
}

export interface TECStatus {
  version: string;
  status: 'initializing' | 'operational' | 'degraded' | 'offline';
  components: {
    asimov: 'online' | 'offline' | 'degraded';
    axiomEngine: 'online' | 'offline' | 'degraded';
    memoryCore: 'online' | 'offline' | 'degraded';
    dialogueInterface: 'online' | 'offline' | 'degraded';
  };
  metrics: {
    totalSessions: number;
    totalExchanges: number;
    totalValidations: number;
    avgAxiomCompliance: number;
    systemUptime: number;
  };
  lastHealthCheck: Date;
}

export interface TECAnalysisRequest {
  content: string;
  type: 'validate' | 'analyze' | 'synthesize' | 'precedent' | 'narrative';
  context?: string;
  userId?: string;
  sessionId?: string;
}

export interface TECAnalysisResult {
  content: string;
  analysis: {
    axiomCompliance: number;
    historicalGrounding: number;
    narrativeStrength: number;
    overallScore: number;
  };
  warnings: string[];
  recommendations: string[];
  precedents: string[];
  nextSteps: string[];
  confidence: number;
}

export class TECSystem {
  private config: TECConfig;
  private asimov: AsimovService;
  private axiomEngine: AxiomEngine;
  private memoryCore: MemoryCore;
  private dialogueInterface: DialogueInterface;
  private startTime: Date;
  private healthCheckInterval?: NodeJS.Timeout;

  constructor(config: TECConfig = {}) {
    this.config = config;
    this.startTime = new Date();
    
    // Initialize core components
    this.asimov = new AsimovService(config.azureOpenAI?.apiKey);
    this.axiomEngine = new AxiomEngine(this.asimov);
    this.memoryCore = new MemoryCore();
    this.dialogueInterface = createDialogueInterface(
      this.asimov, 
      this.axiomEngine, 
      this.memoryCore
    );
  }

  /**
   * Initialize the TEC system
   */
  async initialize(): Promise<void> {
    console.log('🚀 Initializing The Elidoras Codex System...');
    
    try {
      // Test AI service connection
      console.log('🧠 Testing Asimov Service...');
      const asimovHealthy = await this.asimov.healthCheck();
      if (!asimovHealthy) {
        console.warn('⚠️  Asimov Service health check failed - running in degraded mode');
      } else {
        console.log('✅ Asimov Service operational');
      }

      // Initialize axiom engine
      console.log('⚖️  Initializing Axiom Engine...');
      const axioms = this.axiomEngine.getAllAxioms();
      console.log(`✅ Axiom Engine loaded with ${Object.keys(axioms).length} foundational axioms`);

      // Initialize memory core
      console.log('🧠 Initializing Memory Core...');
      const memoryStats = this.memoryCore.getStats();
      console.log(`✅ Memory Core loaded with ${memoryStats.totalEvents} events, ${memoryStats.totalPatterns} patterns`);

      // Start health monitoring
      this.startHealthMonitoring();

      console.log('🎯 TEC System initialization complete - STATUS: OPERATIONAL');
      console.log('📖 "The ultimate power is not the ability to act, but the ability to control the narrative that defines the action." - The Architect');
      
    } catch (error) {
      console.error('❌ TEC System initialization failed:', error);
      throw error;
    }
  }

  /**
   * Perform comprehensive analysis using all TEC components
   */
  async analyze(request: TECAnalysisRequest): Promise<TECAnalysisResult> {
    const results: Partial<TECAnalysisResult> = {
      warnings: [],
      recommendations: [],
      precedents: [],
      nextSteps: []
    };

    try {
      // Axiom validation
      const axiomResult = await this.axiomEngine.validateContent({
        content: request.content,
        contentType: this.mapRequestTypeToContentType(request.type)
      });

      // Historical precedent analysis
      const precedentResult = await this.memoryCore.findPrecedents({
        situation: request.content,
        context: request.context,
        minRelevance: 0.3
      });

      // AI analysis
      const aiAnalysis = await this.asimov.analyze({
        content: request.content,
        context: request.context || '',
        analysisType: this.mapRequestTypeToAIType(request.type)
      });

      // Combine results
      results.content = aiAnalysis.analysis;
      results.analysis = {
        axiomCompliance: axiomResult.score,
        historicalGrounding: precedentResult.confidence,
        narrativeStrength: request.type === 'narrative' ? 0.8 : 0.6, // Placeholder
        overallScore: (axiomResult.score + precedentResult.confidence + 0.7) / 3
      };

      results.warnings = [
        ...axiomResult.violations.filter(v => v.severity === 'HIGH' || v.severity === 'CRITICAL')
          .map(v => v.description),
        ...precedentResult.warnings,
        ...(aiAnalysis.warnings || [])
      ];

      results.recommendations = [
        ...axiomResult.recommendations,
        ...precedentResult.recommendations,
        ...(aiAnalysis.recommendations || [])
      ];

      results.precedents = precedentResult.events.map(e => 
        `${e.title} (${e.period}): ${e.lessons.slice(0, 2).join(', ')}`
      );

      results.nextSteps = this.generateNextSteps(request, results as TECAnalysisResult);
      results.confidence = (axiomResult.score + precedentResult.confidence + aiAnalysis.confidence) / 3;

    } catch (error) {
      results.warnings!.push(`Analysis error: ${error instanceof Error ? error.message : String(error)}`);
      results.confidence = 0.3;
      results.content = 'Analysis completed with errors. See warnings for details.';
      results.analysis = {
        axiomCompliance: 0.5,
        historicalGrounding: 0.5,
        narrativeStrength: 0.5,
        overallScore: 0.5
      };
    }

    return results as TECAnalysisResult;
  }

  /**
   * Start a new dialogue session
   */
  async startDialogue(userId: string, topic: string, context?: any) {
    return await this.dialogueInterface.startSession(userId, topic, context);
  }

  /**
   * Continue a dialogue session
   */
  async continueDialogue(sessionId: string, userInput: string, inputType: string = 'statement') {
    return await this.dialogueInterface.processInput(sessionId, {
      content: userInput,
      type: inputType as any,
      confidence: 0.8
    });
  }

  /**
   * Quick validation against axioms
   */
  async quickValidate(content: string): Promise<boolean> {
    return await this.axiomEngine.quickValidate(content);
  }

  /**
   * Find historical precedents
   */
  async findPrecedents(situation: string, context?: string) {
    return await this.memoryCore.findPrecedents({
      situation,
      context,
      minRelevance: 0.3,
      maxResults: 5
    });
  }

  /**
   * Get system status and metrics
   */
  async getStatus(): Promise<TECStatus> {
    const asimovHealthy = await this.asimov.healthCheck();
    const memoryStats = this.memoryCore.getStats();
    
    // Get dialogue statistics
    const allSessions = Array.from(this.dialogueInterface['sessions'].values());
    const totalExchanges = allSessions.reduce((sum, session) => sum + session.exchanges.length, 0);
    
    // Calculate average axiom compliance (placeholder)
    const avgAxiomCompliance = 0.75;

    return {
      version: '0.1.0-genesis',
      status: asimovHealthy ? 'operational' : 'degraded',
      components: {
        asimov: asimovHealthy ? 'online' : 'offline',
        axiomEngine: 'online',
        memoryCore: 'online',
        dialogueInterface: 'online'
      },
      metrics: {
        totalSessions: allSessions.length,
        totalExchanges,
        totalValidations: 0, // Would track this in production
        avgAxiomCompliance,
        systemUptime: Date.now() - this.startTime.getTime()
      },
      lastHealthCheck: new Date()
    };
  }

  /**
   * Get axiom information
   */
  getAxioms() {
    return this.axiomEngine.getAllAxioms();
  }

  /**
   * Get memory core statistics
   */
  getMemoryStats() {
    return this.memoryCore.getStats();
  }

  /**
   * Shut down the system gracefully
   */
  async shutdown(): Promise<void> {
    console.log('🛑 Shutting down TEC System...');
    
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval);
    }

    // Archive active sessions
    const allSessions = Array.from(this.dialogueInterface['sessions'].values());
    allSessions.forEach(session => {
      if (session.status === 'active') {
        this.dialogueInterface.archiveSession(session.id);
      }
    });

    console.log('✅ TEC System shutdown complete');
  }

  // Private helper methods

  private mapRequestTypeToContentType(type: string): 'story' | 'decision' | 'policy' | 'dialogue' | 'narrative' {
    switch (type) {
      case 'narrative':
        return 'story';
      case 'validate':
      case 'analyze':
        return 'policy';
      case 'synthesize':
        return 'dialogue';
      default:
        return 'narrative';
    }
  }

  private mapRequestTypeToAIType(type: string): 'axiom' | 'historical' | 'narrative' | 'decision' | 'precedent' {
    switch (type) {
      case 'validate':
        return 'axiom';
      case 'precedent':
        return 'precedent';
      case 'narrative':
        return 'narrative';
      case 'synthesize':
        return 'decision';
      default:
        return 'historical';
    }
  }

  private generateNextSteps(request: TECAnalysisRequest, result: TECAnalysisResult): string[] {
    const steps: string[] = [];

    if (result.analysis.axiomCompliance < 0.6) {
      steps.push('Revise content to better align with TEC axioms');
    }

    if (result.analysis.historicalGrounding < 0.5) {
      steps.push('Research additional historical precedents');
    }

    if (result.warnings.length > 0) {
      steps.push('Address identified warnings and risks');
    }

    if (request.type === 'analyze') {
      steps.push('Consider implementing recommendations');
      steps.push('Monitor outcomes and iterate');
    }

    return steps.length > 0 ? steps : ['Continue development based on analysis'];
  }

  private startHealthMonitoring(): void {
    this.healthCheckInterval = setInterval(async () => {
      try {
        const status = await this.getStatus();
        if (status.status === 'degraded') {
          console.warn('⚠️  TEC System health check: DEGRADED');
        }
      } catch (error) {
        console.error('❌ Health check failed:', error);
      }
    }, 300000); // Check every 5 minutes
  }
}

// Export factory function for easy setup
export function createTECSystem(config: TECConfig = {}): TECSystem {
  return new TECSystem(config);
}

// Export singleton for global access
export const tec = createTECSystem();
