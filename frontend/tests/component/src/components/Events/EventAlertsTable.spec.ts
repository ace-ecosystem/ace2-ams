// Example Cypress Vue component test that we might use one day

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import router from "@/router";

import EventAlertsTable from "@/components/Events/EventAlertsTable.vue";
import { Alert } from "@/services/api/alert";
import { alertReadFactory } from "../../../../mocks/alert";

const mockAlert = alertReadFactory();

describe("EventAlertsTable", () => {
  it("renders", () => {
    cy.stub(Alert, "readAllPages").returns([mockAlert, mockAlert, mockAlert]);

    mount(EventAlertsTable, {
      global: {
        plugins: [router, PrimeVue, createPinia()],
        provide: { nodeType: "events" },
      },
      propsData: {
        eventUuid: "uuid1",
      },
    });
  });
});
