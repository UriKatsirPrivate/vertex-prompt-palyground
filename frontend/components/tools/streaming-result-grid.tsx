"use client";

import { AlertCircle } from "lucide-react";

import { ResultBlock } from "@/components/tools/result-block";
import { Skeleton } from "@/components/ui/skeleton";
import type { ResultBlock as ResultBlockType } from "@/lib/types";

// Renders a fixed grid of `count` slots. Each slot shows a skeleton until its
// block streams in (then the result) or an error card if that block failed.
// Slots are keyed by index so the layout stays stable as results pop in.
export function StreamingResultGrid({
  slots,
  errors,
  count,
}: {
  slots: (ResultBlockType | null)[];
  errors: (string | null)[];
  count: number;
}) {
  const cols = count >= 2 ? "grid-cols-1 lg:grid-cols-2" : "grid-cols-1";

  return (
    <div className={`grid gap-4 ${cols}`}>
      {Array.from({ length: count }).map((_, i) => {
        const block = slots[i];
        if (block) return <ResultBlock key={i} block={block} />;

        const err = errors[i];
        if (err) {
          return (
            <div
              key={i}
              className="text-destructive flex items-start gap-2 rounded-lg border p-4 text-sm"
            >
              <AlertCircle className="mt-0.5 size-4 shrink-0" />
              <span>{err}</span>
            </div>
          );
        }

        return (
          <div key={i} className="space-y-2 rounded-lg border p-4">
            <Skeleton className="h-4 w-24" />
            <Skeleton className="h-3 w-full" />
            <Skeleton className="h-3 w-5/6" />
            <Skeleton className="h-3 w-4/6" />
          </div>
        );
      })}
    </div>
  );
}
