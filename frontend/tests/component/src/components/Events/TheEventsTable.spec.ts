import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import { testConfiguration } from "@/etc/configuration/test/index";

import TheEventsTable from "@/components/Events/TheEventsTable.vue";
import router from "@/router/index";

// Nothing will show because there is no queue set to decide the available columns
describe("TheEventsTable", () => {
  it("renders", () => {
    mount(TheEventsTable, {
      global: {
        plugins: [PrimeVue, createPinia(), router],
        provide: {
          nodeType: "events",
          config: testConfiguration,
        },
      },
    });
  });
});
