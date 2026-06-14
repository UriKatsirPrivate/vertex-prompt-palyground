import { AlertTriangle } from "lucide-react";

import { ApiError } from "@/lib/api";

export function ErrorState({ error }: { error: unknown }) {
  const isApi = error instanceof ApiError;
  const message = error instanceof Error ? error.message : "Something went wrong.";
  const hint =
    isApi && error.code === "safety_blocked"
      ? "Try rephrasing your prompt — it may have triggered the safety filters."
      : isApi && error.code === "network_error"
        ? "Check that the backend API is running."
        : null;

  return (
    <div className="border-destructive/40 bg-destructive/5 text-destructive flex items-start gap-3 rounded-lg border p-4 text-sm">
      <AlertTriangle className="mt-0.5 size-4 shrink-0" />
      <div className="space-y-1">
        <p className="font-medium">{message}</p>
        {hint && <p className="text-destructive/80">{hint}</p>}
      </div>
    </div>
  );
}
