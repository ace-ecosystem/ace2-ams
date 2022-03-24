// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import EditEventModal from "@/components/Modals/EditEventModal.vue";
import { Event } from "@/services/api/event";
import { eventReadFactory, mockEventUUID } from "./@mocks/events";
import { testConfiguration } from "@/etc/configuration/test/index";

describe("EventAlertsTable", () => {
  it("renders", () => {
    cy.stub(Event, "read").returns(eventReadFactory());

    mount(EditEventModal, {
      global: {
        plugins: [PrimeVue, createPinia()],
        provide: {
          availableEditFields: testConfiguration.events.eventEditableProperties,
        },
      },
      propsData: {
        eventUuid: mockEventUUID,
        name: "EditEventModal",
      },
    });
  });
});
