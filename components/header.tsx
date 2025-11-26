"use client";

import { useState } from "react";
import { Calendar } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export function Header() {
  const [period, setPeriod] = useState("30");

  return (
    <header className="border-b border-border/50 backdrop-blur-xl bg-card/20">
      <div className="flex items-center justify-between px-8 py-4">
        <div className="flex items-center gap-4">
          <Calendar className="w-5 h-5 text-vortex-cyan" />
          <span className="text-sm font-medium text-muted-foreground">
            Date Range
          </span>
          <Select value={period} onValueChange={setPeriod}>
            <SelectTrigger className="w-[180px] bg-background/50">
              <SelectValue placeholder="Select period" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7">Last 7 days</SelectItem>
              <SelectItem value="14">Last 14 days</SelectItem>
              <SelectItem value="30">Last 30 days</SelectItem>
              <SelectItem value="60">Last 60 days</SelectItem>
              <SelectItem value="90">Last 90 days</SelectItem>
              <SelectItem value="180">Last 180 days</SelectItem>
              <SelectItem value="365">Last 365 days</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="flex items-center gap-3">
          <div className="text-right">
            <p className="text-xs text-muted-foreground">Last Updated</p>
            <p className="text-sm font-medium">
              {new Date().toLocaleString("en-US", {
                month: "short",
                day: "numeric",
                hour: "2-digit",
                minute: "2-digit",
              })}
            </p>
          </div>
          <Button variant="vortex" size="sm">
            Refresh
          </Button>
        </div>
      </div>
    </header>
  );
}


