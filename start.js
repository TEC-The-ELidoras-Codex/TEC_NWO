#!/usr/bin/env node

/**
 * TEC System Startup Script
 * 
 * This script initializes and starts The Elidoras Codex system
 * with proper environment validation and graceful startup.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ANSI color codes for terminal output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m'
};

class TECStartup {
  constructor() {
    this.projectRoot = process.cwd();
    this.requiredEnvVars = [
      'NODE_ENV',
      'PORT',
      'AZURE_OPENAI_API_KEY',
      'AZURE_OPENAI_ENDPOINT'
    ];
  }

  log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
  }

  error(message) {
    this.log(`❌ ${message}`, 'red');
  }

  success(message) {
    this.log(`✅ ${message}`, 'green');
  }

  info(message) {
    this.log(`ℹ️  ${message}`, 'blue');
  }

  warning(message) {
    this.log(`⚠️  ${message}`, 'yellow');
  }

  header(message) {
    this.log('', 'reset');
    this.log('='.repeat(60), 'cyan');
    this.log(`🎯 ${message}`, 'cyan');
    this.log('='.repeat(60), 'cyan');
    this.log('', 'reset');
  }

  async checkEnvironment() {
    this.header('ENVIRONMENT VALIDATION');

    // Check if .env file exists
    const envPath = path.join(this.projectRoot, '.env');
    if (!fs.existsSync(envPath)) {
      this.warning('.env file not found');
      
      const templatePath = path.join(this.projectRoot, '.env.template');
      if (fs.existsSync(templatePath)) {
        this.info('Copying .env.template to .env');
        fs.copyFileSync(templatePath, envPath);
        this.warning('Please configure your .env file with actual values');
      } else {
        this.error('No .env template found. Please create .env file manually.');
        return false;
      }
    } else {
      this.success('.env file found');
    }

    // Load environment variables
    require('dotenv').config({ path: envPath });

    // Check required environment variables
    const missingVars = this.requiredEnvVars.filter(varName => !process.env[varName]);
    
    if (missingVars.length > 0) {
      this.error(`Missing required environment variables: ${missingVars.join(', ')}`);
      this.info('Please configure these variables in your .env file');
      return false;
    }

    this.success('All required environment variables found');
    return true;
  }

  async checkDependencies() {
    this.header('DEPENDENCY VALIDATION');

    try {
      // Check if node_modules exists
      const nodeModulesPath = path.join(this.projectRoot, 'node_modules');
      if (!fs.existsSync(nodeModulesPath)) {
        this.warning('node_modules not found, installing dependencies...');
        execSync('npm install', { stdio: 'inherit' });
      }

      this.success('Dependencies verified');
      return true;
    } catch (error) {
      this.error(`Dependency installation failed: ${error.message}`);
      return false;
    }
  }

  async buildProject() {
    this.header('PROJECT BUILD');

    try {
      const distPath = path.join(this.projectRoot, 'dist');
      if (!fs.existsSync(distPath)) {
        this.info('Building TypeScript project...');
        execSync('npm run build', { stdio: 'inherit' });
      } else {
        this.info('Checking if rebuild is needed...');
        // Simple check - in a real system you'd compare timestamps
        execSync('npm run build', { stdio: 'inherit' });
      }

      this.success('Project build completed');
      return true;
    } catch (error) {
      this.error(`Build failed: ${error.message}`);
      return false;
    }
  }

  async checkDatabase() {
    this.header('DATABASE CONNECTIVITY');

    try {
      const databaseUrl = process.env.DATABASE_URL;
      if (!databaseUrl) {
        this.warning('DATABASE_URL not configured - running without persistent storage');
        return true;
      }

      // In a real implementation, we'd test the database connection
      this.info('Database connection configuration found');
      this.info('Database connectivity will be tested during startup');
      return true;
    } catch (error) {
      this.error(`Database check failed: ${error.message}`);
      return false;
    }
  }

  async checkAzureOpenAI() {
    this.header('AZURE OPENAI VALIDATION');

    const apiKey = process.env.AZURE_OPENAI_API_KEY;
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT;

    if (!apiKey || apiKey === 'your-azure-openai-api-key-here') {
      this.warning('Azure OpenAI API key not configured');
      this.info('System will run with limited AI capabilities');
      return true;
    }

    if (!endpoint || endpoint === 'https://your-openai-resource.openai.azure.com/') {
      this.warning('Azure OpenAI endpoint not configured');
      this.info('Please update AZURE_OPENAI_ENDPOINT in your .env file');
      return true;
    }

    this.success('Azure OpenAI configuration found');
    return true;
  }

  async startServer() {
    this.header('STARTING TEC SYSTEM');

    try {
      this.info('Initializing The Elidoras Codex...');
      this.log('', 'reset');
      this.log('🌟 "We are not building an app. We are architecting a civilization." - The Architect', 'magenta');
      this.log('', 'reset');
      
      // Start the compiled server
      const serverPath = path.join(this.projectRoot, 'dist', 'server.js');
      if (fs.existsSync(serverPath)) {
        this.info('Starting compiled server...');
        require(serverPath);
      } else {
        this.info('Starting development server...');
        require('ts-node/register');
        require(path.join(this.projectRoot, 'src', 'server.ts'));
      }

    } catch (error) {
      this.error(`Server startup failed: ${error.message}`);
      return false;
    }
  }

  async run() {
    try {
      this.log('🚀 The Elidoras Codex System Startup', 'bright');
      this.log('📖 "This is not a game. This is not a drill. This is the work."', 'magenta');

      // Run all validation checks
      const checks = [
        this.checkEnvironment(),
        this.checkDependencies(),
        this.buildProject(),
        this.checkDatabase(),
        this.checkAzureOpenAI()
      ];

      const results = await Promise.all(checks);
      
      if (results.every(result => result)) {
        this.success('All system checks passed');
        await this.startServer();
      } else {
        this.error('System checks failed - please resolve issues before starting');
        process.exit(1);
      }

    } catch (error) {
      this.error(`Startup failed: ${error.message}`);
      process.exit(1);
    }
  }
}

// Handle graceful shutdown
process.on('SIGTERM', () => {
  console.log('\n🛑 Received SIGTERM - shutting down gracefully...');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('\n🛑 Received SIGINT - shutting down gracefully...');
  process.exit(0);
});

// Start the system
const startup = new TECStartup();
startup.run().catch(error => {
  console.error('Fatal startup error:', error);
  process.exit(1);
});
