// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import { testConfiguration } from "@/etc/configuration/test/index";

import NodePropertyInput from "@/components/Node/NodePropertyInput.vue";

const props = {
  modelValue: { propertyType: null, propertyValue: null },
  queue: "external",
  formType: "filter",
};

describe("NodePropertyInput", () => {
  it("renders", () => {
    mount(NodePropertyInput, {
      global: {
        plugins: [PrimeVue, createPinia()],
        provide: {
          availableEditFields: {},
          availableFilters: testConfiguration.alerts.alertFilters,
        },
      },
      propsData: props,
    });
  });
});
