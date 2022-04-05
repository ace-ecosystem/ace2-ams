// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import TheAlertActionToolbar from "@/components/Alerts/TheAlertActionToolbar.vue";
import router from "@/router/index";

const props = {
  reloadObject: "node",
};

function factory() {
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
});
