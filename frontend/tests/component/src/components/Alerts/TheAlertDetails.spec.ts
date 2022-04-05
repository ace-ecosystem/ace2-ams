// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";

import PrimeVue from "primevue/config";

import TheAlertDetails from "@/components/Alerts/TheAlertDetails.vue";
import router from "@/router/index";
import { alertReadFactory } from "@mocks/alert";
import { alertRead } from "@/models/alert";
import { genericObjectReadFactory } from "@mocks/genericObject";

function factory(initialAlertStoreState: {
  open: null | alertRead;
  requestReload: boolean;
}) {
  return mount(TheAlertDetails, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          initialState: { alertStore: initialAlertStoreState },
        }),
        router,
      ],
    },
  });
}

describe("TheAlertDetails", () => {
  it("renders correctly when there is not an open alert", () => {
    factory({
      open: null,
      requestReload: false,
    });
    cy.contains("Test Alert").should("not.exist");
  });
  it("renders correctly when there is an open alert", () => {
    factory({
      open: alertReadFactory({
        tags: [genericObjectReadFactory({ value: "TestTag" })],
      }),
      requestReload: false,
    });
    cy.contains("Test Alert").should("be.visible");
    cy.get("button .pi-link").should("be.visible");
    cy.get("tr").should("have.length", 10);
    cy.contains("Insert Time")
      .siblings()
      .should("have.text", "3/24/2022, 12:00:00 AM");
    cy.contains("Event Time")
      .siblings()
      .should("have.text", "3/24/2022, 12:00:00 AM");
    cy.contains("Tool").siblings().should("have.text", "testAlertTool");
    cy.contains("Tool Instance")
      .siblings()
      .should("have.text", "testAlertToolInstance");
    cy.contains("Type").siblings().should("have.text", "testAlertType");
    cy.contains("Disposition").siblings().should("have.text", "OPEN");
    cy.get("td:contains(Event)").eq(1).siblings().should("have.text", "None");
    cy.contains("Queue").siblings().should("have.text", "testAlertQueue");
    cy.contains("Owner").siblings().should("have.text", "None");
    cy.contains("Comments").siblings().should("have.text", "None");
  });
});
