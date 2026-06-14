import { AppConfigProvider } from "@/components/config/app-config-provider";
import { AppShell } from "@/components/app-shell";

export default function ToolsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <AppConfigProvider>
      <AppShell>{children}</AppShell>
    </AppConfigProvider>
  );
}
