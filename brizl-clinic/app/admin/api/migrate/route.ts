import { NextResponse } from 'next/server';
import { runMigrations, checkDatabaseConnection, getTableStats } from '@/lib/migrations';

export async function GET() {
  try {
    // Check database connection first
    const connectionStatus = await checkDatabaseConnection();
    
    if (!connectionStatus.connected) {
      return NextResponse.json({
        success: false,
        error: 'Database connection failed',
        details: connectionStatus.error
      }, { status: 500 });
    }
    
    // Get current table stats
    const tableStats = await getTableStats();
    
    return NextResponse.json({
      success: true,
      message: 'Database connection successful',
      tables: tableStats
    });
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: 'Failed to check database status',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}

export async function POST() {
  try {
    // Run migrations
    const result = await runMigrations();
    
    if (result.success) {
      // Get updated table stats
      const tableStats = await getTableStats();
      
      return NextResponse.json({
        success: true,
        message: result.message,
        tables_created: result.tables,
        table_stats: tableStats
      });
    } else {
      return NextResponse.json({
        success: false,
        error: result.message
      }, { status: 500 });
    }
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: 'Migration failed',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}