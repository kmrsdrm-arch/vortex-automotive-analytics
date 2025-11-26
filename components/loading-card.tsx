import { Card, CardContent } from "@/components/ui/card";

export function LoadingCard() {
  return (
    <Card className="h-64">
      <CardContent className="h-full flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-16 h-16 border-4 border-vortex-purple border-t-transparent rounded-full animate-spin" />
          <p className="text-sm text-muted-foreground">Loading data...</p>
        </div>
      </CardContent>
    </Card>
  );
}


