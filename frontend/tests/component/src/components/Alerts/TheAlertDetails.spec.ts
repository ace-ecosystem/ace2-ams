import { mount } from "@cypress/vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";

import PrimeVue from "primevue/config";

import TheAlertDetails from "@/components/Alerts/TheAlertDetails.vue";
import router from "@/router/index";
import { alertTreeReadFactory } from "@mocks/alert";
import { alertRead } from "@/models/alert";
import { genericObjectReadFactory } from "@mocks/genericObject";
import { userReadFactory } from "@mocks/user";
import { metadataTagReadFactory } from "@mocks/metadata";
import { testConfiguration } from "@/etc/configuration/test/index";
import { rootAnalysisTreeReadFactory } from "@mocks/analysis";

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
      provide: {
        config: testConfiguration,
      },
    },
  });
}

describe("TheAlertDetails", () => {
  it("renders correctly when there is not an open alert", () => {
    factory({
      open: null,
      requestReload: false,
    });
    cy.contains("Alert Details").should("be.visible");
    cy.get(".pi").click();
    cy.contains("No alert details available.").should("be.visible");
  });
  it("renders correctly when there is an open alert that has no available details", () => {
    factory({
      open: alertTreeReadFactory({}),
      requestReload: false,
    });
    cy.contains("Alert Details").should("be.visible");
    cy.get(".pi").click();
    cy.contains("No alert details available.").should("be.visible");
  });
  it("renders correctly when there that has available details and a configured custom component", () => {
    factory({
      open: alertTreeReadFactory({
        rootAnalysis: rootAnalysisTreeReadFactory({
          details: { test: "content" },
        }),
        type: genericObjectReadFactory({ value: "test type - a" }),
      }),
      requestReload: false,
    });
    cy.contains("Alert Details").should("be.visible");
    cy.get(".pi").click();
    cy.contains("Testing 123").should("be.visible");
  });
  it("renders correctly when there that has available details and no configured custom component", () => {
    factory({
      open: alertTreeReadFactory({
        rootAnalysis: rootAnalysisTreeReadFactory({
          details: { test: "content" },
        }),
      }),
      requestReload: false,
    });
    cy.contains("Alert Details").should("be.visible");
    cy.get(".pi").click();
    cy.contains('{ "test": "content" }').should("be.visible");
  });
});
