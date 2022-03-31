// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import router from "@/router/index";
import { testConfiguration } from "@/etc/configuration/test/index";
import ViewAnalysis from "@/pages/Alerts/ViewAnalysis.vue";

describe("ViewAnalysis", () => {
  it("renders", () => {
    mount(ViewAnalysis, {
      global: {
        plugins: [PrimeVue, createPinia(), router],
        provide: { config: testConfiguration },
      },
    });
  });
});
