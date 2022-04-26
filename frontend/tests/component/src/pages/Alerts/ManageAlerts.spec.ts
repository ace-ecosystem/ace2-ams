// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import PrimeVue from "primevue/config";

import router from "@/router/index";
import { testConfiguration } from "@/etc/configuration/test/index";
import Tooltip from "primevue/tooltip";
import ToastService from "primevue/toastservice";

import ManageAlerts from "@/pages/Alerts/ManageAlerts.vue";

describe("ManageAlerts", () => {
  it("renders", () => {
    mount(ManageAlerts, {
      global: {
        directives: { tooltip: Tooltip },
        plugins: [
          ToastService,
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
        provide: { config: testConfiguration, nodeType: "alerts" },
      },
    });
  });
});
