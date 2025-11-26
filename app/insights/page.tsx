"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Lightbulb, Loader2, Sparkles } from "lucide-react";
import { generateInsights } from "@/lib/actions/insights";

export default function InsightsPage() {
  const [loading, setLoading] = useState(false);
  const [insights, setInsights] = useState<any>(null);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const result = await generateInsights(30);
      setInsights(result);
    } catch (error) {
      console.error("Error generating insights:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8 animate-fade-in max-w-5xl mx-auto">
      <div className="text-center space-y-4">
        <h1 className="font-orbitron text-5xl font-black gradient-text">
          AI-Powered Insights
        </h1>
        <p className="text-xl text-muted-foreground">
          Get strategic recommendations powered by GPT-4
        </p>
      </div>

      <Card className="text-center">
        <CardContent className="py-12">
          <Sparkles className="w-16 h-16 mx-auto mb-4 text-vortex-purple" />
          <h2 className="text-2xl font-bold mb-4">Generate Strategic Insights</h2>
          <p className="text-muted-foreground mb-6">
            Our AI will analyze your sales data and provide actionable recommendations
          </p>
          <Button
            onClick={handleGenerate}
            variant="vortex"
            size="lg"
            disabled={loading}
            className="px-12"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Lightbulb className="w-5 h-5 mr-2" />
                Generate Insights
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {insights && (
        <Card>
          <CardHeader>
            <CardTitle className={insights.success ? "text-vortex-cyan" : "text-red-500"}>
              {insights.success ? "📊 Strategic Insights" : "✗ Error"}
            </CardTitle>
            {insights.success && (
              <CardDescription>
                Generated {new Date(insights.generatedAt).toLocaleString()}
              </CardDescription>
            )}
          </CardHeader>
          <CardContent>
            {insights.success ? (
              <div className="prose prose-invert max-w-none">
                <div className="whitespace-pre-wrap text-foreground leading-relaxed">
                  {insights.insights}
                </div>
                {insights.dataPoints && (
                  <div className="mt-6 pt-6 border-t border-border">
                    <p className="text-sm text-muted-foreground">
                      Analysis based on: {insights.dataPoints.trendDays} days of sales data, {insights.dataPoints.regions} regions, {insights.dataPoints.topVehicles} top vehicles
                    </p>
                  </div>
                )}
              </div>
            ) : (
              <p className="text-red-500">{insights.error}</p>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}


