import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import { testConfiguration } from "@/etc/configuration/test/index";
import AlertUrlDomainSummary from "@/components/Alerts/AlertUrlDomainSummary.vue";
import router from "@/router/index";
import { Alert } from "@/services/api/alert";

const props = {
  alertUuid: "uuid",
};

function factory() {
  return mount(AlertUrlDomainSummary, {
    global: {
      plugins: [PrimeVue, createPinia(), router],
      provide: { config: testConfiguration },
    },
    propsData: props,
  });
}

describe("AlertUrlDomainSummary", () => {
  it("renders correctly when request to fetch data fails", () => {
    cy.stub(Alert, "readUrlDomainSummary")
      .withArgs("uuid")
      .rejects(new Error("404 Request failed"));
    factory();
    cy.get("[data-cy=error-banner]")
      .should("be.visible")
      .should("contain.text", "URL Domain Summary: 404 Request failed");
    cy.get("[data-cy=alert-url-domain-summary]").should("not.exist");
  });
  it("renders correctly when request to fetch data successfully returns empty", () => {
    cy.stub(Alert, "readUrlDomainSummary")
      .withArgs("uuid")
      .returns({ domains: [] });
    factory();
    cy.get("[data-cy=alert-url-domain-summary]").should("not.exist"); // Panel shouldn't exist if there's domains
  });
  it("renders correctly when request to fetch data successfully returns results", () => {
    cy.stub(Alert, "readUrlDomainSummary")
      .withArgs("uuid")
      .returns({
        domains: [
          { domain: "google.com", count: 10 },
          { domain: "youtube.com", count: 5 },
        ],
      });
    factory();
    cy.get("#pv_id_1_header > .pi").click(); // Open panel, should be collapsed by default
    cy.get("canvas").should("be.visible");
    cy.findByRole("table").should("be.visible");
    cy.get("tr").should("have.length", 3);
    cy.get("tr").eq(0).children().eq(0).should("contain.text", "Domain");
    cy.get("tr").eq(0).children().eq(1).should("contain.text", "Count");
    cy.get("tr").eq(1).children().eq(0).should("contain.text", "google.com");
    cy.get("tr").eq(1).children().eq(1).should("contain.text", "10");
    cy.get("tr").eq(2).children().eq(0).should("contain.text", "youtube.com");
    cy.get("tr").eq(2).children().eq(1).should("contain.text", "5");
  });
});
