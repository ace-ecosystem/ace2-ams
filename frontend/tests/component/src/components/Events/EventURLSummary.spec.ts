// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import { testConfiguration } from "@/etc/configuration/test/index";
import EventURLSummary from "@/components/Events/EventURLSummary.vue";
import router from "@/router/index";
import { NodeTree } from "@/services/api/nodeTree";
import { observableReadFactory } from "@mocks/observable";
import { genericObjectReadFactory } from "@mocks/genericObject";

const props = {
  eventAlertUuids: ["uuidA"],
};

function factory() {
  return mount(EventURLSummary, {
    global: {
      plugins: [PrimeVue, createPinia(), router],
      provide: { config: testConfiguration },
    },
    propsData: props,
  });
}

describe("EventURLSummary", () => {
  it("renders correctly when request to fetch URLs successfully returns results", () => {
    cy.stub(NodeTree, "readNodesOfNodeTree")
      .withArgs(props.eventAlertUuids, "observable")
      .returns([
        observableReadFactory(),
        observableReadFactory({
          value: "www.google.com",
          type: genericObjectReadFactory({ value: "url" }),
        }),
      ]);
    factory();
    cy.findByRole("listbox").children().should("have.length", 1);
    cy.findByRole("listbox")
      .children()
      .eq(0)
      .should("have.text", "www.google.com");
  });
  it("renders correctly when request to fetch URLs successfully returns empty", () => {
    cy.stub(NodeTree, "readNodesOfNodeTree")
      .withArgs(props.eventAlertUuids, "observable")
      .returns([]);
    factory();
    cy.findByRole("listbox").should(
      "contain.text",
      "This event doesn't have any URL observables.",
    );
  });
  it("renders correctly when request to fetch URLs fails", () => {
    cy.stub(NodeTree, "readNodesOfNodeTree")
      .withArgs(props.eventAlertUuids, "observable")
      .rejects(new Error("404 request failed"));
    factory();
    cy.get("[data-cy=error-banner]").should(
      "contain.text",
      "404 request failed",
    );
    cy.findByRole("listbox").should(
      "contain.text",
      "This event doesn't have any URL observables.",
    );
  });
});
