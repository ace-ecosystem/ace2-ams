import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import TheAlertActionToolbar from "@/components/Alerts/TheAlertActionToolbar.vue";
import router from "@/router/index";

interface TheAlertActionToolbarProps {
  reloadObject: "object" | "table";
  showFalsePositiveShortcut?: boolean;
  showIgnoreShortcut?: boolean;
}

const defaultProps: TheAlertActionToolbarProps = {
  reloadObject: "object",
};

function factory(props = defaultProps) {
  return mount(TheAlertActionToolbar, {
    global: {
      plugins: [PrimeVue, createPinia(), router],
      provide: {
        objectType: "alerts",
      },
    },
    propsData: props,
  });
}

describe("TheAlertActionToolbar", () => {
  it("renders as expected", () => {
    factory();
    cy.contains("Disposition").should("be.visible");
    cy.contains("Remediate").should("be.visible");
  });
  it("opens disposition modal when 'Disposition' button clicked", () => {
    factory();
    cy.contains("Disposition").click();
    cy.contains("Set Disposition").should("be.visible");
  });
  it("renders as expected when optional button props are enabled", () => {
    factory({
      reloadObject: "object",
      showFalsePositiveShortcut: true,
      showIgnoreShortcut: true,
    });
    cy.contains("FP").should("be.visible");
    cy.contains("Ignore").should("be.visible");
    cy.contains("Disposition").should("be.visible");
    cy.contains("Remediate").should("be.visible");
  });
  it("should emit 'falsePositiveClicked' when FP button clicked", () => {
    factory({
      reloadObject: "object",
      showFalsePositiveShortcut: true,
    });
    cy.contains("FP")
      .click()
      .then(() => {
        cy.wrap(Cypress.vueWrapper.emitted()).should(
          "have.property",
          "falsePositiveClicked",
        );
      });
  });
  it("should emit 'ignoreClicked' when ignore button clicked", () => {
    factory({
      reloadObject: "object",
      showIgnoreShortcut: true,
    });
    cy.contains("Ignore")
      .click()
      .then(() => {
        cy.wrap(Cypress.vueWrapper.emitted()).should(
          "have.property",
          "ignoreClicked",
        );
      });
  });
  it("should show Add Observables button when reload object is 'object'", () => {
    factory({
      reloadObject: "object",
    });
    cy.contains("Add Observable(s)").should("be.visible");
  });
  it("should not show Add Observables button when reload object is not 'object'", () => {
    factory({
      reloadObject: "table",
    });
    cy.contains("Add Observable(s)").should("not.be.exist");
  });
});
