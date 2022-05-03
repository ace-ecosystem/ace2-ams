import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import TheAlertActionToolbar from "@/components/Alerts/TheAlertActionToolbar.vue";
import router from "@/router/index";

interface TheAlertActionToolbarProps {
  reloadObject: "node" | "table";
  showFalsePositiveShortcut?: boolean;
  showIgnoreShortcut?: boolean;
}

const defaultProps: TheAlertActionToolbarProps = {
  reloadObject: "node",
};

function factory(props = defaultProps) {
  return mount(TheAlertActionToolbar, {
    global: {
      plugins: [PrimeVue, createPinia(), router],
      provide: {
        nodeType: "alerts",
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
      reloadObject: "node",
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
      reloadObject: "node",
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
      reloadObject: "node",
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
});
