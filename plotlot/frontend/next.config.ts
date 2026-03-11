import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
};

// Only wrap with Sentry when auth token is available (production with Sentry configured)
let config = nextConfig;
if (process.env.SENTRY_AUTH_TOKEN) {
  const { withSentryConfig } = require("@sentry/nextjs");
  config = withSentryConfig(nextConfig, {
    silent: true,
    disableLogger: true,
  });
}

export default config;
