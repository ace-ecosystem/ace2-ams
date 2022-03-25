// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import NodeQueueSelector from "@/components/Node/NodeQueueSelector.vue";

const props = {
  nodeQueue: "external",
};

describe("NodeQueueSelector", () => {
  it("renders", () => {
    mount(NodeQueueSelector, {
      global: {
        plugins: [PrimeVue, createPinia()],
      },
      propsData: props,
    });
  });
});
