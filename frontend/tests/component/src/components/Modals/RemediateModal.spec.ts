// This component currently not in use; no actual tests have been written

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import RemediateModal from "@/components/Modals/RemediateModal.vue";

describe("RemediateModal", () => {
  it("renders", () => {
    mount(RemediateModal, {
      global: {
        plugins: [PrimeVue, createPinia()],
        provide: {
          nodeType: "alerts",
        },
      },
      propsData: {
        name: "RemediateModal",
      },
    });
  });
});
