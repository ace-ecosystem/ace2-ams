import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import NodeRelationship from "@/components/Node/NodeRelationship.vue";

const props = {
  type: "IS_HASH_OF",
  value: "file.txt",
};

describe("NodeRelationship", () => {
  it("renders correctly", () => {
    mount(NodeRelationship, {
      global: {
        plugins: [PrimeVue, createPinia()],
      },
      propsData: props,
    });
    cy.contains("IS_HASH_OF: file.txt").should("be.visible");
  });
});
