// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import Tooltip from "primevue/tooltip";

import AnalyzeAlert from "@/pages/Alerts/AnalyzeAlert.vue";

describe("AnalyzeAlert", () => {
  it("renders", () => {
    mount(AnalyzeAlert, {
      global: {
        directives: { tooltip: Tooltip },
        plugins: [PrimeVue, createPinia()],
      },
    });
  });
});
