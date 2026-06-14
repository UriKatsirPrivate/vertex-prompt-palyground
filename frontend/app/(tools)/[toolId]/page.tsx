import { ToolPage } from "@/components/tools/tool-page";
import { GENERIC_TOOL_IDS } from "@/lib/tools";

// Static export must enumerate dynamic segments at build time.
export function generateStaticParams() {
  return GENERIC_TOOL_IDS.map((toolId) => ({ toolId }));
}

export default async function Page({
  params,
}: {
  params: Promise<{ toolId: string }>;
}) {
  const { toolId } = await params;
  return <ToolPage toolId={toolId} />;
}
