import { sql } from "@vercel/postgres";

async function migrate() {
  console.log("🔄 Running database migrations...");

  try {
    // Create vehicles table
    await sql`
      CREATE TABLE IF NOT EXISTS vehicles (
        id SERIAL PRIMARY KEY,
        vin VARCHAR(17) UNIQUE NOT NULL,
        make VARCHAR(50) NOT NULL,
        model VARCHAR(50) NOT NULL,
        year INTEGER NOT NULL,
        category VARCHAR(50) NOT NULL,
        msrp DECIMAL(12, 2) NOT NULL,
        specifications JSONB,
        created_at TIMESTAMP DEFAULT NOW() NOT NULL
      )
    `;
    console.log("✓ Created vehicles table");

    // Create sales table
    await sql`
      CREATE TABLE IF NOT EXISTS sales (
        id SERIAL PRIMARY KEY,
        vehicle_id INTEGER REFERENCES vehicles(id) NOT NULL,
        sale_date TIMESTAMP NOT NULL,
        quantity INTEGER DEFAULT 1 NOT NULL,
        total_amount DECIMAL(12, 2) NOT NULL,
        customer_segment VARCHAR(50),
        region VARCHAR(50) NOT NULL,
        dealer_name VARCHAR(100),
        created_at TIMESTAMP DEFAULT NOW() NOT NULL
      )
    `;
    console.log("✓ Created sales table");

    // Create inventory table
    await sql`
      CREATE TABLE IF NOT EXISTS inventory (
        id SERIAL PRIMARY KEY,
        vehicle_id INTEGER REFERENCES vehicles(id) NOT NULL,
        warehouse VARCHAR(100) NOT NULL,
        region VARCHAR(50) NOT NULL,
        quantity_available INTEGER DEFAULT 0 NOT NULL,
        status VARCHAR(20) DEFAULT 'in_stock' NOT NULL,
        last_updated TIMESTAMP DEFAULT NOW() NOT NULL
      )
    `;
    console.log("✓ Created inventory table");

    // Create indexes
    await sql`CREATE INDEX IF NOT EXISTS idx_vin ON vehicles(vin)`;
    await sql`CREATE INDEX IF NOT EXISTS idx_category ON vehicles(category)`;
    await sql`CREATE INDEX IF NOT EXISTS idx_sale_date ON sales(sale_date)`;
    await sql`CREATE INDEX IF NOT EXISTS idx_region ON sales(region)`;
    await sql`CREATE INDEX IF NOT EXISTS idx_sale_vehicle ON sales(vehicle_id)`;
    await sql`CREATE INDEX IF NOT EXISTS idx_inv_vehicle ON inventory(vehicle_id)`;
    await sql`CREATE INDEX IF NOT EXISTS idx_status ON inventory(status)`;
    await sql`CREATE INDEX IF NOT EXISTS idx_inv_region ON inventory(region)`;
    console.log("✓ Created indexes");

    // Create analytics_snapshot table
    await sql`
      CREATE TABLE IF NOT EXISTS analytics_snapshot (
        id SERIAL PRIMARY KEY,
        snapshot_date TIMESTAMP NOT NULL,
        metric_type VARCHAR(50) NOT NULL,
        metric_data JSONB NOT NULL,
        created_at TIMESTAMP DEFAULT NOW() NOT NULL
      )
    `;
    console.log("✓ Created analytics_snapshot table");

    // Create insights_history table
    await sql`
      CREATE TABLE IF NOT EXISTS insights_history (
        id SERIAL PRIMARY KEY,
        insight_type VARCHAR(50) NOT NULL,
        title VARCHAR(200) NOT NULL,
        description TEXT NOT NULL,
        confidence DECIMAL(5, 2),
        context JSONB,
        generated_at TIMESTAMP DEFAULT NOW() NOT NULL
      )
    `;
    console.log("✓ Created insights_history table");

    // Create query_history table
    await sql`
      CREATE TABLE IF NOT EXISTS query_history (
        id SERIAL PRIMARY KEY,
        user_query TEXT NOT NULL,
        generated_sql TEXT,
        query_results JSONB,
        execution_time INTEGER,
        created_at TIMESTAMP DEFAULT NOW() NOT NULL
      )
    `;
    console.log("✓ Created query_history table");

    console.log("✅ Database migration completed successfully!");
  } catch (error) {
    console.error("❌ Error running migrations:", error);
    throw error;
  }
}

migrate()
  .catch((error) => {
    console.error("Migration failed:", error);
    process.exit(1);
  });

