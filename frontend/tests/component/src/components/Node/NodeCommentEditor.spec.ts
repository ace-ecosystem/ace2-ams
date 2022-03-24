// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import { commentReadFactory } from "@mocks/comment";

import NodeCommentEditor from "@/components/Node/NodeCommentEditor.vue";

const props = {
  modelValue: [commentReadFactory()],
};

describe("NodeCommentEditor", () => {
  it("renders", () => {
    mount(NodeCommentEditor, {
      global: {
        plugins: [PrimeVue, createPinia()],
      },
      propsData: props,
    });
  });
});
