import { getTopVehicles } from "@/lib/actions/analytics";
import { TopVehiclesChartClient } from "./charts-client";

export async function TopVehiclesChart() {
  const topVehicles = await getTopVehicles(5, 30);

  const chartData = topVehicles.map(v => ({
    name: v.name,
    units: v.units,
  }));

  return <TopVehiclesChartClient data={chartData} />;
}
