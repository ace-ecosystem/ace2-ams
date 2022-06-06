import { defineConfig } from "cypress";

export default defineConfig({
  fixturesFolder: "tests/e2e/fixtures",
  screenshotsFolder: "tests/e2e/screenshots",
  videosFolder: "tests/e2e/videos",
  viewportWidth: 1280,
  viewportHeight: 720,
  e2e: {
    specPattern: "tests/e2e/specs/**/*.spec.js",
    supportFile: "tests/e2e/support/index-e2e.js",
    baseUrl: "http://ace2-ams:8080",
  },
  component: {
    specPattern: "tests/component/src/**/*.spec.ts",
    supportFile: "tests/e2e/support/index-ct.js",
    devServer: {
      framework: "vue",
      bundler: "vite",
    },
  },
});
