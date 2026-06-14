"use client";

import { useAppConfig } from "@/components/config/app-config-provider";
import { GenericToolForm } from "@/components/tools/generic-tool-form";
import { Skeleton } from "@/components/ui/skeleton";

export function ToolPage({ toolId }: { toolId: string }) {
  const { config, loading, error } = useAppConfig();

  if (loading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-44 w-full" />
      </div>
    );
  }

  if (error || !config) {
    return (
      <p className="text-destructive text-sm">
        Failed to load configuration: {error ?? "unknown error"}
      </p>
    );
  }

  const tool = config.tools.find((t) => t.id === toolId);
  if (!tool) {
    return <p className="text-muted-foreground">Unknown tool: {toolId}</p>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">{tool.label}</h1>
        <p className="text-muted-foreground mt-1 text-sm">
          Category: {tool.category}
        </p>
      </div>
      <GenericToolForm tool={tool} />
    </div>
  );
}
