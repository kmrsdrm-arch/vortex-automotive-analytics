import { getTopVehicles } from "@/lib/actions/analytics";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { formatCurrency } from "@/lib/utils";

export async function TopVehiclesChart() {
  const topVehicles = await getTopVehicles(5, 30);

  const chartData = topVehicles.map(v => ({
    name: v.name,
    amount: v.totalAmount,
  }));

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-vortex-cyan">
          🏆 Top Selling Vehicles
        </CardTitle>
        <CardDescription>Top 5 vehicles by revenue (last 30 days)</CardDescription>
      </CardHeader>
      <CardContent>
        {chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <defs>
                <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#7b2ff7" stopOpacity={1}/>
                  <stop offset="100%" stopColor="#f026ff" stopOpacity={1}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#2a3342" />
              <XAxis 
                dataKey="name" 
                stroke="#64748b"
                style={{ fontSize: "11px" }}
                angle={-15}
                textAnchor="end"
                height={80}
              />
              <YAxis 
                stroke="#64748b"
                style={{ fontSize: "12px" }}
                tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "rgba(17, 24, 39, 0.95)",
                  border: "1px solid #2a3342",
                  borderRadius: "8px",
                }}
                formatter={(value: number) => [formatCurrency(value), "Revenue"]}
              />
              <Bar 
                dataKey="amount" 
                fill="url(#barGradient)"
                radius={[8, 8, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <div className="h-[300px] flex items-center justify-center text-muted-foreground">
            No vehicle data available
          </div>
        )}
      </CardContent>
    </Card>
  );
}


