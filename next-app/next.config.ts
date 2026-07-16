import type { NextConfig } from "next";
import path from "path";
import { config } from "dotenv";

config({ path: path.resolve(__dirname, '..env') })
const nextConfig: NextConfig = {
  output: 'standalone',
  images: {
    remotePatterns: [new URL("https://lh3.googleusercontent.com/**")]
  }
};

export default nextConfig;
