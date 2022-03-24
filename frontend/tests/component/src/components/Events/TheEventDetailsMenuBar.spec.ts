// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createCustomCypressPinia } from "@unit/helpers";

import PrimeVue from "primevue/config";

import TheEventDetailsMenuBar from "@/components/Events/TheEventDetailsMenuBar.vue";
import router from "@/router/index";

import { testConfiguration } from "@/etc/configuration/test/index";

const props = {
  eventUuid: "uuid",
};

describe("TheEventDetailsMenuBar", () => {
  it("renders", () => {
    mount(TheEventDetailsMenuBar, {
      global: {
        provide: {
          nodeType: "events",
          availableEditFields: testConfiguration.events.eventEditableProperties,
        },
        plugins: [
          PrimeVue,
          createCustomCypressPinia({
            initialState: {
              eventStore: {
                open: {
                  name: "test",
                  tags: [],
                  childTags: [],
                  comments: [],
                  insert_time: "03/23/2022",
                  uuid: "test",
                  queue: { value: "test" },
                  type: { value: "test" },
                  analysisTypes: [],
                },
                requestReload: false,
              },
            },
          }),
          router,
        ],
      },
      propsData: props,
    });
  });
});
