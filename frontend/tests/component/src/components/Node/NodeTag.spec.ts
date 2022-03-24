// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import NodeTag from "@/components/Node/NodeTag.vue";

const props = {
  tag: { value: "testTag" },
};

describe("NodeTag", () => {
  it("renders", () => {
    mount(NodeTag, {
      global: {
        plugins: [PrimeVue, createPinia()],
        provide: { nodeType: "alerts" },
      },
      propsData: props,
    });
  });
});
