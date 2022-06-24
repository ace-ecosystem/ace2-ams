// This component currently not in use; no actual tests have been written

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
          objectType: "alerts",
        },
      },
      propsData: {
        name: "DeleteModal",
      },
    });
  });
});
