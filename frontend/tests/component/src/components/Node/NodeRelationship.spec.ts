// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import NodeRelationship from "@/components/Node/NodeRelationship.vue";

const props = {
  type: "IS_HASH_OF",
  value: "file.txt",
};

describe("NodeRelationship", () => {
  it("renders", () => {
    mount(NodeRelationship, {
      global: {
        plugins: [PrimeVue, createPinia()],
      },
      propsData: props,
    });
  });
});
