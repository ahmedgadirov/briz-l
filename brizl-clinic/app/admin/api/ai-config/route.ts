import { NextRequest, NextResponse } from 'next/server';
import { getAIConfig, updateAIConfig, initAIConfigTable } from '@/lib/admin-db';

// Initialize table on first request
let initialized = false;

export async function GET() {
  try {
    if (!initialized) {
      await initAIConfigTable();
      initialized = true;
    }
    
    const config = await getAIConfig();
    return NextResponse.json(config);
  } catch (error) {
    console.error('Error fetching AI config:', error);
    return NextResponse.json({ error: 'Failed to fetch AI config' }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    if (!initialized) {
      await initAIConfigTable();
      initialized = true;
    }
    
    const body = await request.json();
    const success = await updateAIConfig(body);
    
    if (success) {
      return NextResponse.json({ success: true, message: 'Configuration saved' });
    } else {
      return NextResponse.json({ error: 'Failed to save configuration' }, { status: 500 });
    }
  } catch (error) {
    console.error('Error saving AI config:', error);
    return NextResponse.json({ error: 'Failed to save configuration' }, { status: 500 });
  }
}