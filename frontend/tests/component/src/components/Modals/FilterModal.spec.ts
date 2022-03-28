// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import PrimeVue from "primevue/config";

import FilterModal from "@/components/Modals/FilterModal.vue";

describe("FilterModal", () => {
  it("renders", () => {
    mount(FilterModal, {
      global: {
        plugins: [
          PrimeVue,
          createCustomCypressPinia({
            initialState: {
              currentUserSettingsStore: {
                queues: {
                  alerts: { value: "external" },
                  events: { value: "external" },
                },
              },
              modalStore: { openModals: ["FilterModal"] },
            },
          }),
        ],
        provide: {
          nodeType: "alerts",
        },
      },
      propsData: {
        name: "FilterModal",
      },
    });
  });
});
