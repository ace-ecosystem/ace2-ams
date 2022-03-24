// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import CommentModal from "@/components/Modals/CommentModal.vue";


describe("CommentModal", () => {
  it("renders", () => {

    mount(CommentModal, {
      global: {
        plugins: [PrimeVue, createPinia()],
        provide: {
          nodeType: "alerts",
        },
      },
      propsData: {
        name: "CommentModal",
      },
    });
  });
});
