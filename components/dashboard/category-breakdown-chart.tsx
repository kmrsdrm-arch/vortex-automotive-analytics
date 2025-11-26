import { getCategoryBreakdown } from "@/lib/actions/analytics";
import { CategoryBreakdownChartClient } from "./charts-client";

export async function CategoryBreakdownChart() {
  const categories = await getCategoryBreakdown(30);

  const chartData = categories.map(c => ({
    name: c.category,
    value: c.units,
  }));

  return <CategoryBreakdownChartClient data={chartData} />;
}
