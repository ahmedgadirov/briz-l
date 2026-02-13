import { NextResponse } from 'next/server';
import { getConversionFunnel } from '@/lib/admin-db';

export async function GET() {
  try {
    const funnel = await getConversionFunnel();
    return NextResponse.json(funnel);
  } catch (error) {
    console.error('Error fetching funnel:', error);
    return NextResponse.json({ error: 'Failed to fetch funnel' }, { status: 500 });
  }
}