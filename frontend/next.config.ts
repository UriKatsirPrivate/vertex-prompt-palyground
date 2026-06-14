import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Single-container deployment: FastAPI serves this static export from /static.
  output: "export",
  // Static export cannot use the default Image Optimization server.
  images: { unoptimized: true },
};

export default nextConfig;
