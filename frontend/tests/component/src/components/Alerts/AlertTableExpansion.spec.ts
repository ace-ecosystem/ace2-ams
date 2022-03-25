// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import AlertTableExpansion from "@/components/Alerts/AlertTableExpansion.vue";
import router from "@/router/index";
import { observableReadFactory } from "../../../../mocks/observable";

const props = {
  observables: [observableReadFactory()],
};

describe("AlertTableExpansion", () => {
  it("renders", () => {
    mount(AlertTableExpansion, {
      global: {
        plugins: [PrimeVue, createPinia(), router],
      },
      propsData: props,
    });
  });
});
