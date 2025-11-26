import { drizzle } from 'drizzle-orm/vercel-postgres';
import { sql } from '@vercel/postgres';
import * as schema from './schema';

// Create the database instance
export const db = drizzle(sql, { schema });

// Export all schema for convenience
export * from './schema';


