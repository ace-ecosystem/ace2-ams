// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import PrimeVue from "primevue/config";

import router from "@/router/index";
import { testConfiguration } from "@/etc/configuration/test/index";
import Tooltip from "primevue/tooltip";

import ManageEvents from "@/pages/Events/ManageEvents.vue";

describe("ManageEvents", () => {
  it("renders", () => {
    mount(ManageEvents, {
      global: {
        directives: { tooltip: Tooltip },
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
        provide: { config: testConfiguration, nodeType: "events" },
      },
    });
  });
});
