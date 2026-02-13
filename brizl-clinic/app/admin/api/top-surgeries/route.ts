import { NextResponse } from 'next/server';
import { getTopSurgeries } from '@/lib/admin-db';

export async function GET() {
  try {
    const surgeries = await getTopSurgeries(10);
    return NextResponse.json(surgeries);
  } catch (error) {
    console.error('Error fetching top surgeries:', error);
    return NextResponse.json({ error: 'Failed to fetch top surgeries' }, { status: 500 });
  }
}