import { Skeleton } from "@/components/ui/skeleton";

export function LoadingState({ count = 1 }: { count?: number }) {
  return (
    <div
      className={`grid gap-4 ${count >= 2 ? "grid-cols-1 lg:grid-cols-2" : "grid-cols-1"}`}
    >
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="space-y-2 rounded-lg border p-4">
          <Skeleton className="h-4 w-24" />
          <Skeleton className="h-3 w-full" />
          <Skeleton className="h-3 w-5/6" />
          <Skeleton className="h-3 w-4/6" />
        </div>
      ))}
    </div>
  );
}
