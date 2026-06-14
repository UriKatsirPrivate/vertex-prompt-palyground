"use client";

import { Check, Copy, Download } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import type { ResultBlock as ResultBlockType } from "@/lib/types";

function downloadText(content: string, filename: string) {
  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

export function ResultBlock({ block }: { block: ResultBlockType }) {
  const [copied, setCopied] = useState(false);
  const isJson = block.language === "json";

  async function copy() {
    try {
      await navigator.clipboard.writeText(block.content);
      setCopied(true);
      toast.success("Copied to clipboard");
      setTimeout(() => setCopied(false), 1500);
    } catch {
      toast.error("Copy failed");
    }
  }

  function download() {
    const ext = isJson ? "json" : "txt";
    const base = block.title?.toLowerCase().replace(/\s+/g, "-") || "result";
    downloadText(block.content, `${base}.${ext}`);
  }

  return (
    <Card className="gap-3">
      <CardHeader className="flex flex-row items-center justify-between gap-2 space-y-0">
        <div className="flex items-center gap-2">
          {block.title && (
            <CardTitle className="text-sm font-medium">{block.title}</CardTitle>
          )}
          {block.language && (
            <Badge variant="secondary" className="text-xs">
              {block.language}
            </Badge>
          )}
        </div>
        <div className="flex items-center gap-1">
          <Button
            variant="ghost"
            size="icon"
            className="size-7"
            onClick={copy}
            aria-label="Copy"
          >
            {copied ? <Check className="size-4" /> : <Copy className="size-4" />}
          </Button>
          <Button
            variant="ghost"
            size="icon"
            className="size-7"
            onClick={download}
            aria-label="Download"
          >
            <Download className="size-4" />
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <pre className="bg-muted/50 max-h-[28rem] overflow-auto rounded-md p-3 font-mono text-sm whitespace-pre-wrap">
          {block.content}
        </pre>
      </CardContent>
    </Card>
  );
}
