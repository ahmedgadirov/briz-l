import { Pool } from 'pg';

// Database connection
const pool = new Pool({
  host: process.env.DB_HOST || 'rasa-brizl-tbycs9',
  port: parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME || 'briz-l',
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || 'herahera',
});

// Analytics types
export interface LeadStats {
  total_leads: number;
  hot_leads: number;
  today_leads: number;
  warm_leads: number;
  cold_leads: number;
  new_leads: number;
  converted: number;
}

export interface Lead {
  user_id: string;
  first_contact: Date;
  last_interaction: Date;
  total_messages: number;
  symptoms: string[];
  surgeries_interested: string[];
  doctors_inquired: string[];
  lead_score: number;
  lead_status: string;
  booking_intent_detected: boolean;
  conversation_history: any[];
}

export interface DailyStats {
  date: string;
  total_leads: number;
  hot_leads: number;
  booking_intents: number;
  follow_ups_sent: number;
  follow_up_responses: number;
}

export interface ConversionFunnel {
  total_leads: number;
  engaged_leads: number;
  hot_leads: number;
  booking_intents: number;
  converted: number;
}

export interface ConversionRates {
  engagement_rate: number;
  hot_lead_rate: number;
  intent_rate: number;
  conversion_rate: number;
}

// Get lead statistics
export async function getLeadStats(): Promise<LeadStats> {
  try {
    const client = await pool.connect();
    
    // Total leads
    const totalResult = await client.query('SELECT COUNT(*) as count FROM marketing_leads;');
    const total_leads = parseInt(totalResult.rows[0]?.count || '0');
    
    // Hot leads
    const hotResult = await client.query("SELECT COUNT(*) as count FROM marketing_leads WHERE lead_status = 'hot';");
    const hot_leads = parseInt(hotResult.rows[0]?.count || '0');
    
    // Warm leads
    const warmResult = await client.query("SELECT COUNT(*) as count FROM marketing_leads WHERE lead_status = 'warm';");
    const warm_leads = parseInt(warmResult.rows[0]?.count || '0');
    
    // Cold leads
    const coldResult = await client.query("SELECT COUNT(*) as count FROM marketing_leads WHERE lead_status = 'cold';");
    const cold_leads = parseInt(coldResult.rows[0]?.count || '0');
    
    // New leads
    const newResult = await client.query("SELECT COUNT(*) as count FROM marketing_leads WHERE lead_status = 'new';");
    const new_leads = parseInt(newResult.rows[0]?.count || '0');
    
    // Today's leads
    const todayResult = await client.query("SELECT COUNT(*) as count FROM marketing_leads WHERE DATE(first_contact) = CURRENT_DATE;");
    const today_leads = parseInt(todayResult.rows[0]?.count || '0');
    
    // Converted
    const convertedResult = await client.query("SELECT COUNT(*) as count FROM marketing_leads WHERE lead_status = 'converted';");
    const converted = parseInt(convertedResult.rows[0]?.count || '0');
    
    client.release();
    
    return {
      total_leads,
      hot_leads,
      today_leads,
      warm_leads,
      cold_leads,
      new_leads,
      converted,
    };
  } catch (error) {
    console.error('Error getting lead stats:', error);
    return {
      total_leads: 0,
      hot_leads: 0,
      today_leads: 0,
      warm_leads: 0,
      cold_leads: 0,
      new_leads: 0,
      converted: 0,
    };
  }
}

// Get all leads with pagination
export async function getLeads(page: number = 1, limit: number = 20, status?: string): Promise<{ leads: Lead[]; total: number }> {
  try {
    const client = await pool.connect();
    const offset = (page - 1) * limit;
    
    let whereClause = '';
    const params: any[] = [];
    
    if (status && status !== 'all') {
      whereClause = 'WHERE lead_status = $1';
      params.push(status);
    }
    
    // Get total count
    const countQuery = `SELECT COUNT(*) as count FROM marketing_leads ${whereClause};`;
    const countResult = await client.query(countQuery, params);
    const total = parseInt(countResult.rows[0]?.count || '0');
    
    // Get leads
    const leadsQuery = `
      SELECT 
        user_id,
        first_contact,
        last_interaction,
        total_messages,
        symptoms,
        surgeries_interested,
        doctors_inquired,
        lead_score,
        lead_status,
        booking_intent_detected,
        conversation_history
      FROM marketing_leads
      ${whereClause}
      ORDER BY last_interaction DESC
      LIMIT $${params.length + 1} OFFSET $${params.length + 2};
    `;
    
    const leadsResult = await client.query(leadsQuery, [...params, limit, offset]);
    
    client.release();
    
    return {
      leads: leadsResult.rows,
      total,
    };
  } catch (error) {
    console.error('Error getting leads:', error);
    return { leads: [], total: 0 };
  }
}

// Get single lead details
export async function getLeadById(userId: string): Promise<Lead | null> {
  try {
    const client = await pool.connect();
    const result = await client.query(
      'SELECT * FROM marketing_leads WHERE user_id = $1;',
      [userId]
    );
    client.release();
    return result.rows[0] || null;
  } catch (error) {
    console.error('Error getting lead:', error);
    return null;
  }
}

// Update lead status
export async function updateLeadStatus(userId: string, status: string): Promise<boolean> {
  try {
    const client = await pool.connect();
    await client.query(
      'UPDATE marketing_leads SET lead_status = $1 WHERE user_id = $2;',
      [status, userId]
    );
    client.release();
    return true;
  } catch (error) {
    console.error('Error updating lead status:', error);
    return false;
  }
}

// Get daily stats for charts
export async function getDailyStats(days: number = 7): Promise<DailyStats[]> {
  try {
    const client = await pool.connect();
    const result = await client.query(`
      SELECT 
        date,
        COALESCE(total_leads, 0) as total_leads,
        COALESCE(hot_leads, 0) as hot_leads,
        COALESCE(booking_intents, 0) as booking_intents,
        COALESCE(follow_ups_sent, 0) as follow_ups_sent,
        COALESCE(follow_up_responses, 0) as follow_up_responses
      FROM marketing_analytics
      WHERE date >= CURRENT_DATE - INTERVAL '${days} days'
      ORDER BY date DESC;
    `);
    client.release();
    return result.rows;
  } catch (error) {
    console.error('Error getting daily stats:', error);
    return [];
  }
}

// Get conversion funnel
export async function getConversionFunnel(): Promise<{ funnel: ConversionFunnel; rates: ConversionRates }> {
  try {
    const client = await pool.connect();
    
    // Total leads
    const totalResult = await client.query('SELECT COUNT(*) as count FROM marketing_leads;');
    const total_leads = parseInt(totalResult.rows[0]?.count || '0');
    
    // Engaged leads (3+ messages)
    const engagedResult = await client.query('SELECT COUNT(*) as count FROM marketing_leads WHERE total_messages >= 3;');
    const engaged_leads = parseInt(engagedResult.rows[0]?.count || '0');
    
    // Hot leads
    const hotResult = await client.query("SELECT COUNT(*) as count FROM marketing_leads WHERE lead_status = 'hot';");
    const hot_leads = parseInt(hotResult.rows[0]?.count || '0');
    
    // Booking intents
    const intentResult = await client.query('SELECT COUNT(*) as count FROM marketing_leads WHERE booking_intent_detected = TRUE;');
    const booking_intents = parseInt(intentResult.rows[0]?.count || '0');
    
    // Converted
    const convertedResult = await client.query("SELECT COUNT(*) as count FROM marketing_leads WHERE lead_status = 'converted';");
    const converted = parseInt(convertedResult.rows[0]?.count || '0');
    
    client.release();
    
    // Calculate rates
    const engagement_rate = total_leads > 0 ? Math.round((engaged_leads / total_leads) * 100) : 0;
    const hot_lead_rate = total_leads > 0 ? Math.round((hot_leads / total_leads) * 100) : 0;
    const intent_rate = total_leads > 0 ? Math.round((booking_intents / total_leads) * 100) : 0;
    const conversion_rate = total_leads > 0 ? Math.round((converted / total_leads) * 100) : 0;
    
    return {
      funnel: {
        total_leads,
        engaged_leads,
        hot_leads,
        booking_intents,
        converted,
      },
      rates: {
        engagement_rate,
        hot_lead_rate,
        intent_rate,
        conversion_rate,
      },
    };
  } catch (error) {
    console.error('Error getting conversion funnel:', error);
    return {
      funnel: { total_leads: 0, engaged_leads: 0, hot_leads: 0, booking_intents: 0, converted: 0 },
      rates: { engagement_rate: 0, hot_lead_rate: 0, intent_rate: 0, conversion_rate: 0 },
    };
  }
}

// Get top surgeries
export async function getTopSurgeries(limit: number = 10): Promise<{ surgery: string; inquiry_count: number }[]> {
  try {
    const client = await pool.connect();
    const result = await client.query(`
      SELECT 
        UNNEST(surgeries_interested) as surgery,
        COUNT(*) as inquiry_count
      FROM marketing_leads
      WHERE ARRAY_LENGTH(surgeries_interested, 1) > 0
      GROUP BY surgery
      ORDER BY inquiry_count DESC
      LIMIT $1;
    `, [limit]);
    client.release();
    return result.rows;
  } catch (error) {
    console.error('Error getting top surgeries:', error);
    return [];
  }
}

// Get recent hot leads
export async function getRecentHotLeads(limit: number = 10): Promise<Lead[]> {
  try {
    const client = await pool.connect();
    const result = await client.query(`
      SELECT 
        user_id,
        lead_score,
        last_interaction,
        surgeries_interested,
        booking_intent_detected
      FROM marketing_leads
      WHERE lead_status = 'hot'
      ORDER BY last_interaction DESC
      LIMIT $1;
    `, [limit]);
    client.release();
    return result.rows;
  } catch (error) {
    console.error('Error getting hot leads:', error);
    return [];
  }
}

// Get AI configuration
export async function getAIConfig(): Promise<any> {
  try {
    const client = await pool.connect();
    const result = await client.query('SELECT * FROM ai_config ORDER BY updated_at DESC LIMIT 1;');
    client.release();
    return result.rows[0] || null;
  } catch (error) {
    console.error('Error getting AI config:', error);
    return null;
  }
}

// Update AI configuration
export async function updateAIConfig(config: {
  system_prompt?: string;
  doctors?: any;
  surgeries?: any;
  scoring_weights?: any;
  platform_settings?: any;
}): Promise<boolean> {
  try {
    const client = await pool.connect();
    await client.query(`
      INSERT INTO ai_config (system_prompt, doctors, surgeries, scoring_weights, platform_settings, updated_at)
      VALUES ($1, $2, $3, $4, $5, NOW())
      ON CONFLICT (id) DO UPDATE SET
        system_prompt = EXCLUDED.system_prompt,
        doctors = EXCLUDED.doctors,
        surgeries = EXCLUDED.surgeries,
        scoring_weights = EXCLUDED.scoring_weights,
        platform_settings = EXCLUDED.platform_settings,
        updated_at = NOW();
    `, [
      config.system_prompt,
      JSON.stringify(config.doctors),
      JSON.stringify(config.surgeries),
      JSON.stringify(config.scoring_weights),
      JSON.stringify(config.platform_settings),
    ]);
    client.release();
    return true;
  } catch (error) {
    console.error('Error updating AI config:', error);
    return false;
  }
}

// Initialize AI config table
export async function initAIConfigTable(): Promise<void> {
  try {
    const client = await pool.connect();
    await client.query(`
      CREATE TABLE IF NOT EXISTS ai_config (
        id SERIAL PRIMARY KEY,
        system_prompt TEXT,
        doctors JSONB,
        surgeries JSONB,
        scoring_weights JSONB,
        platform_settings JSONB,
        updated_at TIMESTAMP DEFAULT NOW()
      );
    `);
    client.release();
    console.log('AI config table initialized');
  } catch (error) {
    console.error('Error initializing AI config table:', error);
  }
}

export { pool };