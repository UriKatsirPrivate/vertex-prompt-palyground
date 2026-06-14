"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { useAppConfig } from "@/components/config/app-config-provider";
import { Skeleton } from "@/components/ui/skeleton";
import { CATEGORY_ORDER } from "@/lib/tools";
import type { ToolMeta } from "@/lib/types";
import { cn } from "@/lib/utils";

function groupByCategory(tools: ToolMeta[]): [string, ToolMeta[]][] {
  const groups = new Map<string, ToolMeta[]>();
  for (const t of tools) {
    const list = groups.get(t.category) ?? [];
    list.push(t);
    groups.set(t.category, list);
  }
  const ordered = [...groups.entries()].sort(
    (a, b) => CATEGORY_ORDER.indexOf(a[0]) - CATEGORY_ORDER.indexOf(b[0]),
  );
  return ordered;
}

export function SidebarNav({ onNavigate }: { onNavigate?: () => void }) {
  const { config, loading } = useAppConfig();
  const pathname = usePathname();

  if (loading || !config) {
    return (
      <div className="space-y-2 p-3">
        {Array.from({ length: 8 }).map((_, i) => (
          <Skeleton key={i} className="h-8 w-full" />
        ))}
      </div>
    );
  }

  return (
    <nav className="space-y-5 p-3">
      {groupByCategory(config.tools).map(([category, tools]) => (
        <div key={category}>
          <p className="text-muted-foreground px-2 pb-1 text-xs font-semibold tracking-wide uppercase">
            {category}
          </p>
          <ul className="space-y-0.5">
            {tools.map((tool) => {
              const active = pathname === tool.route;
              return (
                <li key={tool.id}>
                  <Link
                    href={tool.route}
                    onClick={onNavigate}
                    className={cn(
                      "block rounded-md px-2 py-1.5 text-sm transition-colors",
                      active
                        ? "bg-accent text-accent-foreground font-medium"
                        : "text-muted-foreground hover:bg-accent/50 hover:text-foreground",
                    )}
                  >
                    {tool.label}
                  </Link>
                </li>
              );
            })}
          </ul>
        </div>
      ))}
    </nav>
  );
}
