'use client';

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from "recharts";
import { formatCurrency } from "@/lib/utils";

const COLORS = ["#00d4ff", "#7b2ff7", "#f026ff", "#4ade80", "#facc15", "#fb923c"];

export function SalesTrendChartClient({ data }: { data: any[] }) {
  return (
    <Card className="glass-card hover-glow animate-slide-up">
      <CardHeader>
        <CardTitle className="font-orbitron text-vortex-cyan flex items-center gap-2">
          📈 Sales Trend
        </CardTitle>
        <CardDescription>Daily revenue performance over the last 30 days</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" />
            <XAxis dataKey="date" stroke="#94a3b8" style={{ fontSize: "12px" }} />
            <YAxis stroke="#94a3b8" style={{ fontSize: "12px" }} />
            <Tooltip
              contentStyle={{
                backgroundColor: "rgba(15, 23, 42, 0.9)",
                border: "1px solid #00d4ff40",
                borderRadius: "8px"
              }}
              formatter={(value: number) => [formatCurrency(value), "Revenue"]}
            />
            <Line
              type="monotone"
              dataKey="revenue"
              stroke="#00d4ff"
              strokeWidth={3}
              dot={{ fill: "#00d4ff", r: 4 }}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}

export function TopVehiclesChartClient({ data }: { data: any[] }) {
  return (
    <Card className="glass-card hover-glow animate-slide-up">
      <CardHeader>
        <CardTitle className="font-orbitron text-vortex-cyan flex items-center gap-2">
          🏆 Top Selling Vehicles
        </CardTitle>
        <CardDescription>Best performers by units sold in the last 30 days</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" />
            <XAxis dataKey="name" stroke="#94a3b8" style={{ fontSize: "12px" }} />
            <YAxis stroke="#94a3b8" style={{ fontSize: "12px" }} />
            <Tooltip
              contentStyle={{
                backgroundColor: "rgba(15, 23, 42, 0.9)",
                border: "1px solid #7b2ff740",
                borderRadius: "8px"
              }}
              formatter={(value: number) => [value, "Units"]}
            />
            <Bar dataKey="units" fill="#7b2ff7" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}

export function RegionalPerformanceChartClient({ data }: { data: any[] }) {
  return (
    <Card className="glass-card hover-glow animate-slide-up">
      <CardHeader>
        <CardTitle className="font-orbitron text-vortex-cyan flex items-center gap-2">
          🌍 Regional Performance
        </CardTitle>
        <CardDescription>Revenue distribution across regions</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={(entry) => `${entry.name}: ${formatCurrency(entry.value)}`}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                backgroundColor: "rgba(15, 23, 42, 0.9)",
                border: "1px solid #00d4ff40",
                borderRadius: "8px"
              }}
              formatter={(value: number) => [formatCurrency(value), "Revenue"]}
            />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}

export function CategoryBreakdownChartClient({ data }: { data: any[] }) {
  return (
    <Card className="glass-card hover-glow animate-slide-up">
      <CardHeader>
        <CardTitle className="font-orbitron text-vortex-cyan flex items-center gap-2">
          📊 Category Breakdown
        </CardTitle>
        <CardDescription>Sales distribution by vehicle category</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={(entry) => `${entry.name}: ${entry.value} units`}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                backgroundColor: "rgba(15, 23, 42, 0.9)",
                border: "1px solid #f026ff40",
                borderRadius: "8px"
              }}
            />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}

