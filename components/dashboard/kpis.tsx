import { getKPIs } from "@/lib/actions/analytics";
import { Card, CardContent } from "@/components/ui/card";
import { formatCurrency, formatNumber, formatPercentage } from "@/lib/utils";
import { TrendingUp, TrendingDown, DollarSign, ShoppingCart, Target, Percent } from "lucide-react";

export async function DashboardKPIs() {
  const kpis = await getKPIs(30);

  if (!kpis) {
    return (
      <Card>
        <CardContent className="py-12 text-center text-muted-foreground">
          Unable to load KPIs. Please check your database connection.
        </CardContent>
      </Card>
    );
  }

  const metrics = [
    {
      title: "Total Revenue",
      value: formatCurrency(kpis.totalRevenue),
      change: kpis.revenueChange,
      icon: DollarSign,
      color: "text-green-500",
    },
    {
      title: "Units Sold",
      value: formatNumber(kpis.unitsSold),
      change: 8.2,
      icon: ShoppingCart,
      color: "text-blue-500",
    },
    {
      title: "Avg Deal Size",
      value: formatCurrency(kpis.avgDealSize),
      change: 3.1,
      icon: Target,
      color: "text-purple-500",
    },
    {
      title: "Conversion Rate",
      value: `${kpis.conversionRate}%`,
      change: 2.4,
      icon: Percent,
      color: "text-cyan-500",
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {metrics.map((metric, index) => {
        const Icon = metric.icon;
        const isPositive = metric.change >= 0;
        const TrendIcon = isPositive ? TrendingUp : TrendingDown;

        return (
          <Card key={index} className="group hover:scale-105 transition-transform duration-300">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div className={`p-3 rounded-lg bg-gradient-to-br from-${metric.color}/20 to-transparent`}>
                  <Icon className={`w-6 h-6 ${metric.color}`} />
                </div>
                <div className={`flex items-center gap-1 text-sm font-medium ${
                  isPositive ? "text-green-500" : "text-red-500"
                }`}>
                  <TrendIcon className="w-4 h-4" />
                  {formatPercentage(metric.change)}
                </div>
              </div>
              <h3 className="text-sm font-medium text-muted-foreground mb-1">
                {metric.title}
              </h3>
              <p className="text-3xl font-bold gradient-text">
                {metric.value}
              </p>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}


