"use server";

import { openai, DEFAULT_MODEL } from "@/lib/ai/openai";
import { db } from "@/lib/db";
import { sql } from "drizzle-orm";

const SYSTEM_PROMPT = `You are a SQL query generator for an automotive analytics database.

Database Schema:
- vehicles: id, vin, make, model, year, category, msrp, specifications, created_at
- sales: id, vehicle_id, sale_date, quantity, total_amount, customer_segment, region, dealer_name, created_at
- inventory: id, vehicle_id, warehouse, region, quantity_available, status, last_updated

Generate ONLY the SELECT query. Do not include any explanations or markdown.
Use PostgreSQL syntax. Return ONLY raw SQL.

Examples:
User: "What were total sales last month?"
SQL: SELECT SUM(total_amount) as total FROM sales WHERE sale_date >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month') AND sale_date < DATE_TRUNC('month', CURRENT_DATE)

User: "Top 5 selling vehicles"
SQL: SELECT v.make, v.model, SUM(s.total_amount) as revenue FROM sales s JOIN vehicles v ON s.vehicle_id = v.id GROUP BY v.make, v.model ORDER BY revenue DESC LIMIT 5`;

export async function generateSQLFromNL(userQuery: string) {
  try {
    const completion = await openai.chat.completions.create({
      model: DEFAULT_MODEL,
      messages: [
        { role: "system", content: SYSTEM_PROMPT },
        { role: "user", content: userQuery },
      ],
      temperature: 0.1,
      max_tokens: 500,
    });

    const generatedSQL = completion.choices[0]?.message?.content?.trim() || "";
    
    // Clean up the SQL (remove markdown code blocks if present)
    let cleanSQL = generatedSQL
      .replace(/```sql/gi, "")
      .replace(/```/g, "")
      .trim();

    return cleanSQL;
  } catch (error) {
    console.error("Error generating SQL:", error);
    throw new Error("Failed to generate SQL query");
  }
}

export async function executeNLQuery(userQuery: string) {
  try {
    const generatedSQL = await generateSQLFromNL(userQuery);
    
    // Execute the query
    const startTime = Date.now();
    const result = await db.execute(sql.raw(generatedSQL));
    const executionTime = Date.now() - startTime;

    return {
      success: true,
      query: generatedSQL,
      results: result.rows,
      executionTime,
      userQuery,
    };
  } catch (error: any) {
    console.error("Error executing NL query:", error);
    return {
      success: false,
      query: "",
      results: [],
      executionTime: 0,
      error: error.message || "Failed to execute query",
      userQuery,
    };
  }
}


