"use client";

import { History, Trash2 } from "lucide-react";
import { useState } from "react";

import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import {
  clearHistory,
  loadHistory,
  type HistoryEntry,
} from "@/lib/history";

export function HistoryDrawer({
  toolId,
  onRestore,
}: {
  toolId: string;
  onRestore: (entry: HistoryEntry) => void;
}) {
  const [open, setOpen] = useState(false);
  const [entries, setEntries] = useState<HistoryEntry[]>([]);

  function refresh() {
    setEntries(loadHistory(toolId));
  }

  return (
    <Sheet
      open={open}
      onOpenChange={(o) => {
        setOpen(o);
        if (o) refresh();
      }}
    >
      <SheetTrigger
        render={
          <Button variant="outline" size="sm">
            <History className="size-4" /> History
          </Button>
        }
      />
      <SheetContent className="flex w-full flex-col gap-0 sm:max-w-md">
        <SheetHeader>
          <SheetTitle>Run history</SheetTitle>
          <SheetDescription>
            Your last runs for this tool, stored locally in this browser.
          </SheetDescription>
        </SheetHeader>

        <ScrollArea className="flex-1 px-4">
          {entries.length === 0 ? (
            <p className="text-muted-foreground py-8 text-center text-sm">
              No history yet.
            </p>
          ) : (
            <ul className="space-y-2 py-2">
              {entries.map((e) => (
                <li key={e.id}>
                  <button
                    onClick={() => {
                      onRestore(e);
                      setOpen(false);
                    }}
                    className="hover:bg-accent w-full rounded-md border p-3 text-left text-sm transition-colors"
                  >
                    <p className="line-clamp-2 font-medium">{e.input}</p>
                    <p className="text-muted-foreground mt-1 text-xs">
                      {new Date(e.ts).toLocaleString()} · {e.modelConfig.model_name}
                    </p>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </ScrollArea>

        {entries.length > 0 && (
          <div className="border-t p-4">
            <Button
              variant="ghost"
              size="sm"
              className="text-muted-foreground w-full"
              onClick={() => {
                clearHistory(toolId);
                refresh();
              }}
            >
              <Trash2 className="size-4" /> Clear history
            </Button>
          </div>
        )}
      </SheetContent>
    </Sheet>
  );
}
