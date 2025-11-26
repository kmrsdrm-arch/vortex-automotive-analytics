import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { getInventorySummary } from "@/lib/actions/analytics";
import { formatCurrency, formatNumber } from "@/lib/utils";
import { Package, DollarSign, AlertTriangle, AlertCircle, Warehouse } from "lucide-react";

export const dynamic = 'force-dynamic';

export default async function InventoryPage() {
  const inventory = await getInventorySummary();

  const metrics = [
    {
      title: "Total Units",
      value: formatNumber(inventory?.totalUnits || 0),
      icon: Package,
      color: "text-blue-500",
      bgColor: "from-blue-500/20",
      description: "Across all warehouses",
    },
    {
      title: "Total Value",
      value: formatCurrency(inventory?.totalValue || 0),
      icon: DollarSign,
      color: "text-green-500",
      bgColor: "from-green-500/20",
      description: "Based on MSRP",
    },
    {
      title: "Low Stock Items",
      value: formatNumber(inventory?.lowStockCount || 0),
      icon: AlertTriangle,
      color: "text-yellow-500",
      bgColor: "from-yellow-500/20",
      description: "Requires restocking",
    },
    {
      title: "Out of Stock",
      value: formatNumber(inventory?.outOfStockCount || 0),
      icon: AlertCircle,
      color: "text-red-500",
      bgColor: "from-red-500/20",
      description: "Immediate action needed",
    },
  ];

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="text-center space-y-4">
        <h1 className="font-orbitron text-5xl font-black gradient-text">
          Inventory Analytics
        </h1>
        <p className="text-xl text-muted-foreground">
          Real-time inventory tracking and alerts
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {metrics.map((metric, index) => {
          const Icon = metric.icon;

          return (
            <Card key={index} className="group hover:scale-105 transition-transform duration-300">
              <CardContent className="p-6">
                <div className="flex items-start gap-4">
                  <div className={`p-3 rounded-lg bg-gradient-to-br ${metric.bgColor} to-transparent`}>
                    <Icon className={`w-6 h-6 ${metric.color}`} />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-sm font-medium text-muted-foreground mb-1">
                      {metric.title}
                    </h3>
                    <p className="text-3xl font-bold mb-1">
                      {metric.value}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {metric.description}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Stock Status Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-vortex-cyan">
            <Warehouse className="w-6 h-6" />
            Stock Status Overview
          </CardTitle>
          <CardDescription>
            Real-time inventory levels and alerts
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* Stock Level Indicator */}
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Stock Health</span>
                <span className="font-medium">
                  {inventory ? Math.round(((inventory.totalUnits - inventory.lowStockCount - inventory.outOfStockCount) / inventory.totalUnits) * 100) : 0}%
                </span>
              </div>
              <div className="h-3 bg-background rounded-full overflow-hidden">
                <div 
                  className="h-full bg-vortex-gradient"
                  style={{ 
                    width: `${inventory ? Math.round(((inventory.totalUnits - inventory.lowStockCount - inventory.outOfStockCount) / inventory.totalUnits) * 100) : 0}%` 
                  }}
                />
              </div>
            </div>

            {/* Alerts */}
            {inventory && (inventory.lowStockCount > 0 || inventory.outOfStockCount > 0) && (
              <div className="space-y-3 pt-4 border-t border-border">
                <h4 className="font-semibold text-sm">⚠️ Active Alerts</h4>
                {inventory.lowStockCount > 0 && (
                  <div className="flex items-center gap-3 p-3 rounded-lg bg-yellow-500/10 border border-yellow-500/30">
                    <AlertTriangle className="w-5 h-5 text-yellow-500" />
                    <div>
                      <p className="font-medium text-sm">{inventory.lowStockCount} Low Stock Items</p>
                      <p className="text-xs text-muted-foreground">Consider restocking soon</p>
                    </div>
                  </div>
                )}
                {inventory.outOfStockCount > 0 && (
                  <div className="flex items-center gap-3 p-3 rounded-lg bg-red-500/10 border border-red-500/30">
                    <AlertCircle className="w-5 h-5 text-red-500" />
                    <div>
                      <p className="font-medium text-sm">{inventory.outOfStockCount} Out of Stock Items</p>
                      <p className="text-xs text-muted-foreground">Immediate action required</p>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Additional Info */}
      <Card>
        <CardHeader>
          <CardTitle className="text-vortex-cyan">📊 Inventory Insights</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <p className="text-3xl font-bold gradient-text mb-2">
                {inventory ? Math.round(inventory.totalValue / inventory.totalUnits) : 0}
              </p>
              <p className="text-sm text-muted-foreground">Avg Value per Unit</p>
            </div>
            <div>
              <p className="text-3xl font-bold gradient-text mb-2">
                {inventory ? ((inventory.lowStockCount / inventory.totalUnits) * 100).toFixed(1) : 0}%
              </p>
              <p className="text-sm text-muted-foreground">Low Stock Rate</p>
            </div>
            <div>
              <p className="text-3xl font-bold gradient-text mb-2">
                {inventory ? ((inventory.outOfStockCount / inventory.totalUnits) * 100).toFixed(1) : 0}%
              </p>
              <p className="text-sm text-muted-foreground">Out of Stock Rate</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}


