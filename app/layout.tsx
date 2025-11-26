import type { Metadata } from "next";
import { Inter, Orbitron } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";
import { Sidebar } from "@/components/sidebar";
import { Header } from "@/components/header";

const inter = Inter({ 
  subsets: ["latin"],
  variable: "--font-inter",
});

const orbitron = Orbitron({ 
  subsets: ["latin"],
  variable: "--font-orbitron",
});

export const metadata: Metadata = {
  title: "Vortex | Executive Intelligence Platform",
  description: "AI-Powered Automotive Analytics & Strategic Insights",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={cn(
        inter.variable,
        orbitron.variable,
        "font-inter antialiased"
      )}>
        <div className="relative min-h-screen">
          {/* Background Effects */}
          <div className="fixed inset-0 bg-vortex-radial pointer-events-none" />
          <div className="fixed inset-0 bg-[radial-gradient(circle_at_80%_20%,rgba(240,38,255,0.1),transparent_50%)] pointer-events-none" />
          
          {/* Layout */}
          <div className="relative flex min-h-screen">
            <Sidebar />
            <main className="flex-1 flex flex-col">
              <Header />
              <div className="flex-1 p-8">
                {children}
              </div>
            </main>
          </div>
        </div>
      </body>
    </html>
  );
}


