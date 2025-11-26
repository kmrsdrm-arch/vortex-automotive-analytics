import { Suspense } from "react";
import { DashboardKPIs } from "@/components/dashboard/kpis";
import { SalesTrendChart } from "@/components/dashboard/sales-trend-chart";
import { TopVehiclesChart } from "@/components/dashboard/top-vehicles-chart";
import { RegionalPerformanceChart } from "@/components/dashboard/regional-performance-chart";
import { CategoryBreakdownChart } from "@/components/dashboard/category-breakdown-chart";
import { InventoryOverview } from "@/components/dashboard/inventory-overview";
import { LoadingCard } from "@/components/loading-card";

export const dynamic = 'force-dynamic';

export default function DashboardPage() {
  return (
    <div className="space-y-8 animate-fade-in">
      {/* Hero Header */}
      <div className="text-center space-y-4 pb-8">
        <h1 className="font-orbitron text-6xl font-black gradient-text tracking-wide">
          Executive Intelligence Platform
        </h1>
        <p className="text-xl text-muted-foreground font-light tracking-wide">
          AI-Powered Automotive Analytics & Strategic Insights
        </p>
      </div>

      {/* KPIs Section */}
      <section>
        <h2 className="font-orbitron text-2xl font-bold text-vortex-cyan mb-6 flex items-center gap-3">
          <span className="text-3xl">⚡</span>
          Key Performance Metrics
        </h2>
        <Suspense fallback={<LoadingCard />}>
          <DashboardKPIs />
        </Suspense>
      </section>

      {/* Charts Grid */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Suspense fallback={<LoadingCard />}>
          <SalesTrendChart />
        </Suspense>
        <Suspense fallback={<LoadingCard />}>
          <TopVehiclesChart />
        </Suspense>
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Suspense fallback={<LoadingCard />}>
          <RegionalPerformanceChart />
        </Suspense>
        <Suspense fallback={<LoadingCard />}>
          <CategoryBreakdownChart />
        </Suspense>
      </section>

      {/* Inventory Section */}
      <section>
        <h2 className="font-orbitron text-2xl font-bold text-vortex-cyan mb-6 flex items-center gap-3">
          <span className="text-3xl">📦</span>
          Inventory Status
        </h2>
        <Suspense fallback={<LoadingCard />}>
          <InventoryOverview />
        </Suspense>
      </section>
    </div>
  );
}


