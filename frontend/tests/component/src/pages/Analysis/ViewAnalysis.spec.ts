import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import router from "@/router";

import { testConfiguration } from "@/etc/configuration/test/index";
import ViewAnalysis from "@/pages/Analysis/ViewAnalysis.vue";
import { userReadFactory } from "@mocks/user";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { alertReadFactory } from "@mocks/alert";
import {
  analysisModuleTypeReadFactory,
  analysisReadFactory,
} from "@mocks/analysis";
import { Analysis } from "@/services/api/analysis";
import { alertRead } from "@/models/alert";
import AnalysisDetailsBase from "@/components/Analysis/AnalysisDetailsBase.vue";
import TestComponent from "@/components/test/TestComponent.vue";

function factory(initialAlert: alertRead | null = alertReadFactory()) {
  mount(ViewAnalysis, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          initialState: {
            authStore: {
              user: userReadFactory(),
            },
            alertStore: { open: initialAlert },
          },
        }),
        router,
      ],
      provide: {
        config: testConfiguration,
      },
    },
  });
}

describe("ViewAnalysis", () => {
  it("renders correctly when neither alert nor analysis are available", () => {
    cy.stub(Analysis, "read").rejects(new Error("Could not load analysis"));
    factory(null);
    cy.get(".p-menuitem-link").eq(1).should("have.text", '"Unknown Alert"');
    cy.get(".p-menuitem-link").eq(2).should("have.text", '"Unknown Analysis"');
    cy.get("body").then(() => {
      cy.wrap(Cypress.vueWrapper.findComponent(AnalysisDetailsBase)).should(
        "exist",
      );
    });
  });
  it("renders correctly when parent alert is available, but analysis is not", () => {
    cy.stub(Analysis, "read").rejects(new Error("Could not load analysis"));
    factory();
    cy.get(".p-menuitem-link").eq(1).should("have.text", '"Test Alert"');
    cy.get(".p-menuitem-link").eq(2).should("have.text", '"Unknown Analysis"');
    cy.get("body").then(() => {
      cy.wrap(Cypress.vueWrapper.findComponent(AnalysisDetailsBase)).should(
        "exist",
      );
    });
  });
  it("renders correctly when parent alert is not available, but analysis is available", () => {
    cy.stub(Analysis, "read").resolves(analysisReadFactory());
    factory(null);
    cy.get(".p-menuitem-link").eq(1).should("have.text", '"Unknown Alert"');
    cy.get(".p-menuitem-link").eq(2).should("have.text", '"File Analysis"');
    cy.get("body").then(() => {
      cy.wrap(Cypress.vueWrapper.findComponent(AnalysisDetailsBase)).should(
        "exist",
      );
    });
  });
  it("renders correctly when parent alert and analysis are available, and there IS NOT a configured component for analysis type", () => {
    cy.stub(Analysis, "read").resolves(analysisReadFactory());
    factory();
    cy.get(".p-menuitem-link").eq(1).should("have.text", '"Test Alert"');
    cy.get(".p-menuitem-link").eq(2).should("have.text", '"File Analysis"');
    cy.get("body").then(() => {
      cy.wrap(Cypress.vueWrapper.findComponent(AnalysisDetailsBase)).should(
        "exist",
      );
    });
  });
  it("renders correctly when parent alert and analysis are available, and there IS configured component for analysis type", () => {
    cy.stub(Analysis, "read").resolves(
      analysisReadFactory({
        analysisModuleType: analysisModuleTypeReadFactory({
          value: "Test Analysis",
        }),
      }),
    );
    factory();
    cy.get(".p-menuitem-link").eq(1).should("have.text", '"Test Alert"');
    cy.get(".p-menuitem-link").eq(2).should("have.text", '"Test Analysis"');
    cy.get("body").then(() => {
      cy.wrap(Cypress.vueWrapper.findComponent(TestComponent)).should("exist");
    });
  });
});
