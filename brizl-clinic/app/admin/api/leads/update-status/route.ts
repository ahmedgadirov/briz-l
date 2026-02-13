import { NextRequest, NextResponse } from 'next/server';
import { updateLeadStatus } from '@/lib/admin-db';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { userId, status } = body;

    if (!userId || !status) {
      return NextResponse.json({ error: 'Missing userId or status' }, { status: 400 });
    }

    const success = await updateLeadStatus(userId, status);
    
    if (success) {
      return NextResponse.json({ success: true });
    } else {
      return NextResponse.json({ error: 'Failed to update status' }, { status: 500 });
    }
  } catch (error) {
    console.error('Error updating lead status:', error);
    return NextResponse.json({ error: 'Failed to update status' }, { status: 500 });
  }
}