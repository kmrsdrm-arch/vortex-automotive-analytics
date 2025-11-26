"use server";

import { openai, DEFAULT_MODEL } from "@/lib/ai/openai";
import { getKPIs, getSalesTrends, getTopVehicles, getRegionalPerformance } from "./analytics";

export async function generateInsights(days: number = 30) {
  try {
    // Gather analytics data
    const [kpis, trends, topVehicles, regional] = await Promise.all([
      getKPIs(days),
      getSalesTrends(days),
      getTopVehicles(5, days),
      getRegionalPerformance(days),
    ]);

    // Prepare context for AI
    const context = `
Analyze the following automotive sales data and provide strategic insights:

KPIs (Last ${days} days):
- Total Revenue: $${kpis?.totalRevenue.toLocaleString() || 0}
- Units Sold: ${kpis?.unitsSold.toLocaleString() || 0}
- Average Deal Size: $${kpis?.avgDealSize.toLocaleString() || 0}
- Revenue Change: ${kpis?.revenueChange.toFixed(1)}%

Top Selling Vehicles:
${topVehicles.map((v, i) => `${i + 1}. ${v.name} - $${v.totalAmount.toLocaleString()}`).join('\n')}

Regional Performance:
${regional.map(r => `- ${r.region}: $${r.amount.toLocaleString()}`).join('\n')}

Sales Trend:
${trends.slice(-7).map(t => `${t.date}: $${t.amount.toLocaleString()}`).join('\n')}

Provide 5-7 actionable insights covering:
1. Key trends and patterns
2. Performance anomalies
3. Regional opportunities
4. Product mix recommendations
5. Strategic recommendations
`;

    const completion = await openai.chat.completions.create({
      model: DEFAULT_MODEL,
      messages: [
        {
          role: "system",
          content: "You are an executive automotive analyst. Provide concise, data-driven insights in bullet points. Be specific and actionable.",
        },
        { role: "user", content: context },
      ],
      temperature: 0.7,
      max_tokens: 1000,
    });

    const insights = completion.choices[0]?.message?.content || "Unable to generate insights.";

    return {
      success: true,
      insights,
      generatedAt: new Date().toISOString(),
      dataPoints: {
        kpis,
        topVehicles: topVehicles.length,
        regions: regional.length,
        trendDays: trends.length,
      },
    };
  } catch (error: any) {
    console.error("Error generating insights:", error);
    return {
      success: false,
      insights: "",
      error: error.message || "Failed to generate insights",
      generatedAt: new Date().toISOString(),
    };
  }
}

export async function generateReport(reportType: "executive" | "detailed", days: number = 30) {
  try {
    const [kpis, trends, topVehicles, regional] = await Promise.all([
      getKPIs(days),
      getSalesTrends(days),
      getTopVehicles(10, days),
      getRegionalPerformance(days),
    ]);

    const prompt = reportType === "executive"
      ? `Generate a concise executive summary report (max 500 words) for automotive sales performance over the last ${days} days. Include key metrics, highlights, and recommendations.`
      : `Generate a comprehensive detailed report (max 1500 words) for automotive sales performance over the last ${days} days. Include in-depth analysis, trends, regional breakdown, and strategic recommendations.`;

    const context = `
Data Summary:
- Total Revenue: $${kpis?.totalRevenue.toLocaleString() || 0}
- Units Sold: ${kpis?.unitsSold.toLocaleString() || 0}
- Revenue Growth: ${kpis?.revenueChange.toFixed(1)}%
- Top Vehicle: ${topVehicles[0]?.name || "N/A"}
- Best Region: ${regional[0]?.region || "N/A"}
- Trend: ${trends.length} days of data
`;

    const completion = await openai.chat.completions.create({
      model: DEFAULT_MODEL,
      messages: [
        {
          role: "system",
          content: "You are an executive automotive analyst. Write professional, data-driven reports with clear structure and actionable insights.",
        },
        { role: "user", content: `${prompt}\n\n${context}` },
      ],
      temperature: 0.7,
      max_tokens: reportType === "executive" ? 800 : 2000,
    });

    const report = completion.choices[0]?.message?.content || "Unable to generate report.";

    return {
      success: true,
      report,
      reportType,
      period: `${days} days`,
      generatedAt: new Date().toISOString(),
    };
  } catch (error: any) {
    console.error("Error generating report:", error);
    return {
      success: false,
      report: "",
      error: error.message || "Failed to generate report",
      reportType,
      generatedAt: new Date().toISOString(),
    };
  }
}


