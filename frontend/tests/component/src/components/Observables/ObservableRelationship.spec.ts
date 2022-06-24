import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import ObservableRelationship from "@/components/Node/ObservableRelationship.vue";

const props = {
  type: "IS_HASH_OF",
  value: "file.txt",
};

describe("ObservableRelationship", () => {
  it("renders correctly", () => {
    mount(ObservableRelationship, {
      global: {
        plugins: [PrimeVue, createPinia()],
      },
      propsData: props,
    });
    cy.contains("IS_HASH_OF: file.txt").should("be.visible");
  });
});
