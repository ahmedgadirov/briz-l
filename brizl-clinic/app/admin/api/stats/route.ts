import { NextResponse } from 'next/server';
import { getLeadStats } from '@/lib/admin-db';

export async function GET() {
  try {
    const stats = await getLeadStats();
    return NextResponse.json(stats);
  } catch (error) {
    console.error('Error fetching stats:', error);
    return NextResponse.json({ error: 'Failed to fetch stats' }, { status: 500 });
  }
}