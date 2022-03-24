// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import { commentReadFactory } from "../../../../mocks/comment";

import NodeComment from "@/components/Node/NodeComment.vue";

const props = {
  comment: commentReadFactory(),
};

describe("NodeComment", () => {
  it("renders", () => {
    mount(NodeComment, {
      global: {
        plugins: [PrimeVue, createPinia()],
      },
      propsData: props,
    });
  });
});
