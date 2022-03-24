// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import FilterChip from "@/components/Filters/FilterChip.vue";
import router from "@/router/index";

const props = {
  filterName: "name",
  filterValue: "test",
};

// Nothing will show because there is no queue set to decide the available columns
describe("FilterChip", () => {
  it("renders", () => {
    mount(FilterChip, {
      global: {
        plugins: [PrimeVue, createPinia(), router],
        provide: {
          nodeType: "alerts",
        },
      },
      propsData: props,
    });
  });
});
