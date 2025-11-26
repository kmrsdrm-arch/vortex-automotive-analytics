"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FileText, Loader2, Download } from "lucide-react";
import { generateReport } from "@/lib/actions/insights";

export default function ReportsPage() {
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState<any>(null);

  const handleGenerate = async (type: "executive" | "detailed") => {
    setLoading(true);
    try {
      const result = await generateReport(type, 30);
      setReport(result);
    } catch (error) {
      console.error("Error generating report:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (!report || !report.success) return;

    const blob = new Blob([report.report], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `vortex-report-${report.reportType}-${Date.now()}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-8 animate-fade-in max-w-5xl mx-auto">
      <div className="text-center space-y-4">
        <h1 className="font-orbitron text-5xl font-black gradient-text">
          Report Generation
        </h1>
        <p className="text-xl text-muted-foreground">
          AI-generated reports with comprehensive analysis
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="text-center hover:border-vortex-purple/50 transition-all">
          <CardContent className="py-12">
            <FileText className="w-16 h-16 mx-auto mb-4 text-vortex-cyan" />
            <h2 className="text-2xl font-bold mb-2">Executive Summary</h2>
            <p className="text-muted-foreground mb-6">
              Concise one-page overview with key metrics and recommendations
            </p>
            <Button
              onClick={() => handleGenerate("executive")}
              variant="vortex"
              disabled={loading}
            >
              {loading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                "Generate"
              )}
            </Button>
          </CardContent>
        </Card>

        <Card className="text-center hover:border-vortex-purple/50 transition-all">
          <CardContent className="py-12">
            <FileText className="w-16 h-16 mx-auto mb-4 text-vortex-purple" />
            <h2 className="text-2xl font-bold mb-2">Detailed Report</h2>
            <p className="text-muted-foreground mb-6">
              Comprehensive analysis with in-depth insights and trends
            </p>
            <Button
              onClick={() => handleGenerate("detailed")}
              variant="vortex"
              disabled={loading}
            >
              {loading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                "Generate"
              )}
            </Button>
          </CardContent>
        </Card>
      </div>

      {report && (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className={report.success ? "text-vortex-cyan" : "text-red-500"}>
                  {report.success ? `📄 ${report.reportType === "executive" ? "Executive" : "Detailed"} Report` : "✗ Error"}
                </CardTitle>
                {report.success && (
                  <CardDescription>
                    Generated {new Date(report.generatedAt).toLocaleString()} • Period: {report.period}
                  </CardDescription>
                )}
              </div>
              {report.success && (
                <Button
                  onClick={handleDownload}
                  variant="outline"
                  size="sm"
                >
                  <Download className="w-4 h-4 mr-2" />
                  Download
                </Button>
              )}
            </div>
          </CardHeader>
          <CardContent>
            {report.success ? (
              <div className="prose prose-invert max-w-none">
                <div className="whitespace-pre-wrap text-foreground leading-relaxed">
                  {report.report}
                </div>
              </div>
            ) : (
              <p className="text-red-500">{report.error}</p>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}


