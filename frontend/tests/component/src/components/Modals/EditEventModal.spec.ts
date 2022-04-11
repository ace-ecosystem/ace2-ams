// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import EditEventModal from "@/components/Modals/EditEventModal.vue";
import { Event } from "@/services/api/event";
import { eventReadFactory, mockEventUUID } from "@mocks/events";
import { testConfiguration } from "@/etc/configuration/test/index";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { genericObjectReadFactory } from "@mocks/genericObject";

function factory(args = { modalIsOpen: true, stubActions: true }) {
  let initialState;
  if (args.modalIsOpen) {
    initialState = { modalStore: { openModals: ["EditEventModal"] } };
  } else {
    initialState = { modalStore: { openModals: [] } };
  }
  const wrapper = mount(EditEventModal, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          initialState: initialState,
          stubActions: args.stubActions,
        }),
      ],
      provide: {
        availableEditFields: testConfiguration.events.eventEditableProperties,
      },
    },
    propsData: {
      eventUuid: mockEventUUID,
      name: "EditEventModal",
    },
  });
  return wrapper;
}

describe("EventAlertsTable", () => {
  it.skip("renders when modal is closed", () => {
    cy.stub(Event, "read").returns(eventReadFactory());
    factory({ modalIsOpen: false, stubActions: true });
  });
  it.skip("renders when modal is open", () => {
    cy.stub(Event, "read").returns(eventReadFactory());
    factory();
  });
  it.only("correctly pre-loads the form with existing event data", () => {
    cy.stub(Event, "read").returns(
      eventReadFactory({
        queue: genericObjectReadFactory({ value: "external" }),
      }),
    );
    const wrapper = factory({
      modalIsOpen: false,
      stubActions: false,
    });
    wrapper.then((wrapper) => {
      wrapper.vm.modalStore.open("EditEventModal");
    });
  });
  it("correctly submits updated event data and updates modal form when re-opened", () => {
    cy.stub(Event, "read").returns(eventReadFactory());
    factory();
  });
  it("correctly displays error if event attribute data (status, owners, etc.) cannot be fetched", () => {
    cy.stub(Event, "read").rejects(
      new Error("404 request could not be completed"),
    );
    factory();
  });
  it("correctly displays error if event queue is not valid", () => {
    cy.stub(Event, "read").returns(eventReadFactory());
    factory();
  });
  it("correctly displays error if event data cannot be fetched", () => {
    cy.stub(Event, "read").rejects(
      new Error("404 request could not be completed"),
    );
    factory();
  });
  it("correctly displays error if event cannot be updated", () => {
    cy.stub(Event, "read").returns(eventReadFactory());
    cy.stub(Event, "update").rejects(
      new Error("404 request could not be completed"),
    );
    factory();
  });
});
