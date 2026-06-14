"use client";

import { Sparkles } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

import { ErrorState } from "@/components/tools/error-state";
import { LoadingState } from "@/components/tools/loading-state";
import { ResultList } from "@/components/tools/result-list";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import { ApiError, callDare, callDareArtifacts } from "@/lib/api";
import { useConfigStore } from "@/store/config-store";

export default function DarePage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">D.A.R.E Prompting</h1>
        <p className="text-muted-foreground mt-1 text-sm">
          Ground responses in a vision and mission. See{" "}
          <a
            href="https://www.linkedin.com/posts/ram-seshadri-nyc-nj_how-do-you-reduce-hallucinations-ensure-activity-7085123540177285121-THrK/"
            target="_blank"
            rel="noopener noreferrer"
            className="underline"
          >
            the technique
          </a>
          .
        </p>
      </div>

      <Tabs defaultValue="dare">
        <TabsList>
          <TabsTrigger value="dare">D.A.R.E</TabsTrigger>
          <TabsTrigger value="artifacts">Create Artifacts</TabsTrigger>
        </TabsList>
        <TabsContent value="dare" className="pt-4">
          <DareForm />
        </TabsContent>
        <TabsContent value="artifacts" className="pt-4">
          <ArtifactsForm />
        </TabsContent>
      </Tabs>
    </div>
  );
}

function DareForm() {
  const [vision, setVision] = useState("");
  const [mission, setMission] = useState("");
  const [context, setContext] = useState("");
  const [prompt, setPrompt] = useState("");
  const [content, setContent] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<unknown>(null);
  const asModelConfig = useConfigStore((s) => s.asModelConfig);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!prompt.trim() || loading) return;
    setLoading(true);
    setError(null);
    setContent(null);
    try {
      const res = await callDare(
        { vision, mission, context, prompt },
        asModelConfig(),
      );
      setContent(res.content);
    } catch (err) {
      setError(err);
      toast.error(err instanceof ApiError ? err.message : "Request failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={submit} className="space-y-4">
      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="Vision" value={vision} onChange={setVision} placeholder="Marketing assistant" />
        <Field label="Mission" value={mission} onChange={setMission} placeholder="Help people plan marketing events" />
      </div>
      <div className="space-y-1.5">
        <Label>Context</Label>
        <Textarea value={context} onChange={(e) => setContext(e.target.value)} placeholder="You are a marketing assistant. Be as elaborate as makes sense" className="min-h-20" />
      </div>
      <div className="space-y-1.5">
        <Label>Prompt</Label>
        <Textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} placeholder="Plan a Cloud Run marketing workshop" className="min-h-24" />
      </div>
      <Button type="submit" disabled={loading || !prompt.trim()}>
        <Sparkles className="size-4" />
        {loading ? "Generating…" : "D.A.R.E"}
      </Button>

      {loading && <LoadingState />}
      {!loading && error != null && <ErrorState error={error} />}
      {!loading && content && <ResultList blocks={[{ content }]} />}
    </form>
  );
}

function ArtifactsForm() {
  const [input, setInput] = useState("");
  const [content, setContent] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<unknown>(null);
  const asModelConfig = useConfigStore((s) => s.asModelConfig);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim() || loading) return;
    setLoading(true);
    setError(null);
    setContent(null);
    try {
      const res = await callDareArtifacts(input, asModelConfig());
      setContent(res.content);
    } catch (err) {
      setError(err);
      toast.error(err instanceof ApiError ? err.message : "Request failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={submit} className="space-y-4">
      <div className="space-y-1.5">
        <Label>Prompt</Label>
        <Textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="marketing assistant"
          className="min-h-24"
        />
        <p className="text-muted-foreground text-xs">
          Generates the Vision, Mission, and Context artifacts for a D.A.R.E prompt.
        </p>
      </div>
      <Button type="submit" disabled={loading || !input.trim()}>
        <Sparkles className="size-4" />
        {loading ? "Generating…" : "D.A.R.E Artifacts"}
      </Button>

      {loading && <LoadingState />}
      {!loading && error != null && <ErrorState error={error} />}
      {!loading && content && <ResultList blocks={[{ content }]} />}
    </form>
  );
}

function Field({
  label,
  value,
  onChange,
  placeholder,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
}) {
  return (
    <div className="space-y-1.5">
      <Label>{label}</Label>
      <Input value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} />
    </div>
  );
}
