/**
 * TEC Server - The Constitutional Platform Server
 * 
 * This server provides the RESTful API and real-time capabilities
 * for The Elidoras Codex platform.
 */

import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import { createServer } from 'http';
import { WebSocketServer, WebSocket } from 'ws';
import { IncomingMessage } from 'http';
import { TECSystem, TECConfig } from './core/TECSystem';

const app = express();
const server = createServer(app);
const wss = new WebSocketServer({ server });

// Configuration
const config: TECConfig = {
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
  },
  features: {
    enableCommunityPlatform: process.env.ENABLE_COMMUNITY === 'true',
    enableNarrativeGenerator: process.env.ENABLE_NARRATIVE === 'true',
    enableAdvancedAnalytics: process.env.ENABLE_ANALYTICS === 'true'
  }
};

// Initialize TEC System
const tec = new TECSystem(config);

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

// Health check endpoint
app.get('/health', async (req, res) => {
  try {
    const status = await tec.getStatus();
    res.json({
      ...status,
      message: status.status === 'operational' 
        ? 'TEC System is operational - Ready to architect the future'
        : 'TEC System experiencing issues - We adapt and overcome'
    });
  } catch (error) {
    res.status(500).json({
      error: 'Health check failed',
      status: 'offline'
    });
  }
});

// System information endpoints
app.get('/api/axioms', (req, res) => {
  const axioms = tec.getAxioms();
  res.json({
    axioms,
    count: Object.keys(axioms).length,
    message: 'The foundational principles that guide all decisions'
  });
});

app.get('/api/memory/stats', (req, res) => {
  const stats = tec.getMemoryStats();
  res.json({
    ...stats,
    message: 'Historical wisdom informing present action'
  });
});

app.get('/api/status', async (req, res) => {
  try {
    const status = await tec.getStatus();
    res.json(status);
  } catch (error) {
    res.status(500).json({
      error: 'Status check failed'
    });
  }
});

// Analysis endpoints
app.post('/api/analyze', async (req, res) => {
  try {
    const { content, type = 'analyze', context, userId } = req.body;
    
    if (!content) {
      return res.status(400).json({
        error: 'Content is required for analysis'
      });
    }

    const result = await tec.analyze({
      content,
      type,
      context,
      userId
    });

    res.json({
      ...result,
      timestamp: new Date().toISOString(),
      message: 'Analysis complete - Knowledge becomes wisdom through understanding'
    });

  } catch (error) {
    res.status(500).json({
      error: 'Analysis failed',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
});

app.post('/api/validate', async (req, res) => {
  try {
    const { content } = req.body;
    
    if (!content) {
      return res.status(400).json({
        error: 'Content is required for validation'
      });
    }

    const isValid = await tec.quickValidate(content);
    
    res.json({
      valid: isValid,
      content,
      timestamp: new Date().toISOString(),
      message: isValid 
        ? 'Content aligns with TEC axioms' 
        : 'Content requires refinement to align with TEC principles'
    });

  } catch (error) {
    res.status(500).json({
      error: 'Validation failed',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
});

app.post('/api/precedents', async (req, res) => {
  try {
    const { situation, context } = req.body;
    
    if (!situation) {
      return res.status(400).json({
        error: 'Situation description is required'
      });
    }

    const precedents = await tec.findPrecedents(situation, context);
    
    res.json({
      ...precedents,
      timestamp: new Date().toISOString(),
      message: 'Historical wisdom illuminates the path forward'
    });

  } catch (error) {
    res.status(500).json({
      error: 'Precedent search failed',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
});

// Dialogue endpoints
app.post('/api/dialogue/start', async (req, res) => {
  try {
    const { userId, topic, context } = req.body;
    
    if (!userId || !topic) {
      return res.status(400).json({
        error: 'userId and topic are required'
      });
    }

    const session = await tec.startDialogue(userId, topic, context);
    
    res.json({
      session,
      message: 'Dialogue initiated - The Ellison and Asimov await your contribution'
    });

  } catch (error) {
    res.status(500).json({
      error: 'Failed to start dialogue',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
});

app.post('/api/dialogue/:sessionId/continue', async (req, res) => {
  try {
    const { sessionId } = req.params;
    const { input, inputType = 'statement' } = req.body;
    
    if (!input) {
      return res.status(400).json({
        error: 'Input is required to continue dialogue'
      });
    }

    const response = await tec.continueDialogue(sessionId, input, inputType);
    
    res.json({
      response,
      sessionId,
      message: 'Synthesis achieved through collaborative intelligence'
    });

  } catch (error) {
    res.status(500).json({
      error: 'Failed to continue dialogue',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
});

// WebSocket handling for real-time collaboration
wss.on('connection', (ws: WebSocket, req: IncomingMessage) => {
  console.log('New WebSocket connection established');
  
  ws.on('message', async (data: Buffer) => {
    try {
      const message = JSON.parse(data.toString());
      
      switch (message.type) {
        case 'dialogue_input':
          if (message.sessionId && message.input) {
            const response = await tec.continueDialogue(
              message.sessionId, 
              message.input, 
              message.inputType
            );
            ws.send(JSON.stringify({
              type: 'dialogue_response',
              sessionId: message.sessionId,
              response
            }));
          }
          break;
          
        case 'quick_validate':
          if (message.content) {
            const isValid = await tec.quickValidate(message.content);
            ws.send(JSON.stringify({
              type: 'validation_result',
              content: message.content,
              valid: isValid
            }));
          }
          break;
          
        case 'ping':
          ws.send(JSON.stringify({ type: 'pong' }));
          break;
          
        default:
          ws.send(JSON.stringify({
            type: 'error',
            message: 'Unknown message type'
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
    console.log('WebSocket connection closed');
  });

  // Send welcome message
  ws.send(JSON.stringify({
    type: 'welcome',
    message: 'Connected to TEC System - Real-time constitutional collaboration enabled',
    timestamp: new Date().toISOString()
  }));
});

// Error handling middleware
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('Server error:', err);
  res.status(500).json({
    error: 'Internal server error',
    message: 'The system encountered an unexpected error - Resilience is our strength'
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not found',
    message: 'The requested resource does not exist in this constitutional framework'
  });
});

// Server startup
const PORT = process.env.PORT || 3001;

async function startServer() {
  try {
    console.log('🚀 Starting The Elidoras Codex Server...');
    
    // Initialize TEC System
    await tec.initialize();
    
    // Start HTTP server
    server.listen(PORT, () => {
      console.log(`🌟 TEC Server operational on port ${PORT}`);
      console.log(`📖 Health check: http://localhost:${PORT}/health`);
      console.log(`🔗 API endpoints: http://localhost:${PORT}/api/*`);
      console.log(`⚡ WebSocket ready for real-time collaboration`);
      console.log('');
      console.log('🎯 "We are not building an app. We are architecting a civilization." - The Architect');
      console.log('');
      console.log('STATUS: OPERATIONAL - Ready to reshape the future');
    });

    // Graceful shutdown handling
    process.on('SIGTERM', gracefulShutdown);
    process.on('SIGINT', gracefulShutdown);

  } catch (error) {
    console.error('❌ Failed to start TEC Server:', error);
    process.exit(1);
  }
}

async function gracefulShutdown() {
  console.log('🛑 Initiating graceful shutdown...');
  
  try {
    await tec.shutdown();
    server.close(() => {
      console.log('✅ TEC Server shutdown complete');
      process.exit(0);
    });
  } catch (error) {
    console.error('❌ Error during shutdown:', error);
    process.exit(1);
  }
}

// Start the server
startServer();

export { app, server, tec };
