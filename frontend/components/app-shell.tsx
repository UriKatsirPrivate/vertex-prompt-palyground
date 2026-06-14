"use client";

import { Menu, Sparkles } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

import { ModelConfigPanel } from "@/components/config/model-config-panel";
import { SidebarNav } from "@/components/nav/sidebar-nav";
import { ThemeToggle } from "@/components/theme-toggle";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import {
  Sheet,
  SheetContent,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";

function SidebarBody({ onNavigate }: { onNavigate?: () => void }) {
  return (
    <div className="flex h-full flex-col">
      <ScrollArea className="flex-1">
        <SidebarNav onNavigate={onNavigate} />
      </ScrollArea>
      <Separator />
      <ModelConfigPanel />
    </div>
  );
}

export function AppShell({ children }: { children: React.ReactNode }) {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="flex min-h-screen flex-col">
      <header className="bg-background/80 sticky top-0 z-30 flex h-14 items-center gap-3 border-b px-4 backdrop-blur">
        <Sheet open={mobileOpen} onOpenChange={setMobileOpen}>
          <SheetTrigger
            render={
              <Button variant="ghost" size="icon" className="md:hidden">
                <Menu className="size-5" />
              </Button>
            }
          />
          <SheetContent side="left" className="w-80 p-0">
            <SheetTitle className="sr-only">Navigation</SheetTitle>
            <SidebarBody onNavigate={() => setMobileOpen(false)} />
          </SheetContent>
        </Sheet>

        <Link href="/" className="flex items-center gap-2 font-semibold">
          <Sparkles className="size-5" />
          <span>The Prompt Playground</span>
        </Link>
        <div className="ml-auto">
          <ThemeToggle />
        </div>
      </header>

      <div className="flex flex-1">
        <aside className="bg-sidebar hidden w-72 shrink-0 border-r md:block">
          <div className="sticky top-14 h-[calc(100vh-3.5rem)]">
            <SidebarBody />
          </div>
        </aside>
        <main className="min-w-0 flex-1 px-4 py-6 md:px-8">
          <div className="mx-auto max-w-5xl">{children}</div>
        </main>
      </div>
    </div>
  );
}
