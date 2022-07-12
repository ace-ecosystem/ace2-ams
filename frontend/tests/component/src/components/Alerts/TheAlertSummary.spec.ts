import { mount } from "@cypress/vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";

import PrimeVue from "primevue/config";

import TheAlertSummary from "@/components/Alerts/TheAlertSummary.vue";
import router from "@/router/index";
import { alertReadFactory } from "@mocks/alert";
import { alertRead } from "@/models/alert";
import { genericObjectReadFactory } from "@mocks/genericObject";
import { userReadFactory } from "@mocks/user";
import {
  metadataDetectionPointReadFactory,
  metadataTagReadFactory,
} from "@mocks/metadata";

function factory(initialAlertStoreState: {
  open: null | alertRead;
  requestReload: boolean;
}) {
  return mount(TheAlertSummary, {
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

describe("TheAlertSummary", () => {
  it("renders correctly when there is not an open alert", () => {
    factory({
      open: null,
      requestReload: false,
    });
    cy.contains("Test Alert").should("not.exist");
  });
  it("renders correctly when there is an open alert that has no observables with detection points or instructions", () => {
    factory({
      open: alertReadFactory({
        tags: [metadataTagReadFactory({ value: "TestTag" })],
      }),
      requestReload: false,
    });

    cy.contains("Test Alert").should("be.visible");
    cy.get("button .pi-link").should("be.visible");
    cy.get("tr").should("have.length", 11);
    cy.contains("Insert Time")
      .siblings()
      .should("have.text", "2/24/2022, 12:00:00 AM UTC");
    cy.contains("Event Time")
      .siblings()
      .should("have.text", "2/24/2022, 12:00:00 AM UTC");
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
    cy.contains("No detections found").should("be.visible");
  });
  it("renders correctly when there is an open alert has an owner and disposition set (uses the correct alertSummary fields)", () => {
    const date = "2020-05-04T12:00:00.000000+00:00";
    factory({
      open: alertReadFactory({
        tags: [metadataTagReadFactory({ value: "TestTag" })],
        owner: userReadFactory(),
        ownershipTime: date,
        disposition: {
          rank: 0,
          ...genericObjectReadFactory({ value: "FALSE POSITIVE" }),
        },
        dispositionUser: userReadFactory(),
        dispositionTime: date,
      }),
      requestReload: false,
    });

    // Should still have all the same rows
    cy.get("tr").should("have.length", 11);
    // Check these specific fields
    cy.contains("Disposition")
      .siblings()
      .should(
        "have.text",
        "FALSE POSITIVE by Test Analyst @ 5/4/2020, 12:00:00 PM UTC",
      );
    cy.contains("Owner")
      .siblings()
      .should("have.text", "Test Analyst @ 5/4/2020, 12:00:00 PM UTC");
  });
  it("renders correctly when there is an open alert that has instructions available", () => {
    factory({
      open: alertReadFactory({
        instructions: "alert instructions example",
        tags: [metadataTagReadFactory({ value: "TestTag" })],
      }),
      requestReload: false,
    });

    cy.get("tr").should("have.length", 12);
    cy.contains("Instructions")
      .siblings()
      .should("have.text", "alert instructions example");
  });
  it("renders correctly when there is an open alert that does have observables with detection points", () => {
    const detectionPointA = metadataDetectionPointReadFactory({
      value: "detectionA",
    });
    const detectionPointB = metadataDetectionPointReadFactory({
      value: "detectionB",
    });
    const detectionPointC = metadataDetectionPointReadFactory({
      value: "detectionC",
    });

    factory({
      open: alertReadFactory({
        // The detection points are returned from the API sorted by their values
        childDetectionPoints: [
          detectionPointA,
          detectionPointB,
          detectionPointC,
        ],
        tags: [metadataTagReadFactory({ value: "TestTag" })],
      }),
      requestReload: false,
    });

    cy.findAllByText("Detection").should("have.length", 3);
    cy.findAllByText("Detection")
      .eq(0)
      .siblings()
      .should("contain.text", "detectionA");
    cy.findAllByText("Detection");
    cy.findAllByText("Detection")
      .eq(1)
      .siblings()
      .should("contain.text", "detectionB");
    cy.findAllByText("Detection")
      .eq(2)
      .siblings()
      .should("contain.text", "detectionC");
  });
});
