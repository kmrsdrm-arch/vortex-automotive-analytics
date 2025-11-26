import { getInventorySummary } from "@/lib/actions/analytics";
import { Card, CardContent } from "@/components/ui/card";
import { formatCurrency, formatNumber } from "@/lib/utils";
import { Package, DollarSign, AlertTriangle, AlertCircle } from "lucide-react";

export async function InventoryOverview() {
  const inventory = await getInventorySummary();

  if (!inventory) {
    return (
      <Card>
        <CardContent className="py-12 text-center text-muted-foreground">
          Unable to load inventory data.
        </CardContent>
      </Card>
    );
  }

  const metrics = [
    {
      title: "Total Units",
      value: formatNumber(inventory.totalUnits),
      icon: Package,
      color: "text-blue-500",
      bgColor: "from-blue-500/20",
    },
    {
      title: "Total Value",
      value: formatCurrency(inventory.totalValue),
      icon: DollarSign,
      color: "text-green-500",
      bgColor: "from-green-500/20",
    },
    {
      title: "Low Stock Items",
      value: formatNumber(inventory.lowStockCount),
      icon: AlertTriangle,
      color: "text-yellow-500",
      bgColor: "from-yellow-500/20",
    },
    {
      title: "Out of Stock",
      value: formatNumber(inventory.outOfStockCount),
      icon: AlertCircle,
      color: "text-red-500",
      bgColor: "from-red-500/20",
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {metrics.map((metric, index) => {
        const Icon = metric.icon;

        return (
          <Card key={index}>
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className={`p-3 rounded-lg bg-gradient-to-br ${metric.bgColor} to-transparent`}>
                  <Icon className={`w-6 h-6 ${metric.color}`} />
                </div>
                <div>
                  <h3 className="text-sm font-medium text-muted-foreground mb-1">
                    {metric.title}
                  </h3>
                  <p className="text-2xl font-bold">
                    {metric.value}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}


