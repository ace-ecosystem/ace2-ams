// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createCustomCypressPinia } from "@unit/helpers";

import PrimeVue from "primevue/config";
import { testConfiguration } from "@/etc/configuration/test/index";
import Tooltip from "primevue/tooltip";

import TheFilterToolbar from "@/components/Filters/TheFilterToolbar.vue";
import router from "@/router/index";

// Nothing will show because there is no queue set to decide the available columns
describe("TheFilterToolbar", () => {
  it("renders", () => {
    mount(TheFilterToolbar, {
      global: {
        directives: {tooltip: Tooltip},
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
            },
          }),
          router,
        ],
        provide: {
          nodeType: "alerts",
          rangeFilters: testConfiguration.alerts.alertRangeFilters,
          availableFilters: testConfiguration.alerts.alertFilters,
        },
      },
    });
  });
});
