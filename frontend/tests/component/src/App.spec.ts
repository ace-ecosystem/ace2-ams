// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import App from "@/App.vue";

describe("App", () => {
  it("renders", () => {
    mount(App, {
      global: {
        plugins: [PrimeVue, createPinia()],
      },
    });
  });
});
