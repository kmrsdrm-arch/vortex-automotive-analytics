import { getRegionalPerformance } from "@/lib/actions/analytics";
import { RegionalPerformanceChartClient } from "./charts-client";

export async function RegionalPerformanceChart() {
  const regional = await getRegionalPerformance(30);

  const chartData = regional.map(r => ({
    name: r.region,
    value: r.revenue,
  }));

  return <RegionalPerformanceChartClient data={chartData} />;
}
