"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard,
  TrendingUp,
  Package,
  MessageSquare,
  Lightbulb,
  FileText,
  Settings,
} from "lucide-react";

const navigation = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Sales Analytics", href: "/sales", icon: TrendingUp },
  { name: "Inventory", href: "/inventory", icon: Package },
  { name: "NL Query", href: "/query", icon: MessageSquare },
  { name: "AI Insights", href: "/insights", icon: Lightbulb },
  { name: "Reports", href: "/reports", icon: FileText },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-72 border-r border-border/50 backdrop-blur-xl bg-card/30 flex flex-col">
      {/* Logo */}
      <div className="p-8 text-center border-b border-border/50">
        <div className="flex justify-center mb-4">
          <VortexLogo />
        </div>
        <h2 className="font-orbitron text-3xl font-black gradient-text tracking-wider">
          VORTEX
        </h2>
        <p className="text-sm text-muted-foreground mt-2 tracking-widest">
          AUTOMOTIVE INTELLIGENCE
        </p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2">
        {navigation.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-4 py-3 rounded-lg transition-all",
                "hover:bg-vortex-purple/10 hover:border-vortex-purple/50",
                isActive
                  ? "bg-vortex-purple/20 border border-vortex-purple/50 text-vortex-cyan font-semibold"
                  : "text-muted-foreground border border-transparent"
              )}
            >
              <item.icon className="w-5 h-5" />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-6 border-t border-border/50 space-y-2">
        <Link
          href="/settings"
          className="flex items-center gap-3 px-4 py-2 rounded-lg text-muted-foreground hover:text-foreground transition-colors"
        >
          <Settings className="w-5 h-5" />
          <span>Settings</span>
        </Link>
        <p className="text-xs text-center text-muted-foreground pt-4">
          ⚡ Vortex v3.0
        </p>
      </div>
    </aside>
  );
}

function VortexLogo() {
  return (
    <svg
      width="60"
      height="60"
      viewBox="0 0 60 60"
      xmlns="http://www.w3.org/2000/svg"
      className="animate-spin-slow drop-shadow-[0_0_15px_rgba(123,47,247,0.5)]"
    >
      <defs>
        <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style={{ stopColor: "#00d4ff", stopOpacity: 1 }} />
          <stop offset="50%" style={{ stopColor: "#7b2ff7", stopOpacity: 1 }} />
          <stop offset="100%" style={{ stopColor: "#f026ff", stopOpacity: 1 }} />
        </linearGradient>
      </defs>
      <circle
        cx="30"
        cy="30"
        r="28"
        fill="none"
        stroke="url(#logoGradient)"
        strokeWidth="2"
        opacity="0.3"
      />
      <circle
        cx="30"
        cy="30"
        r="22"
        fill="none"
        stroke="url(#logoGradient)"
        strokeWidth="2"
        opacity="0.5"
      />
      <circle
        cx="30"
        cy="30"
        r="16"
        fill="none"
        stroke="url(#logoGradient)"
        strokeWidth="2"
        opacity="0.7"
      />
      <path
        d="M 30 14 L 38 30 L 30 46 L 22 30 Z"
        fill="url(#logoGradient)"
        opacity="0.8"
      />
      <circle cx="30" cy="30" r="4" fill="#00d4ff" />
      <circle cx="30" cy="30" r="2" fill="#ffffff" />
    </svg>
  );
}


