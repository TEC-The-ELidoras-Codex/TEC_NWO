# Multi-stage build for The Elidoras Codex
# Stage 1: Build the application
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY tsconfig.json ./

# Install dependencies
RUN npm ci --only=production && npm cache clean --force

# Copy source code
COPY src/ ./src/

# Build the application
RUN npm run build

# Stage 2: Production image
FROM node:18-alpine AS production

# Install security updates
RUN apk upgrade --no-cache

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S tecuser -u 1001

WORKDIR /app

# Copy built application from builder stage
COPY --from=builder --chown=tecuser:nodejs /app/dist ./dist
COPY --from=builder --chown=tecuser:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=tecuser:nodejs /app/package*.json ./

# Create logs directory
RUN mkdir -p /app/logs && chown tecuser:nodejs /app/logs

# Switch to non-root user
USER tecuser

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node dist/server/healthcheck.js || exit 1

# Labels for metadata
LABEL maintainer="The Elidoras Codex Team <team@elidorascodex.org>"
LABEL version="1.0.0"
LABEL description="The Elidoras Codex - A revolutionary Human-AI collaboration platform"
LABEL org.opencontainers.image.title="The Elidoras Codex"
LABEL org.opencontainers.image.description="Dynamic constitutional framework for building better systems"
LABEL org.opencontainers.image.url="https://github.com/Elidorascodex/the-elidoras-codex"
LABEL org.opencontainers.image.source="https://github.com/Elidorascodex/the-elidoras-codex"
LABEL org.opencontainers.image.vendor="The Elidoras Codex Project"
LABEL org.opencontainers.image.licenses="MIT"

# Environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Start the application
CMD ["node", "dist/server/index.js"]
