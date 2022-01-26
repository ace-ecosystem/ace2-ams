/// <reference types="vitest" />

import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";

// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      "@": resolve(__dirname, "./src"),
      "@unit": resolve(__dirname, "./tests/unit"),
    },
  },
  plugins: [vue()],
  test: {
    globals: true,
    environment: "happy-dom",
    include: ["**/unit/**/*.spec.{js,mjs,cjs,ts,mts,cts,jsx,tsx}"],
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
