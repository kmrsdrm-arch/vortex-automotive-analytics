import { pgTable, serial, varchar, decimal, integer, timestamp, text, jsonb, index } from 'drizzle-orm/pg-core';

// Vehicles Table
export const vehicles = pgTable('vehicles', {
  id: serial('id').primaryKey(),
  vin: varchar('vin', { length: 17 }).unique().notNull(),
  make: varchar('make', { length: 50 }).notNull(),
  model: varchar('model', { length: 50 }).notNull(),
  year: integer('year').notNull(),
  category: varchar('category', { length: 50 }).notNull(), // Sedan, SUV, Truck, etc.
  msrp: decimal('msrp', { precision: 12, scale: 2 }).notNull(),
  specifications: jsonb('specifications'),
  createdAt: timestamp('created_at').defaultNow().notNull(),
}, (table) => ({
  vinIdx: index('vin_idx').on(table.vin),
  categoryIdx: index('category_idx').on(table.category),
}));

// Sales Table
export const sales = pgTable('sales', {
  id: serial('id').primaryKey(),
  vehicleId: integer('vehicle_id').references(() => vehicles.id).notNull(),
  saleDate: timestamp('sale_date').notNull(),
  quantity: integer('quantity').default(1).notNull(),
  totalAmount: decimal('total_amount', { precision: 12, scale: 2 }).notNull(),
  customerSegment: varchar('customer_segment', { length: 50 }), // Individual, Fleet, Corporate
  region: varchar('region', { length: 50 }).notNull(), // North, South, East, West
  dealerName: varchar('dealer_name', { length: 100 }),
  createdAt: timestamp('created_at').defaultNow().notNull(),
}, (table) => ({
  saleDateIdx: index('sale_date_idx').on(table.saleDate),
  regionIdx: index('region_idx').on(table.region),
  vehicleIdx: index('sale_vehicle_idx').on(table.vehicleId),
}));

// Inventory Table
export const inventory = pgTable('inventory', {
  id: serial('id').primaryKey(),
  vehicleId: integer('vehicle_id').references(() => vehicles.id).notNull(),
  warehouse: varchar('warehouse', { length: 100 }).notNull(),
  region: varchar('region', { length: 50 }).notNull(),
  quantityAvailable: integer('quantity_available').default(0).notNull(),
  status: varchar('status', { length: 20 }).default('in_stock').notNull(), // in_stock, low_stock, out_of_stock
  lastUpdated: timestamp('last_updated').defaultNow().notNull(),
}, (table) => ({
  vehicleIdx: index('inv_vehicle_idx').on(table.vehicleId),
  statusIdx: index('status_idx').on(table.status),
  regionIdx: index('inv_region_idx').on(table.region),
}));

// Analytics Snapshot Table (for caching)
export const analyticsSnapshot = pgTable('analytics_snapshot', {
  id: serial('id').primaryKey(),
  snapshotDate: timestamp('snapshot_date').notNull(),
  metricType: varchar('metric_type', { length: 50 }).notNull(), // daily_sales, monthly_revenue, etc.
  metricData: jsonb('metric_data').notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
}, (table) => ({
  dateIdx: index('snapshot_date_idx').on(table.snapshotDate),
  typeIdx: index('metric_type_idx').on(table.metricType),
}));

// Insights History Table
export const insightsHistory = pgTable('insights_history', {
  id: serial('id').primaryKey(),
  insightType: varchar('insight_type', { length: 50 }).notNull(), // trend, anomaly, recommendation
  title: varchar('title', { length: 200 }).notNull(),
  description: text('description').notNull(),
  confidence: decimal('confidence', { precision: 5, scale: 2 }), // 0-100
  context: jsonb('context'),
  generatedAt: timestamp('generated_at').defaultNow().notNull(),
}, (table) => ({
  typeIdx: index('insight_type_idx').on(table.insightType),
  dateIdx: index('insight_date_idx').on(table.generatedAt),
}));

// Query History Table
export const queryHistory = pgTable('query_history', {
  id: serial('id').primaryKey(),
  userQuery: text('user_query').notNull(),
  generatedSql: text('generated_sql'),
  queryResults: jsonb('query_results'),
  executionTime: integer('execution_time'), // in milliseconds
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

// Types
export type Vehicle = typeof vehicles.$inferSelect;
export type NewVehicle = typeof vehicles.$inferInsert;
export type Sale = typeof sales.$inferSelect;
export type NewSale = typeof sales.$inferInsert;
export type Inventory = typeof inventory.$inferSelect;
export type NewInventory = typeof inventory.$inferInsert;
export type InsightHistory = typeof insightsHistory.$inferSelect;
export type QueryHistory = typeof queryHistory.$inferSelect;


