// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import router from "@/router/index";
import { testConfiguration } from "@/etc/configuration/test/index";

import ViewAlert from "@/pages/Alerts/ViewAlert.vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { Alert } from "@/services/api/alert";
import { alertTreeReadFactory } from "@mocks/alert";
import TheAlertActionToolbarVue from "@/components/Alerts/TheAlertActionToolbar.vue";
import TheAlertSummaryVue from "@/components/Alerts/TheAlertSummary.vue";
import AlertTreeVue from "@/components/Alerts/AlertTree.vue";
import { userReadFactory } from "@mocks/user";

function factory(stubActions = true) {
  return mount(ViewAlert, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          stubActions: stubActions,
          initialState: {
            authStore: {
              user: userReadFactory(),
            },
          },
        }),
        router,
      ],
      provide: { config: testConfiguration },
    },
  });
}

describe("ViewAlert", () => {
  it("renders correctly when alert can be fetched", () => {
    cy.stub(Alert, "read").resolves(alertTreeReadFactory());
    factory(false).then((wrapper) => {
      cy.get("@spy-9").should("have.been.calledOnce"); // unselectAll
      cy.get("@spy-6").should("have.been.calledOnce"); // select alert
      cy.get("@spy-5").should("have.been.calledOnce"); // 'patch' aka reset alertStore
      cy.get("@spy-3").should("have.been.calledOnce"); // read alert
      expect(wrapper.findComponent(TheAlertActionToolbarVue)).to.exist;
      expect(wrapper.findComponent(TheAlertSummaryVue)).to.exist;
      expect(wrapper.findComponent(AlertTreeVue)).to.exist;
    });
  });
  it("attempts to disposition alert as 'false positive' on ignoreClicked event", () => {
    cy.stub(Alert, "read").resolves(alertTreeReadFactory());
    cy.stub(Alert, "update")
      .withArgs([
        {
          uuid: undefined,
          disposition: "FALSE_POSITIVE",
          historyUsername: "analyst",
        },
      ])
      .as("dispositionFP")
      .resolves();
    factory(false);
    cy.get("body").then(() => {
      Cypress.vueWrapper
        .findComponent(TheAlertActionToolbarVue)
        .vm.$emit("falsePositiveClicked");
    });
    cy.get("@dispositionFP").should("have.been.calledOnce");
    cy.get("@spy-3").should("have.been.calledTwice"); // read alert should be called again
  });
  it("attempts to disposition alert as 'ignore' on ignoreClicked event", () => {
    cy.stub(Alert, "read").resolves(alertTreeReadFactory());
    cy.stub(Alert, "update")
      .withArgs([
        {
          uuid: undefined,
          disposition: "IGNORE",
          historyUsername: "analyst",
        },
      ])
      .as("dispositionIgnore")
      .resolves();
    factory(false);
    cy.get("body").then(() => {
      Cypress.vueWrapper
        .findComponent(TheAlertActionToolbarVue)
        .vm.$emit("ignoreClicked");
    });
    cy.get("@dispositionIgnore").should("have.been.calledOnce");
    cy.get("@spy-3").should("have.been.calledTwice"); // read alert should be called again
  });
  it("will display error message if attempt to use FP disposition shortcut fails", () => {
    cy.stub(Alert, "read").resolves(alertTreeReadFactory());
    cy.stub(Alert, "update")
      .withArgs([
        {
          uuid: undefined,
          disposition: "FALSE_POSITIVE",
          historyUsername: "analyst",
        },
      ])
      .as("dispositionFP")
      .rejects(new Error("404 request failed"));
    factory(false);
    cy.get("body").then(() => {
      Cypress.vueWrapper
        .findComponent(TheAlertActionToolbarVue)
        .vm.$emit("falsePositiveClicked");
    });
    cy.get("@dispositionFP").should("have.been.calledOnce");
    cy.get("@spy-3").should("have.been.calledOnce"); // read alert should not be called again
    cy.get("[data-cy=error-message]")
      .should("be.visible")
      .should("contain.text", "404 request failed");
  });
  it("will display error message if attempt to use ignore disposition shortcut fails", () => {
    cy.stub(Alert, "read").resolves(alertTreeReadFactory());
    cy.stub(Alert, "update")
      .withArgs([
        {
          uuid: undefined,
          disposition: "IGNORE",
          historyUsername: "analyst",
        },
      ])
      .as("dispositionIgnore")
      .rejects(new Error("404 request failed"));
    factory(false);
    cy.get("body").then(() => {
      Cypress.vueWrapper
        .findComponent(TheAlertActionToolbarVue)
        .vm.$emit("ignoreClicked");
    });
    cy.get("@dispositionIgnore").should("have.been.calledOnce");
    cy.get("@spy-3").should("have.been.calledOnce"); // read alert should not be called again
    cy.get("[data-cy=error-message]")
      .should("be.visible")
      .should("contain.text", "404 request failed");
  });
});
