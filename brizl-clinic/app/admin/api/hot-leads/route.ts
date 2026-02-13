import { NextResponse } from 'next/server';
import { getRecentHotLeads } from '@/lib/admin-db';

export async function GET() {
  try {
    const leads = await getRecentHotLeads(10);
    return NextResponse.json(leads);
  } catch (error) {
    console.error('Error fetching hot leads:', error);
    return NextResponse.json({ error: 'Failed to fetch hot leads' }, { status: 500 });
  }
}