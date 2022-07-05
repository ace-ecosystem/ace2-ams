/// <reference types="vitest" />

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";

// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      "@": resolve(__dirname, "./src"),
      "@unit": resolve(__dirname, "./tests/unit/src"),
      "@mocks": resolve(__dirname, "./tests/mocks"),
      "@tests": resolve(__dirname, "./tests"),
    },
  },
  plugins: [vue()],
  test: {
    globals: false,
    environment: "jsdom",
    include: ["**/unit/**/*.spec.{js,mjs,cjs,ts,mts,cts,jsx,tsx}"],
    reporters: ["verbose"],
    coverage: {
      // 100: true, // Require 100% coverage
    },
  },
  server: {
    host: "0.0.0.0",
    port: 8080,
    proxy: {
      "/api": {
        target: process.env.VITE_BACKEND_URL,
        changeOrigin: true,
        secure: false,
        ws: true,
      },
    },
    watch: {
      usePolling: true,
    },
    hmr: {
      // Internal port
      port: 8080,
      // External port (Docker host)
      clientPort: 8080,
    },
  },
});
