"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { MessageSquare, Send, Loader2 } from "lucide-react";
import { executeNLQuery } from "@/lib/actions/nlquery";

export default function QueryPage() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await executeNLQuery(query);
      setResult(response);
    } catch (error: any) {
      setResult({
        success: false,
        error: error.message || "Failed to execute query",
      });
    } finally {
      setLoading(false);
    }
  };

  const exampleQueries = [
    "What were total sales last month?",
    "Show me the top 5 selling vehicles",
    "Which region has the highest revenue?",
    "How many vehicles are low on stock?",
  ];

  return (
    <div className="space-y-8 animate-fade-in max-w-5xl mx-auto">
      <div className="text-center space-y-4">
        <h1 className="font-orbitron text-5xl font-black gradient-text">
          Natural Language Query
        </h1>
        <p className="text-xl text-muted-foreground">
          Ask questions about your data in plain English
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-vortex-cyan">
            <MessageSquare className="w-6 h-6" />
            Ask a Question
          </CardTitle>
          <CardDescription>
            Our AI will convert your question into a SQL query and fetch the results
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="flex gap-2">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g., What were total sales last month?"
                className="flex-1 px-4 py-3 rounded-lg bg-background border border-border focus:border-vortex-purple focus:outline-none focus:ring-2 focus:ring-vortex-purple/20 transition-all"
                disabled={loading}
              />
              <Button
                type="submit"
                variant="vortex"
                size="lg"
                disabled={loading || !query.trim()}
                className="px-8"
              >
                {loading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <>
                    <Send className="w-5 h-5 mr-2" />
                    Ask
                  </>
                )}
              </Button>
            </div>

            <div className="flex flex-wrap gap-2">
              {exampleQueries.map((example, index) => (
                <button
                  key={index}
                  type="button"
                  onClick={() => setQuery(example)}
                  className="text-sm px-3 py-1 rounded-full bg-vortex-purple/10 hover:bg-vortex-purple/20 border border-vortex-purple/30 transition-colors"
                  disabled={loading}
                >
                  {example}
                </button>
              ))}
            </div>
          </form>
        </CardContent>
      </Card>

      {result && (
        <Card>
          <CardHeader>
            <CardTitle className={result.success ? "text-green-500" : "text-red-500"}>
              {result.success ? "✓ Query Results" : "✗ Error"}
            </CardTitle>
            {result.query && (
              <CardDescription className="font-mono text-xs bg-background/50 p-3 rounded">
                {result.query}
              </CardDescription>
            )}
          </CardHeader>
          <CardContent>
            {result.success ? (
              <>
                <p className="text-sm text-muted-foreground mb-4">
                  Found {result.results.length} result(s) in {result.executionTime}ms
                </p>
                {result.results.length > 0 ? (
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b border-border">
                          {Object.keys(result.results[0]).map((key) => (
                            <th key={key} className="text-left p-3 font-semibold">
                              {key}
                            </th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {result.results.map((row: any, i: number) => (
                          <tr key={i} className="border-b border-border/50 hover:bg-background/50">
                            {Object.values(row).map((value: any, j: number) => (
                              <td key={j} className="p-3">
                                {value?.toString() || "-"}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <p className="text-muted-foreground">No results found.</p>
                )}
              </>
            ) : (
              <p className="text-red-500">{result.error}</p>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}


