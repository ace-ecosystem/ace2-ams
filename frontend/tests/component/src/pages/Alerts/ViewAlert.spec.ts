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
import AnalysisSummaryDetailVue from "@/components/Analysis/AnalysisSummaryDetail.vue";
import { rootAnalysisTreeReadFactory } from "@mocks/analysis";
import { genericObjectReadFactory } from "@mocks/genericObject";
import { StringDecoder } from "string_decoder";

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
    const summary = {
      content: "test",
      format: genericObjectReadFactory(),
      header: "testHeader",
      uuid: "1111",
    };
    const rootAnalysis = rootAnalysisTreeReadFactory({
      summaryDetails: [summary],})
    cy.stub(Alert, "read").resolves(
      alertTreeReadFactory({ rootAnalysis: rootAnalysis }),
    );
    factory(false).then((wrapper) => {
      cy.get("@spy-9").should("have.been.calledOnce"); // unselectAll
      cy.get("@spy-6").should("have.been.calledOnce"); // select alert
      cy.get("@spy-5").should("have.been.calledOnce"); // 'patch' aka reset alertStore
      cy.get("@spy-3").should("have.been.calledOnce"); // read alert
      expect(wrapper.findComponent(TheAlertActionToolbarVue)).to.exist;
      expect(wrapper.findComponent(TheAlertSummaryVue)).to.exist;
      expect(wrapper.findComponent(AlertTreeVue)).to.exist;
      expect(wrapper.findComponent(AnalysisSummaryDetailVue)).to.exist;
      cy.contains("Summary Details").should('be.visible');
    });
  });

  it.only("displays all summary details", () => {
    const summary = {
      content: "test1",
      format: genericObjectReadFactory(),
      header: "testHeader1",
      uuid: "1111",
    };
    const summary2 = {
      content: "test2",
      format: genericObjectReadFactory(),
      header: "testHeader2",
      uuid: "2222",
    };
    const rootAnalysis = rootAnalysisTreeReadFactory({
      summaryDetails: [summary,summary2],})
    cy.stub(Alert, "read").resolves(
      alertTreeReadFactory({ rootAnalysis: rootAnalysis }),
    );
    factory(false).then((wrapper) => {
      expect(wrapper.findComponent(AnalysisSummaryDetailVue)).to.exist;
      cy.contains("Summary Details").should('be.visible');
      // cy.get('#pv_id_2_header > .pi').click();
      cy.contains("testHeader1").should('be.visible');
      cy.contains("testHeader2").should('be.visible');
    });
  });

  it("does not display Summary Details when there is none", () => {
    cy.stub(Alert, "read").resolves(
      alertTreeReadFactory({}),
    );
    factory(false)
    cy.contains("Summary Details").should('not.exist');
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
