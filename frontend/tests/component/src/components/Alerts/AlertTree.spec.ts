// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import AlertTree from "@/components/Alerts/AlertTree.vue";
import { createCustomCypressPinia } from "@unit/helpers";
import router from "@/router/index";

const props = {
  items: [],
};

describe("AlertTree", () => {
  it("renders", () => {
    mount(AlertTree, {
      global: {
        plugins: [
          PrimeVue,
          createCustomCypressPinia({
            initialState: {
              alertStore: { open: { uuid: "test" }, requestReload: false },
            },
          }),
          router,
        ],
      },
      propsData: props,
    });
  });
});
