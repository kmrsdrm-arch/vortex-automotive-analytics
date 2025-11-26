"use server";

import { db, sales, vehicles, inventory } from "@/lib/db";
import { sql, desc, eq, and, gte, lte } from "drizzle-orm";
import { getDateRange } from "@/lib/utils";

export async function getKPIs(days: number = 30) {
  try {
    const { startDate, endDate } = getDateRange(days);

    // Total Revenue
    const revenueResult = await db
      .select({
        total: sql<number>`COALESCE(SUM(${sales.totalAmount}), 0)`,
      })
      .from(sales)
      .where(
        and(
          gte(sales.saleDate, startDate),
          lte(sales.saleDate, endDate)
        )
      );

    // Units Sold
    const unitsResult = await db
      .select({
        total: sql<number>`COALESCE(SUM(${sales.quantity}), 0)`,
      })
      .from(sales)
      .where(
        and(
          gte(sales.saleDate, startDate),
          lte(sales.saleDate, endDate)
        )
      );

    // Average Deal Size
    const avgDealResult = await db
      .select({
        avg: sql<number>`COALESCE(AVG(${sales.totalAmount}), 0)`,
      })
      .from(sales)
      .where(
        and(
          gte(sales.saleDate, startDate),
          lte(sales.saleDate, endDate)
        )
      );

    // Conversion Rate (mock for now - would need actual lead data)
    const conversionRate = 24.5;

    // Previous period for comparison
    const prevStartDate = new Date(startDate);
    prevStartDate.setDate(prevStartDate.getDate() - days);
    
    const prevRevenueResult = await db
      .select({
        total: sql<number>`COALESCE(SUM(${sales.totalAmount}), 0)`,
      })
      .from(sales)
      .where(
        and(
          gte(sales.saleDate, prevStartDate),
          lte(sales.saleDate, startDate)
        )
      );

    const currentRevenue = Number(revenueResult[0]?.total || 0);
    const prevRevenue = Number(prevRevenueResult[0]?.total || 0);
    const revenueChange = prevRevenue > 0 
      ? ((currentRevenue - prevRevenue) / prevRevenue) * 100 
      : 0;

    return {
      totalRevenue: currentRevenue,
      unitsSold: Number(unitsResult[0]?.total || 0),
      avgDealSize: Number(avgDealResult[0]?.avg || 0),
      conversionRate: conversionRate,
      revenueChange: revenueChange,
    };
  } catch (error) {
    console.error("Error fetching KPIs:", error);
    return null;
  }
}

export async function getSalesTrends(days: number = 30) {
  try {
    const { startDate, endDate } = getDateRange(days);

    const trends = await db
      .select({
        date: sql<string>`DATE(${sales.saleDate})`,
        totalAmount: sql<number>`SUM(${sales.totalAmount})`,
        totalUnits: sql<number>`SUM(${sales.quantity})`,
      })
      .from(sales)
      .where(
        and(
          gte(sales.saleDate, startDate),
          lte(sales.saleDate, endDate)
        )
      )
      .groupBy(sql`DATE(${sales.saleDate})`)
      .orderBy(sql`DATE(${sales.saleDate})`);

    return trends.map(t => ({
      date: t.date,
      amount: Number(t.totalAmount),
      units: Number(t.totalUnits),
    }));
  } catch (error) {
    console.error("Error fetching sales trends:", error);
    return [];
  }
}

export async function getTopVehicles(limit: number = 5, days: number = 30) {
  try {
    const { startDate, endDate } = getDateRange(days);

    const topVehicles = await db
      .select({
        vehicleId: sales.vehicleId,
        make: vehicles.make,
        model: vehicles.model,
        category: vehicles.category,
        totalAmount: sql<number>`SUM(${sales.totalAmount})`,
        totalUnits: sql<number>`SUM(${sales.quantity})`,
      })
      .from(sales)
      .innerJoin(vehicles, eq(sales.vehicleId, vehicles.id))
      .where(
        and(
          gte(sales.saleDate, startDate),
          lte(sales.saleDate, endDate)
        )
      )
      .groupBy(sales.vehicleId, vehicles.make, vehicles.model, vehicles.category)
      .orderBy(desc(sql`SUM(${sales.totalAmount})`))
      .limit(limit);

    return topVehicles.map(v => ({
      vehicleId: v.vehicleId,
      name: `${v.make} ${v.model}`,
      category: v.category,
      totalAmount: Number(v.totalAmount),
      totalUnits: Number(v.totalUnits),
    }));
  } catch (error) {
    console.error("Error fetching top vehicles:", error);
    return [];
  }
}

export async function getRegionalPerformance(days: number = 30) {
  try {
    const { startDate, endDate } = getDateRange(days);

    const regional = await db
      .select({
        region: sales.region,
        totalAmount: sql<number>`SUM(${sales.totalAmount})`,
        totalUnits: sql<number>`SUM(${sales.quantity})`,
      })
      .from(sales)
      .where(
        and(
          gte(sales.saleDate, startDate),
          lte(sales.saleDate, endDate)
        )
      )
      .groupBy(sales.region)
      .orderBy(desc(sql`SUM(${sales.totalAmount})`));

    return regional.map(r => ({
      region: r.region,
      amount: Number(r.totalAmount),
      units: Number(r.totalUnits),
    }));
  } catch (error) {
    console.error("Error fetching regional performance:", error);
    return [];
  }
}

export async function getCategoryBreakdown(days: number = 30) {
  try {
    const { startDate, endDate } = getDateRange(days);

    const categories = await db
      .select({
        category: vehicles.category,
        totalAmount: sql<number>`SUM(${sales.totalAmount})`,
        totalUnits: sql<number>`SUM(${sales.quantity})`,
      })
      .from(sales)
      .innerJoin(vehicles, eq(sales.vehicleId, vehicles.id))
      .where(
        and(
          gte(sales.saleDate, startDate),
          lte(sales.saleDate, endDate)
        )
      )
      .groupBy(vehicles.category)
      .orderBy(desc(sql`SUM(${sales.totalAmount})`));

    return categories.map(c => ({
      category: c.category,
      amount: Number(c.totalAmount),
      units: Number(c.totalUnits),
    }));
  } catch (error) {
    console.error("Error fetching category breakdown:", error);
    return [];
  }
}

export async function getInventorySummary() {
  try {
    const summary = await db
      .select({
        totalUnits: sql<number>`SUM(${inventory.quantityAvailable})`,
        totalValue: sql<number>`SUM(${inventory.quantityAvailable} * ${vehicles.msrp})`,
        lowStockCount: sql<number>`COUNT(CASE WHEN ${inventory.status} = 'low_stock' THEN 1 END)`,
        outOfStockCount: sql<number>`COUNT(CASE WHEN ${inventory.status} = 'out_of_stock' THEN 1 END)`,
      })
      .from(inventory)
      .innerJoin(vehicles, eq(inventory.vehicleId, vehicles.id));

    return {
      totalUnits: Number(summary[0]?.totalUnits || 0),
      totalValue: Number(summary[0]?.totalValue || 0),
      lowStockCount: Number(summary[0]?.lowStockCount || 0),
      outOfStockCount: Number(summary[0]?.outOfStockCount || 0),
    };
  } catch (error) {
    console.error("Error fetching inventory summary:", error);
    return null;
  }
}


