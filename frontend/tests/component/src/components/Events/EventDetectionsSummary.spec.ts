// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import EventDetectionsSummary from "@/components/Events/EventDetectionsSummary.vue";
import router from "@/router/index";
import { Event } from "@/services/api/event";
import { detectionPointSummary } from "@/models/eventSummaries";

const props = {
  eventUuid: "uuid",
};

function factory() {
  return mount(EventDetectionsSummary, {
    global: {
      plugins: [PrimeVue, createPinia(), router],
    },
    propsData: props,
  });
}

describe("EventDetectionsSummary", () => {
  it("renders correctly when API req successfully returns results", () => {
    const result: detectionPointSummary = {
      alertUuid: "alertUuid",
      count: 3,
      insertTime: new Date(3, 14, 2022),
      nodeUuid: "nodeUuid",
      uuid: "detectionUuid",
      value: "Test detection point",
    };
    const detectionSummaryCols = ["Detection", "Count"];
    const detectionSummaryVals = [result.value, result.count];

    cy.stub(Event, "readDetectionSummary")
      .withArgs("uuid")
      .as("readDetectionSummary")
      .returns([result]);

    factory();
    cy.get("[data-cy=error-banner]").should("not.exist");

    // Check table content
    cy.findByRole("table").should("be.visible");
    cy.get("tr").should("have.length", 2);
    cy.get("tr")
      .eq(0)
      .children()
      .each(($li, index) => {
        cy.wrap($li).should("have.text", detectionSummaryCols[index]);
      });
    cy.get("tr")
      .eq(1)
      .children()
      .each(($li, index) => {
        cy.wrap($li).should("contain.text", detectionSummaryVals[index]);
      });

    // Check alert link
    cy.get("a").invoke("attr", "href").should("eql", "/alert/alertUuid");
  });
  it("renders correctly when API req successfully returns empty", () => {
    cy.stub(Event, "readDetectionSummary")
      .withArgs("uuid")
      .as("readDetectionSummary")
      .returns([]);
    factory();
    cy.get("[data-cy=error-banner]").should("not.exist");
    cy.findByRole("table").should("be.visible");
    cy.contains("No detection points found").should("be.visible");
  });
  it("renders correctly when API req fails", () => {
    cy.stub(Event, "readDetectionSummary")
      .withArgs("uuid")
      .as("readDetectionSummary")
      .rejects(new Error("404 request failed"));
    factory();
    cy.get("[data-cy=error-banner]").should("be.visible");
    cy.contains("404 request failed").should("be.visible");
    cy.findByRole("table").should("be.visible");
    cy.contains("No detection points found").should("be.visible");
  });
});
