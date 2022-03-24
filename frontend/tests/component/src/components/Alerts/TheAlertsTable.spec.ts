// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import TheAlertsTable from "@/components/Alerts/TheAlertsTable.vue";
import router from "@/router/index";

describe("TheAlertsTable", () => {
  it("renders", () => {
    mount(TheAlertsTable, {
      global: {
        plugins: [PrimeVue, createPinia(), router],
        provide: {
          nodeType: "alerts",
        },
      },
    });
  });
});
