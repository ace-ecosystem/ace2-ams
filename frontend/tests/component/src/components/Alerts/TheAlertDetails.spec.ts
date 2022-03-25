// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createCustomCypressPinia } from "@unit/helpers";

import PrimeVue from "primevue/config";

import TheAlertDetails from "@/components/Alerts/TheAlertDetails.vue";
import router from "@/router/index";

describe("TheAlertDetails", () => {
  it("renders", () => {
    mount(TheAlertDetails, {
      global: {
        plugins: [
          PrimeVue,
          createCustomCypressPinia({
            initialState: {
              alertStore: {
                open: {
                  name: "test",
                  tags: [],
                  childTags: [],
                  comments: [],
                  insert_time: "03/23/2022",
                  uuid: "test",
                  queue: { value: "test" },
                  type: { value: "test" },
                },
                requestReload: false,
              },
            },
          }),
          router,
        ],
      },
    });
  });
});
