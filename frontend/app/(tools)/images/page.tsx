"use client";

import { Download, ImageIcon, Sparkles } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

import { ErrorState } from "@/components/tools/error-state";
import { LoadingState } from "@/components/tools/loading-state";
import { ResultList } from "@/components/tools/result-list";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ApiError, callImageGenerate, callImagePrompts } from "@/lib/api";
import type { ImageOut } from "@/lib/types";
import { useConfigStore } from "@/store/config-store";

const COUNT = 2;
const PLACEHOLDER = "A photo of a chocolate bar on a kitchen counter";

export default function ImagesPage() {
  const [description, setDescription] = useState("");
  const [prompts, setPrompts] = useState<string | null>(null);
  const [images, setImages] = useState<ImageOut[] | null>(null);
  const [promptsLoading, setPromptsLoading] = useState(false);
  const [imagesLoading, setImagesLoading] = useState(false);
  const [error, setError] = useState<unknown>(null);
  const asModelConfig = useConfigStore((s) => s.asModelConfig);

  async function genPrompts() {
    if (!description.trim() || promptsLoading) return;
    setPromptsLoading(true);
    setError(null);
    setPrompts(null);
    try {
      const res = await callImagePrompts(description, COUNT, asModelConfig());
      setPrompts(res.prompts);
    } catch (err) {
      setError(err);
      toast.error(err instanceof ApiError ? err.message : "Request failed");
    } finally {
      setPromptsLoading(false);
    }
  }

  async function genImages() {
    if (!description.trim() || imagesLoading) return;
    setImagesLoading(true);
    setError(null);
    setImages(null);
    try {
      const res = await callImageGenerate(description, COUNT);
      setImages(res.images);
    } catch (err) {
      setError(err);
      toast.error(err instanceof ApiError ? err.message : "Request failed");
    } finally {
      setImagesLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Images</h1>
        <p className="text-muted-foreground mt-1 text-sm">
          Generate Imagen prompts, then render images.{" "}
          <a
            href="https://cloud.google.com/vertex-ai/docs/generative-ai/image/img-gen-prompt-guide"
            target="_blank"
            rel="noopener noreferrer"
            className="underline"
          >
            Prompt guide
          </a>
        </p>
      </div>

      <Textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder={PLACEHOLDER}
        className="min-h-32"
      />
      <div className="flex flex-wrap gap-2">
        <Button onClick={genPrompts} disabled={promptsLoading || !description.trim()} variant="outline">
          <Sparkles className="size-4" />
          {promptsLoading ? "Generating…" : "Generate Prompt(s)"}
        </Button>
        <Button onClick={genImages} disabled={imagesLoading || !description.trim()}>
          <ImageIcon className="size-4" />
          {imagesLoading ? "Generating…" : "Generate Image(s)"}
        </Button>
      </div>

      {error != null && !promptsLoading && !imagesLoading && <ErrorState error={error} />}

      {promptsLoading && <LoadingState />}
      {!promptsLoading && prompts && (
        <ResultList blocks={[{ title: "Image prompts", content: prompts }]} />
      )}

      {imagesLoading && (
        <div className="grid grid-cols-2 gap-4">
          <LoadingState count={2} />
        </div>
      )}
      {!imagesLoading && images && <ImageGrid images={images} />}
    </div>
  );
}

function ImageGrid({ images }: { images: ImageOut[] }) {
  function download(img: ImageOut, i: number) {
    const a = document.createElement("a");
    a.href = `data:${img.mime_type};base64,${img.data_b64}`;
    a.download = `image-${i + 1}.jpg`;
    a.click();
  }

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
      {images.map((img, i) => (
        <div key={i} className="group relative overflow-hidden rounded-lg border">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={`data:${img.mime_type};base64,${img.data_b64}`}
            alt={`Generated image ${i + 1}`}
            className="h-auto w-full"
          />
          <Button
            size="icon"
            variant="secondary"
            className="absolute top-2 right-2 opacity-0 transition-opacity group-hover:opacity-100"
            onClick={() => download(img, i)}
            aria-label="Download image"
          >
            <Download className="size-4" />
          </Button>
        </div>
      ))}
    </div>
  );
}
