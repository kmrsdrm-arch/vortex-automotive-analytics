import { Suspense } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { SalesTrendChart } from "@/components/dashboard/sales-trend-chart";
import { TopVehiclesChart } from "@/components/dashboard/top-vehicles-chart";
import { RegionalPerformanceChart } from "@/components/dashboard/regional-performance-chart";
import { CategoryBreakdownChart } from "@/components/dashboard/category-breakdown-chart";
import { LoadingCard } from "@/components/loading-card";
import { getKPIs } from "@/lib/actions/analytics";
import { formatCurrency, formatNumber, formatPercentage } from "@/lib/utils";
import { TrendingUp, DollarSign, ShoppingCart } from "lucide-react";

export const dynamic = 'force-dynamic';

export default async function SalesPage() {
  const kpis = await getKPIs(30);

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="text-center space-y-4">
        <h1 className="font-orbitron text-5xl font-black gradient-text">
          Sales Analytics
        </h1>
        <p className="text-xl text-muted-foreground">
          Comprehensive sales performance and trends
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-lg bg-gradient-to-br from-green-500/20 to-transparent">
                <DollarSign className="w-6 h-6 text-green-500" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Total Revenue</p>
                <p className="text-2xl font-bold">{formatCurrency(kpis?.totalRevenue || 0)}</p>
                <p className="text-xs text-green-500">{formatPercentage(kpis?.revenueChange || 0)} vs last period</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-lg bg-gradient-to-br from-blue-500/20 to-transparent">
                <ShoppingCart className="w-6 h-6 text-blue-500" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Units Sold</p>
                <p className="text-2xl font-bold">{formatNumber(kpis?.unitsSold || 0)}</p>
                <p className="text-xs text-blue-500">Last 30 days</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-lg bg-gradient-to-br from-purple-500/20 to-transparent">
                <TrendingUp className="w-6 h-6 text-purple-500" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Avg Deal Size</p>
                <p className="text-2xl font-bold">{formatCurrency(kpis?.avgDealSize || 0)}</p>
                <p className="text-xs text-purple-500">Per transaction</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <Suspense fallback={<LoadingCard />}>
        <SalesTrendChart />
      </Suspense>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Suspense fallback={<LoadingCard />}>
          <TopVehiclesChart />
        </Suspense>
        <Suspense fallback={<LoadingCard />}>
          <RegionalPerformanceChart />
        </Suspense>
      </div>

      <Suspense fallback={<LoadingCard />}>
        <CategoryBreakdownChart />
      </Suspense>
    </div>
  );
}


