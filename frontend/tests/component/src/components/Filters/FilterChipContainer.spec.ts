// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import FilterChipContainer from "@/components/Filters/FilterChipContainer.vue";
import router from "@/router/index";

// Nothing will show because there is no queue set to decide the available columns
describe("FilterChipContainer", () => {
  it("renders", () => {
    mount(FilterChipContainer, {
      global: {
        plugins: [PrimeVue, createPinia(), router],
        provide: {
          nodeType: "alerts",
        },
      },
    });
  });
});
