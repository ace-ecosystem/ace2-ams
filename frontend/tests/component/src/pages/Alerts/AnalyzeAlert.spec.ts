// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import AnalyzeAlert from "@/pages/Alerts/AnalyzeAlert.vue";

describe("AnalyzeAlert", () => {
  it("renders", () => {
    mount(AnalyzeAlert, {
      global: {
        plugins: [PrimeVue, createPinia()],
      },
    });
  });
});
