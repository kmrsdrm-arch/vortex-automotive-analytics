import { getSalesTrends } from "@/lib/actions/analytics";
import { SalesTrendChartClient } from "./charts-client";

export async function SalesTrendChart() {
  const trends = await getSalesTrends(30);

  const chartData = trends.map(t => ({
    date: new Date(t.date).toLocaleDateString("en-US", { month: "short", day: "numeric" }),
    revenue: t.revenue,
  }));

  return <SalesTrendChartClient data={chartData} />;
}
