import { Pool } from 'pg';

const pool = new Pool({
  host: process.env.DB_HOST || 'rasa-brizl-tbycs9',
  port: parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME || 'briz-l',
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || 'herahera',
});

export async function runMigrations(): Promise<{ success: boolean; message: string; tables: string[] }> {
  const client = await pool.connect();
  const createdTables: string[] = [];
  
  try {
    console.log('🔄 Running database migrations...');
    
    // 1. Marketing Leads Table
    await client.query(`
      CREATE TABLE IF NOT EXISTS marketing_leads (
        user_id TEXT PRIMARY KEY,
        first_contact TIMESTAMP DEFAULT NOW(),
        last_interaction TIMESTAMP DEFAULT NOW(),
        total_messages INTEGER DEFAULT 0,
        symptoms TEXT[] DEFAULT '{}',
        surgeries_interested TEXT[] DEFAULT '{}',
        doctors_inquired TEXT[] DEFAULT '{}',
        lead_score INTEGER DEFAULT 0,
        lead_status TEXT DEFAULT 'new',
        booking_intent_detected BOOLEAN DEFAULT FALSE,
        conversation_history JSONB DEFAULT '[]'::jsonb,
        platform TEXT DEFAULT 'web',
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
      );
    `);
    createdTables.push('marketing_leads');
    
    // 2. Follow-ups Table
    await client.query(`
      CREATE TABLE IF NOT EXISTS follow_ups (
        id SERIAL PRIMARY KEY,
        user_id TEXT REFERENCES marketing_leads(user_id) ON DELETE CASCADE,
        follow_up_type TEXT,
        sent_at TIMESTAMP DEFAULT NOW(),
        response_received BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT NOW()
      );
    `);
    createdTables.push('follow_ups');
    
    // 3. Conversion Events Table
    await client.query(`
      CREATE TABLE IF NOT EXISTS conversion_events (
        id SERIAL PRIMARY KEY,
        user_id TEXT REFERENCES marketing_leads(user_id) ON DELETE CASCADE,
        event_type TEXT,
        event_data JSONB,
        created_at TIMESTAMP DEFAULT NOW()
      );
    `);
    createdTables.push('conversion_events');
    
    // 4. Marketing Analytics Table
    await client.query(`
      CREATE TABLE IF NOT EXISTS marketing_analytics (
        date DATE PRIMARY KEY DEFAULT CURRENT_DATE,
        total_leads INTEGER DEFAULT 0,
        hot_leads INTEGER DEFAULT 0,
        booking_intents INTEGER DEFAULT 0,
        follow_ups_sent INTEGER DEFAULT 0,
        follow_up_responses INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT NOW()
      );
    `);
    createdTables.push('marketing_analytics');
    
    // 5. AI Configuration Table
    await client.query(`
      CREATE TABLE IF NOT EXISTS ai_config (
        id SERIAL PRIMARY KEY,
        system_prompt TEXT,
        doctors JSONB DEFAULT '[]'::jsonb,
        surgeries JSONB DEFAULT '[]'::jsonb,
        scoring_weights JSONB DEFAULT '{}'::jsonb,
        platform_settings JSONB DEFAULT '{}'::jsonb,
        updated_at TIMESTAMP DEFAULT NOW(),
        created_at TIMESTAMP DEFAULT NOW()
      );
    `);
    createdTables.push('ai_config');
    
    // Create indexes for performance
    await client.query(`
      CREATE INDEX IF NOT EXISTS idx_leads_status ON marketing_leads(lead_status);
      CREATE INDEX IF NOT EXISTS idx_leads_score ON marketing_leads(lead_score DESC);
      CREATE INDEX IF NOT EXISTS idx_leads_last_interaction ON marketing_leads(last_interaction);
      CREATE INDEX IF NOT EXISTS idx_leads_platform ON marketing_leads(platform);
      CREATE INDEX IF NOT EXISTS idx_events_user ON conversion_events(user_id);
      CREATE INDEX IF NOT EXISTS idx_events_type ON conversion_events(event_type);
      CREATE INDEX IF NOT EXISTS idx_followups_user ON follow_ups(user_id);
    `);
    
    // Seed default AI config if not exists
    const configCheck = await client.query('SELECT COUNT(*) as count FROM ai_config');
    if (parseInt(configCheck.rows[0].count) === 0) {
      await client.query(`
        INSERT INTO ai_config (system_prompt, doctors, surgeries, scoring_weights, platform_settings)
        VALUES (
          'You are Vera, a friendly and professional medical assistant for Briz-L Clinic in Azerbaijan. You help patients with inquiries about cosmetic surgeries, provide information about doctors and procedures, and assist with booking consultations. Always be empathetic, professional, and helpful. Respond in the language the user prefers (Azerbaijani, Russian, or English).',
          '[]'::jsonb,
          '[]'::jsonb,
          '{"symptom_mentioned": 15, "surgery_interest": 25, "doctor_inquiry": 10, "booking_intent": 30, "price_inquiry": 10, "location_inquiry": 5, "repeat_visitor": 5}'::jsonb,
          '{"whatsapp_enabled": true, "telegram_enabled": true, "facebook_enabled": true, "instagram_enabled": true}'::jsonb
        );
      `);
      console.log('✅ Seeded default AI configuration');
    }
    
    console.log('✅ Database migrations completed successfully');
    
    return {
      success: true,
      message: 'All migrations completed successfully',
      tables: createdTables
    };
    
  } catch (error) {
    console.error('❌ Migration error:', error);
    return {
      success: false,
      message: `Migration failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
      tables: createdTables
    };
  } finally {
    client.release();
  }
}

export async function checkDatabaseConnection(): Promise<{ connected: boolean; error?: string }> {
  try {
    const client = await pool.connect();
    await client.query('SELECT 1');
    client.release();
    return { connected: true };
  } catch (error) {
    return { 
      connected: false, 
      error: error instanceof Error ? error.message : 'Unknown error' 
    };
  }
}

export async function getTableStats(): Promise<{ table: string; count: number }[]> {
  const client = await pool.connect();
  try {
    const tables = ['marketing_leads', 'follow_ups', 'conversion_events', 'marketing_analytics', 'ai_config'];
    const stats = [];
    
    for (const table of tables) {
      try {
        const result = await client.query(`SELECT COUNT(*) as count FROM ${table}`);
        stats.push({ table, count: parseInt(result.rows[0].count) });
      } catch {
        stats.push({ table, count: -1 }); // Table doesn't exist
      }
    }
    
    return stats;
  } finally {
    client.release();
  }
}

export { pool };