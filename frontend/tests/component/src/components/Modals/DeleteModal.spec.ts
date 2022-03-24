// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import DeleteModal from "@/components/Modals/DeleteModal.vue";


describe("DeleteModal", () => {
  it("renders", () => {

    mount(DeleteModal, {
      global: {
        plugins: [PrimeVue, createPinia()],
        provide: {
          nodeType: "alerts",
        },
      },
      propsData: {
        name: "DeleteModal",
      },
    });
  });
});
