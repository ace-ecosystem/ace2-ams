// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import Tooltip from "primevue/tooltip";

import { testConfiguration } from "@/etc/configuration/test/index";

import DateRangePicker from "@/components/UserInterface/DateRangePicker.vue";

const props = {
    columns: [{ field: "name", header: "Name", sortable: true, default: true }],
};

describe("DateRangePicker", () => {
  it("renders", () => {
    mount(DateRangePicker, {
      global: {
          directives: {tooltip: Tooltip},
        plugins: [PrimeVue, createPinia()],
        provide: {nodeType: "alerts", rangeFilters: testConfiguration.alerts.alertRangeFilters}
      },
    });
  });
});
