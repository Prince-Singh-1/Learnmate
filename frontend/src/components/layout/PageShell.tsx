/**
 * PageShell — Main layout wrapper with sidebar + topbar + content area.
 */

import type { ReactNode } from "react";
import { Sidebar } from "./Sidebar";
import { TopBar } from "./TopBar";

interface PageShellProps {
  activePage: string;
  onNavigate: (page: string) => void;
  onOpenAi?: () => void;
  children: ReactNode;
}

export function PageShell({
  activePage,
  onNavigate,
  onOpenAi,
  children,
}: PageShellProps) {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Sidebar activePage={activePage} onNavigate={onNavigate} />
      <main className="ml-[220px] min-h-screen">
        <TopBar onOpenAi={onOpenAi} onNavigate={onNavigate} />
        <div className="p-5 lg:p-7 max-w-[1600px] mx-auto">{children}</div>
      </main>
    </div>
  );
}
