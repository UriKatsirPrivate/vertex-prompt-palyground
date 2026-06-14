"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { GENERIC_TOOL_IDS } from "@/lib/tools";

export default function Home() {
  const router = useRouter();
  useEffect(() => {
    router.replace(`/${GENERIC_TOOL_IDS[0]}`);
  }, [router]);
  return (
    <div className="text-muted-foreground flex min-h-screen items-center justify-center">
      Loading the Prompt Playground…
    </div>
  );
}
