"""
PostgreSQL Database Connection Manager for Marketing System
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor, Json
from contextlib import contextmanager
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'postgres'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'briz-l'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'herahera')
}


class DatabaseManager:
    """Manages PostgreSQL database connections and operations"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or DB_CONFIG
        self._connection = None
    
    def get_connection(self):
        """Get or create database connection"""
        if self._connection is None or self._connection.closed:
            try:
                self._connection = psycopg2.connect(**self.config)
                print("✅ Database connected successfully")
            except Exception as e:
                print(f"❌ Database connection error: {e}")
                raise
        return self._connection
    
    @contextmanager
    def get_cursor(self, dict_cursor=True):
        """Context manager for database cursor"""
        conn = self.get_connection()
        cursor_factory = RealDictCursor if dict_cursor else None
        cursor = conn.cursor(cursor_factory=cursor_factory)
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"❌ Database error: {e}")
            raise
        finally:
            cursor.close()
    
    def execute_query(self, query: str, params: tuple = None, fetch: bool = True):
        """Execute a SQL query"""
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            return None
    
    def execute_many(self, query: str, params_list: list):
        """Execute multiple queries"""
        with self.get_cursor() as cursor:
            cursor.executemany(query, params_list)
    
    def close(self):
        """Close database connection"""
        if self._connection and not self._connection.closed:
            self._connection.close()
            print("✅ Database connection closed")
    
    def init_tables(self):
        """Initialize marketing database tables"""
        queries = [
            # Leads table
            """
            CREATE TABLE IF NOT EXISTS marketing_leads (
                user_id TEXT PRIMARY KEY,
                first_contact TIMESTAMP DEFAULT NOW(),
                last_interaction TIMESTAMP DEFAULT NOW(),
                total_messages INTEGER DEFAULT 0,
                symptoms TEXT[],
                surgeries_interested TEXT[],
                doctors_inquired TEXT[],
                lead_score INTEGER DEFAULT 0,
                lead_status TEXT DEFAULT 'new',
                booking_intent_detected BOOLEAN DEFAULT FALSE,
                conversation_history JSONB,
                created_at TIMESTAMP DEFAULT NOW()
            );
            """,
            
            # Follow-ups table
            """
            CREATE TABLE IF NOT EXISTS follow_ups (
                id SERIAL PRIMARY KEY,
                user_id TEXT REFERENCES marketing_leads(user_id),
                follow_up_type TEXT,
                sent_at TIMESTAMP DEFAULT NOW(),
                response_received BOOLEAN DEFAULT FALSE
            );
            """,
            
            # Conversion events table
            """
            CREATE TABLE IF NOT EXISTS conversion_events (
                id SERIAL PRIMARY KEY,
                user_id TEXT REFERENCES marketing_leads(user_id),
                event_type TEXT,
                event_data JSONB,
                created_at TIMESTAMP DEFAULT NOW()
            );
            """,
            
            # Analytics table
            """
            CREATE TABLE IF NOT EXISTS marketing_analytics (
                date DATE PRIMARY KEY DEFAULT CURRENT_DATE,
                total_leads INTEGER DEFAULT 0,
                hot_leads INTEGER DEFAULT 0,
                booking_intents INTEGER DEFAULT 0,
                follow_ups_sent INTEGER DEFAULT 0,
                follow_up_responses INTEGER DEFAULT 0
            );
            """,
            
            # Create indexes for performance
            """
            CREATE INDEX IF NOT EXISTS idx_leads_status ON marketing_leads(lead_status);
            CREATE INDEX IF NOT EXISTS idx_leads_score ON marketing_leads(lead_score DESC);
            CREATE INDEX IF NOT EXISTS idx_leads_last_interaction ON marketing_leads(last_interaction);
            CREATE INDEX IF NOT EXISTS idx_events_user ON conversion_events(user_id);
            CREATE INDEX IF NOT EXISTS idx_events_type ON conversion_events(event_type);
            """
        ]
        
        try:
            for query in queries:
                self.execute_query(query, fetch=False)
            print("✅ Marketing database tables initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing tables: {e}")
            raise


# Global database instance
db = DatabaseManager()


def init_marketing_database():
    """Initialize marketing database tables"""
    db.init_tables()


if __name__ == "__main__":
    # Test connection and initialize tables
    print("Testing database connection...")
    init_marketing_database()
    print("Database setup complete!")
