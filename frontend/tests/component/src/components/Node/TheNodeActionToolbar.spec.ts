// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import TheNodeActionToolbar from "@/components/Node/TheNodeActionToolbar.vue";

const props = {
  reloadObject: "node",
};

describe("TheNodeActionToolbar", () => {
  it("renders", () => {
    mount(TheNodeActionToolbar, {
      global: {
        plugins: [PrimeVue, createPinia()],
        provide: { nodeType: "alerts" },
      },
      propsData: props,
    });
  });
});
