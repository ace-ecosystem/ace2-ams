module.exports = {
  preset: "@vue/cli-plugin-unit-jest/presets/typescript-and-babel",
  transform: {
    "^.+\\.vue$": "vue-jest",
  },
  setupFiles: ["<rootDir>/.jest/setEnvVars.js"],
  setupFilesAfterEnv: ["mock-local-storage"],
  moduleNameMapper: {
    "@/(.*)$": "<rootDir>/src/$1",
    "@unit/(.*)$": "<rootDir>/tests/unit/src/$1",
  },
};
