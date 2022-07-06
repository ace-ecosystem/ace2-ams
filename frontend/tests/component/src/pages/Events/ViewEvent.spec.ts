// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import router from "@/router/index";
import { testConfiguration } from "@/etc/configuration/test/index";
import ViewEvent from "@/pages/Events/ViewEvent.vue";
import { Event } from "@/services/api/event";

describe("ViewEvent", () => {
  it("renders", () => {
    const getStub = cy.stub(Event, "read");
    getStub.as("readEvent").resolves();

    mount(ViewEvent, {
      global: {
        plugins: [PrimeVue, createPinia(), router],
        provide: { config: testConfiguration },
      },
    });
  });
});
