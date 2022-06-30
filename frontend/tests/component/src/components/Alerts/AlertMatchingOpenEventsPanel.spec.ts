import { mount } from "@cypress/vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { alertTreeReadFactory } from "@mocks/alert";
import { eventReadFactory } from "@mocks/events";
import { genericObjectReadFactory } from "@mocks/genericObject";

import PrimeVue from "primevue/config";
import { testConfiguration } from "@/etc/configuration/test/index";

import AlertMatchingOpenEventsPanel from "@/components/Alerts/AlertMatchingOpenEventsPanel.vue";

function factory(openAlert: alertTreeRead | undefined) {
  mount(AlertMatchingOpenEventsPanel, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          initialState: { alertStore: { open: openAlert } },
        }),
      ],
      provide: {
        config: testConfiguration,
      },
    },
  });
}

describe("AlertMatchingOpenEventsPanel", () => {
  it("doesn't render and doesn't error when there is no open alert", () => {
    factory();
    cy.get("[data-cy=matching-open-events-panel]").should("not.exist");
    cy.get("[data-cy=matching-open-events-table]").should("not.exist");
  });
  it("doesn't render and doesn't error when the open alert doesn't have any matchingEvents", () => {
    factory(alertTreeReadFactory());
    cy.get("[data-cy=matching-open-events-panel]").should("not.exist");
    cy.get("[data-cy=matching-open-events-table]").should("not.exist");
  });
  it("doesn't render and doesn't error when the open alert doesn't have any OPEN matchingEvents", () => {
    const matchingEvents: submissionMatchingEventByStatus[] = [
      {
        status: "CLOSED",
        events: [{ count: 1, percent: 100, event: eventReadFactory() }],
      },
    ];
    const openAlert = alertTreeReadFactory({ matchingEvents: matchingEvents });
    factory(openAlert);
    cy.get("[data-cy=matching-open-events-panel]").should("not.exist");
    cy.get("[data-cy=matching-open-events-table]").should("not.exist");
  });
  it("renders correctly when there are OPEN matchingEvents", () => {
    const matchingEvents: submissionMatchingEventByStatus[] = [
      {
        status: "CLOSED",
        events: [{ count: 1, percent: 100, event: eventReadFactory() }],
      },
      {
        status: "OPEN",
        events: [
          { count: 1, percent: 50, event: eventReadFactory({ uuid: "uuidA" }) },
          {
            count: 1,
            percent: 50,
            event: eventReadFactory({
              name: "Test Event B",
              uuid: "uuidB",
              allTags: [
                genericObjectReadFactory({ value: "Test Tag A" }),
                genericObjectReadFactory({ value: "Test Tag B" }),
              ],
              threats: [genericObjectReadFactory({ value: "Threat A" })],
            }),
          },
        ],
      },
    ];
    const openAlert = alertTreeReadFactory({ matchingEvents: matchingEvents });
    factory(openAlert);
    cy.get("[data-cy=matching-open-events-panel]").should("be.visible");
    cy.get("[data-cy=matching-open-events-table]").should("not.be.visible");
    cy.contains(
      "Matching Open Events: 2 Event(s) | 1/0 matching observables | Test Event",
    ).should("be.visible");
    cy.get(".pi").click(); // expand the panel
    cy.get("[data-cy=matching-open-events-table]").should("be.visible");

    // Check header row
    cy.get("tr")
      .eq(0)
      .children()
      .should("have.length", 4)
      .each(($td, index) => {
        if (index === 0) {
          cy.wrap($td).contains("Event");
        } else if (index === 1) {
          cy.wrap($td).contains("Match");
        } else if (index === 2) {
          cy.wrap($td).contains("Threat Names");
        } else if (index === 3) {
          cy.wrap($td).contains("Tags");
        }
      });

    // Check first event row
    cy.get("tr")
      .eq(1)
      .children()
      .should("have.length", 4)
      .each(($td, index) => {
        if (index === 0) {
          cy.wrap($td).contains("Test Event");
          cy.wrap($td)
            .find("router-link")
            .invoke("attr", "to")
            .should("equal", "/event/uuidA");
        } else if (index === 1) {
          cy.wrap($td).contains("50% (1)");
        } else if (index === 2) {
          cy.wrap($td).contains("No threats");
        } else if (index === 3) {
          cy.wrap($td).contains("No tags");
        }
      });

    // Check second event row
    cy.get("tr")
      .eq(2)
      .children()
      .should("have.length", 4)
      .each(($td, index) => {
        if (index === 0) {
          cy.wrap($td).contains("Test Event B");
          cy.wrap($td)
            .find("router-link")
            .invoke("attr", "to")
            .should("equal", "/event/uuidB");
        } else if (index === 1) {
          cy.wrap($td).contains("50% (1)");
        } else if (index === 2) {
          cy.wrap($td)
            .find(".p-tag")
            .should("have.length", 1)
            .should("contain", "Threat A");
        } else if (index === 3) {
          cy.wrap($td).find(".p-tag").should("have.length", 2);
          cy.wrap($td).find(".p-tag").eq(0).should("contain", "Test Tag A");
          cy.wrap($td).find(".p-tag").eq(1).should("contain", "Test Tag B");
        }
      });
  });
});
