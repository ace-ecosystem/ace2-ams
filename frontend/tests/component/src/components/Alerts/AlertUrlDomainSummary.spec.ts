import { mount } from "@cypress/vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";

import PrimeVue from "primevue/config";

import AlertUrlDomainSummary from "@/components/Alerts/AlertUrlDomainSummary.vue";
import router from "@/router/index";
import { alertRead } from "@/models/alert";
import { alertReadFactory } from "@mocks/alert";
import { genericObjectReadFactory } from "@mocks/genericObject";
import { observableReadFactory } from "@mocks/observable";
import { observableRead } from "@/models/observable";

function factory(initialAlertStoreState: {
  open: null | alertRead;
  requestReload: boolean;
  openObservables: observableRead[];
}) {
  return mount(AlertUrlDomainSummary, {
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

// These tests are broken - dependent on backend change to receive all (not unique) observables for a given alert
describe("AlertUrlDomainSummary", () => {
  it("renders correctly when there is not an open alert", () => {
    factory({
      open: null,
      requestReload: false,
      openObservables: [],
    });
    cy.get('[data-cy="url-domain-summary-panel"]').should("not.exist");
  });
  it("renders correctly when there is an open alert with no domain observables", () => {
    factory({
      open: alertReadFactory(),
      requestReload: false,
      openObservables: [observableReadFactory()],
    });
    cy.get('[data-cy="url-domain-summary-panel"]').should("not.exist");
  });
  it("renders correctly when there is an open alert with at least one domain observable", () => {
    factory({
      open: alertReadFactory(),
      requestReload: false,
      openObservables: [
        observableReadFactory(),
        observableReadFactory({
          type: genericObjectReadFactory({ value: "fqdn" }),
        }),
      ],
    });
    cy.get('[data-cy="url-domain-summary-panel"]').should("be.visible");
    // Should be collapsed to start
    cy.get('[data-cy="url-domain-summary-table"]').should("not.be.visible");
    // Open panel and check table
    cy.contains("URL Domain Summary").click();
    cy.get('[data-cy="url-domain-summary-table"]').should("be.visible");
    cy.get("td").should("have.length", 3);
    cy.get("td").eq(0).should("have.text", "TestObservable");
    cy.get("td").eq(1).should("have.text", "1");
    cy.get("td").eq(2).should("have.text", "50.00%");
    // Close panel again
    cy.contains("URL Domain Summary").click();
    cy.get('[data-cy="url-domain-summary-table"]').should("not.be.visible");
  });
});
