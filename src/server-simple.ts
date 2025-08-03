/**
 * TEC Server - Simplified Implementation Ready Version
 * 
 * This is a working version with the essential TEC functionality
 * for the Implementation Phase.
 */

import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import { createServer } from 'http';
import { WebSocketServer, WebSocket } from 'ws';
import { IncomingMessage } from 'http';

const app = express();
const server = createServer(app);
const wss = new WebSocketServer({ server });

// Basic configuration for Implementation Phase
const config = {
  azureOpenAI: {
    apiKey: process.env.AZURE_OPENAI_API_KEY || '',
    endpoint: process.env.AZURE_OPENAI_ENDPOINT || '',
    model: process.env.AZURE_OPENAI_MODEL || 'gpt-4'
  },
  database: {
    connectionString: process.env.DATABASE_URL || 'postgresql://localhost:5432/tec'
  },
  security: {
    encryptionKey: process.env.ENCRYPTION_KEY || 'development-key-not-secure',
    jwtSecret: process.env.JWT_SECRET || 'development-jwt-secret'
  }
};

// Middleware
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    }
  }
}));

app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000'],
  credentials: true
}));

app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.'
});
app.use('/api/', limiter);

// ====== IMPLEMENTATION PHASE - CORE ENDPOINTS ======

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'operational',
    message: 'TEC System is operational - Ready to architect the future',
    timestamp: new Date().toISOString(),
    phase: 'Implementation'
  });
});

// System status
app.get('/api/status', (req, res) => {
  res.json({
    status: 'operational',
    components: {
      axiomEngine: 'ready',
      asimovService: config.azureOpenAI.apiKey ? 'configured' : 'needs_credentials',
      memoryCore: 'initializing',
      dialogueInterface: 'ready'
    },
    phase: 'Implementation - Building the Machine',
    timestamp: new Date().toISOString()
  });
});

// The 8 Foundational Axioms
const AXIOMS = {
  1: "Narrative Supremacy - Stories shape reality more than facts alone",
  2: "Duality Principle - Truth exists in the tension between opposites", 
  3: "Flawed Hero Doctrine - Perfect heroes create imperfect worlds",
  4: "Justifiable Force Doctrine - Power without principle is tyranny",
  5: "Sovereign Accountability - Leaders bear the weight of their choices",
  6: "Authentic Performance - Genuine action over performative gestures",
  7: "Transparency Mandate - Sunlight disinfects corruption",
  8: "The Grey - Reject binary thinking, embrace contextual complexity"
};

app.get('/api/axioms', (req, res) => {
  res.json({
    axioms: AXIOMS,
    count: Object.keys(AXIOMS).length,
    message: 'The foundational principles that guide all decisions',
    philosophy: 'The Grey - Rejection of binary thinking'
  });
});

// ====== IMPLEMENTATION TASK: AXIOM VALIDATION ENDPOINT ======
// This is your first concrete coding task - the AxiomEngine brought to life

app.post('/api/validate', async (req, res) => {
  try {
    const { content, analysisType = 'narrative' } = req.body;
    
    if (!content) {
      return res.status(400).json({
        error: 'Content is required for validation',
        hint: 'Send JSON: { "content": "your text here" }'
      });
    }

    // Basic axiom validation logic (to be enhanced with AI)
    const validation = validateAgainstAxioms(content, analysisType);
    
    res.json({
      valid: validation.isValid,
      content,
      analysisType,
      axiomCompliance: validation.compliance,
      violations: validation.violations,
      suggestions: validation.suggestions,
      confidence: validation.confidence,
      timestamp: new Date().toISOString(),
      message: validation.isValid 
        ? 'Content aligns with TEC axioms - The Grey guides us well' 
        : 'Content requires refinement to align with TEC principles'
    });

  } catch (error) {
    res.status(500).json({
      error: 'Validation failed',
      details: error instanceof Error ? error.message : 'Unknown error',
      phase: 'Implementation - Building systems step by step'
    });
  }
});

// ====== AXIOM ENGINE IMPLEMENTATION ======
function validateAgainstAxioms(content: string, analysisType: string) {
  const results = {
    isValid: true,
    compliance: {} as Record<string, boolean>,
    violations: [] as string[],
    suggestions: [] as string[],
    confidence: 0.8
  };

  // Basic validation rules (to be enhanced with Azure OpenAI)
  const contentLower = content.toLowerCase();
  
  // Check against each axiom
  Object.entries(AXIOMS).forEach(([key, axiom]) => {
    const axiomKey = `axiom_${key}`;
    
    switch(key) {
      case '1': // Narrative Supremacy
        results.compliance[axiomKey] = contentLower.includes('story') || 
                                      contentLower.includes('narrative') ||
                                      contentLower.includes('experience');
        break;
      case '2': // Duality Principle  
        results.compliance[axiomKey] = !(contentLower.includes('always') && 
                                        contentLower.includes('never')) ||
                                      contentLower.includes('both') ||
                                      contentLower.includes('however');
        break;
      case '3': // Flawed Hero Doctrine
        results.compliance[axiomKey] = !contentLower.includes('perfect solution') &&
                                      !contentLower.includes('flawless');
        break;
      case '8': // The Grey
        results.compliance[axiomKey] = !contentLower.includes('black and white') &&
                                      !contentLower.includes('either/or');
        break;
      default:
        results.compliance[axiomKey] = true; // Default to passing for now
    }
    
    if (!results.compliance[axiomKey]) {
      results.isValid = false;
      results.violations.push(`Violates ${axiom}`);
      results.suggestions.push(`Consider how this content aligns with: ${axiom}`);
    }
  });

  return results;
}

// Basic WebSocket for real-time validation
wss.on('connection', (ws: WebSocket, req: IncomingMessage) => {
  console.log('TEC WebSocket connection established');
  
  ws.send(JSON.stringify({
    type: 'welcome',
    message: 'Connected to TEC - The constitutional framework awaits your input',
    axioms: Object.keys(AXIOMS).length,
    phase: 'Implementation'
  }));

  ws.on('message', async (data: Buffer) => {
    try {
      const message = JSON.parse(data.toString());
      
      if (message.type === 'validate' && message.content) {
        const validation = validateAgainstAxioms(message.content, message.analysisType || 'narrative');
        
        ws.send(JSON.stringify({
          type: 'validation_result',
          ...validation,
          content: message.content
        }));
      }
    } catch (error) {
      ws.send(JSON.stringify({
        type: 'error',
        message: 'Failed to process message',
        details: error instanceof Error ? error.message : 'Unknown error'
      }));
    }
  });

  ws.on('close', () => {
    console.log('TEC WebSocket connection closed');
  });
});

// Start the server
const PORT = process.env.PORT || 3000;

server.listen(PORT, () => {
  console.log('🏛️  TEC Server - Implementation Phase Active');
  console.log(`🚀 Server running on http://localhost:${PORT}`);
  console.log('📜 The 8 Axioms stand ready to guide us');
  console.log('🔍 Axiom validation endpoint: POST /api/validate');
  console.log('💡 WebSocket real-time validation available');
  console.log('⚡ Ready to build the machine that runs on chaos');
});

export default app;
