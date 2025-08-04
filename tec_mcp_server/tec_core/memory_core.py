"""
TEC MEMORY CORE
The historical precedent database and contextual memory system

This module manages connections to the TEC Memory database (PostgreSQL + Vector DB)
and provides semantic search capabilities for historical context and precedents.
"""

import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import sqlite3
import json

logger = logging.getLogger(__name__)

class MemoryCore:
    """
    The Memory Core - Historical Context and Precedent Database
    
    Manages the collective memory of TEC, providing historical context
    and precedent-based insights for decision making.
    """
    
    def __init__(self):
        self.status = "INITIALIZING"
        self.connection = None
        self.connection_string = os.getenv('DATABASE_URL', '')
        self.query_history = []
        
    def initialize(self):
        """Initialize the Memory Core and database connections"""
        logger.info("🧠 Initializing Memory Core...")
        
        try:
            if self.connection_string:
                if self.connection_string.startswith('sqlite:'):
                    # SQLite connection for development
                    db_path = self.connection_string.replace('sqlite:///', '')
                    self.connection = sqlite3.connect(db_path, check_same_thread=False)
                    self.connection.row_factory = sqlite3.Row  # For dict-like access
                    logger.info("✅ SQLite database connection established")
                else:
                    # PostgreSQL connection for production
                    import psycopg2
                    from psycopg2.extras import RealDictCursor
                    self.connection = psycopg2.connect(
                        self.connection_string,
                        cursor_factory=RealDictCursor
                    )
                    logger.info("✅ PostgreSQL database connection established")
            else:
                logger.warning("⚠️  No database URL provided, running in offline mode")
            
            # Initialize memory schema if needed
            self._ensure_memory_schema()
            
            self.status = "OPERATIONAL"
            logger.info("✅ Memory Core operational")
            
        except Exception as e:
            self.status = "ERROR"
            logger.error(f"Memory Core initialization failed: {str(e)}")
            # Don't raise - allow system to run in degraded mode
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the Memory Core"""
        return {
            'status': self.status,
            'database_connected': self.connection is not None,
            'queries_performed': len(self.query_history),
            'last_query': self.query_history[-1]['timestamp'] if self.query_history else None
        }
    
    def _ensure_memory_schema(self):
        """Ensure the required database schema exists"""
        if not self.connection:
            return
            
        try:
            cursor = self.connection.cursor()
            
            # Create core memory tables (SQLite compatible)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tec_memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    memory_type VARCHAR(50) NOT NULL,
                    context TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                );
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tec_precedents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    precedent_type VARCHAR(50) NOT NULL,
                    historical_context TEXT,
                    axiom_alignment TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                );
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tec_lore (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entity_name VARCHAR(255) NOT NULL,
                    entity_type VARCHAR(100) NOT NULL,
                    lore_content TEXT NOT NULL,
                    world_context TEXT,
                    relationships TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create indexes for better performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_memories_type 
                ON tec_memories(memory_type);
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_precedents_type 
                ON tec_precedents(precedent_type);
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_lore_entity 
                ON tec_lore(entity_name, entity_type);
            """)
            
            self.connection.commit()
            cursor.close()
            logger.info("Memory schema validated/created")
            
        except Exception as e:
            logger.error(f"Schema creation error: {str(e)}")
            if hasattr(self.connection, 'rollback'):
                self.connection.rollback()
    
    def semantic_search(self, query: str, context_type: str = 'general', limit: int = 10) -> List[Dict[str, Any]]:
        """
        Perform semantic search across the memory database
        
        Args:
            query: Search query
            context_type: Type of context to search (general, lore, precedent)
            limit: Maximum number of results
            
        Returns:
            List of relevant memories/precedents
        """
        try:
            results = []
            
            # Log the query
            query_record = {
                'timestamp': datetime.now().isoformat(),
                'query': query,
                'context_type': context_type
            }
            self.query_history.append(query_record)
            
            if not self.connection:
                # Offline mode - return mock results
                return self._get_offline_results(query, context_type, limit)
            
            cursor = self.connection.cursor()
            
            try:
                if context_type == 'lore':
                    cursor.execute("""
                        SELECT entity_name, entity_type, lore_content, world_context
                        FROM tec_lore
                        WHERE lore_content LIKE ? OR entity_name LIKE ?
                        ORDER BY created_at DESC
                        LIMIT ?
                    """, (f'%{query}%', f'%{query}%', limit))
                    
                elif context_type == 'precedent':
                    cursor.execute("""
                        SELECT title, description, precedent_type, historical_context, axiom_alignment
                        FROM tec_precedents
                        WHERE description LIKE ? OR title LIKE ?
                        ORDER BY created_at DESC
                        LIMIT ?
                    """, (f'%{query}%', f'%{query}%', limit))
                    
                else:  # general memory search
                    cursor.execute("""
                        SELECT content, memory_type, context, metadata
                        FROM tec_memories
                        WHERE content LIKE ?
                        ORDER BY created_at DESC
                        LIMIT ?
                    """, (f'%{query}%', limit))
                
                rows = cursor.fetchall()
                results = [dict(row) for row in rows]
                
            finally:
                cursor.close()
            
            logger.info(f"Memory search returned {len(results)} results for query: {query}")
            return results
            
        except Exception as e:
            logger.error(f"Semantic search error: {str(e)}")
            return []
    
    def _get_offline_results(self, query: str, context_type: str, limit: int) -> List[Dict[str, Any]]:
        """Provide mock results when database is unavailable"""
        # This would be enhanced with local file-based search in production
        return [
            {
                'content': f"Offline result for query: {query}",
                'memory_type': 'system',
                'context': {'offline_mode': True},
                'metadata': {'generated': datetime.now().isoformat()}
            }
        ]
    
    def store_memory(self, content: str, memory_type: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Store a new memory in the database
        
        Args:
            content: The content to store
            memory_type: Type of memory (decision, precedent, lore, etc.)
            context: Additional context information
            
        Returns:
            Success status
        """
        try:
            if not self.connection:
                logger.warning("Cannot store memory - no database connection")
                return False
            
            cursor = self.connection.cursor()
            
            try:
                cursor.execute("""
                    INSERT INTO tec_memories (content, memory_type, context, metadata)
                    VALUES (?, ?, ?, ?)
                """, (
                    content,
                    memory_type,
                    json.dumps(context or {}),
                    json.dumps({
                        'stored_at': datetime.now().isoformat(),
                        'source': 'asimov_engine'
                    })
                ))
                
                self.connection.commit()
                logger.info(f"Memory stored: {memory_type}")
                return True
                
            finally:
                cursor.close()
                
        except Exception as e:
            logger.error(f"Memory storage error: {str(e)}")
            if self.connection:
                self.connection.rollback()
            return False
    
    def get_relevant_context(self, input_text: str, max_context_items: int = 5) -> Dict[str, Any]:
        """
        Get relevant historical context for a given input
        
        This is used by the hybrid synthesis system to provide historical
        perspective on creative inputs.
        """
        try:
            # Search across different context types
            lore_context = self.semantic_search(input_text, 'lore', max_context_items)
            precedent_context = self.semantic_search(input_text, 'precedent', max_context_items)
            memory_context = self.semantic_search(input_text, 'general', max_context_items)
            
            return {
                'lore': lore_context,
                'precedents': precedent_context,
                'memories': memory_context,
                'context_timestamp': datetime.now().isoformat(),
                'query': input_text
            }
            
        except Exception as e:
            logger.error(f"Context retrieval error: {str(e)}")
            return {
                'lore': [],
                'precedents': [],
                'memories': [],
                'error': str(e)
            }
    
    def add_precedent(self, title: str, description: str, precedent_type: str, 
                     historical_context: Optional[Dict[str, Any]] = None) -> bool:
        """Add a new historical precedent to the database"""
        try:
            if not self.connection:
                logger.warning("Cannot add precedent - no database connection")
                return False
            
            cursor = self.connection.cursor()
            
            try:
                cursor.execute("""
                    INSERT INTO tec_precedents (title, description, precedent_type, historical_context)
                    VALUES (?, ?, ?, ?)
                """, (
                    title,
                    description,
                    precedent_type,
                    json.dumps(historical_context or {})
                ))
                
                self.connection.commit()
                logger.info(f"Precedent added: {title}")
                return True
                
            finally:
                cursor.close()
                
        except Exception as e:
            logger.error(f"Precedent addition error: {str(e)}")
            if self.connection:
                self.connection.rollback()
            return False
    
    def add_lore_entry(self, entity_name: str, entity_type: str, lore_content: str,
                      world_context: Optional[Dict[str, Any]] = None) -> bool:
        """Add a new lore entry to the database"""
        try:
            if not self.connection:
                logger.warning("Cannot add lore - no database connection")
                return False
            
            cursor = self.connection.cursor()
            
            try:
                cursor.execute("""
                    INSERT INTO tec_lore (entity_name, entity_type, lore_content, world_context)
                    VALUES (?, ?, ?, ?)
                """, (
                    entity_name,
                    entity_type,
                    lore_content,
                    json.dumps(world_context or {})
                ))
                
                self.connection.commit()
                logger.info(f"Lore entry added: {entity_name} ({entity_type})")
                return True
                
            finally:
                cursor.close()
                
        except Exception as e:
            logger.error(f"Lore addition error: {str(e)}")
            if self.connection:
                self.connection.rollback()
            return False
    
    def close(self):
        """Close database connections"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Memory Core database connection closed")
