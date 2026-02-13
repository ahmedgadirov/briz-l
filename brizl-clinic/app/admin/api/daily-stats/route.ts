import { NextRequest, NextResponse } from 'next/server';
import { getDailyStats } from '@/lib/admin-db';

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const days = parseInt(searchParams.get('days') || '7');

    const stats = await getDailyStats(days);
    return NextResponse.json(stats);
  } catch (error) {
    console.error('Error fetching daily stats:', error);
    return NextResponse.json({ error: 'Failed to fetch daily stats' }, { status: 500 });
  }
}