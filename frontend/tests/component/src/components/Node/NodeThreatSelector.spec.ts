// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import NodeThreatSelector from "@/components/Node/NodeThreatSelector.vue";

describe("NodeThreatSelector", () => {
  it("renders", () => {
    mount(NodeThreatSelector, {
      global: {
        plugins: [PrimeVue, createPinia()],
      },
      propsData: {
        modelValue: "EditEventModal",
      },
    });
  });
});
