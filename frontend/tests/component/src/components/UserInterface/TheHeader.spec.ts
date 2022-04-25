import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import router from "@/router/index";
import authApi from "@/services/api/auth";

import TheHeader from "@/components/UserInterface/TheHeader.vue";

function factory() {
  mount(TheHeader, {
    global: {
      plugins: [PrimeVue, createPinia(), router],
    },
  });
}

describe("TheHeader", () => {
  it("renders with expected elements", () => {
    factory();
    cy.get("img").should("be.visible");
    cy.contains("Analyze").should("be.visible");
    cy.contains("Alerts").should("be.visible");
    cy.contains("Events").should("be.visible");
    cy.get(".pi").should("have.length", 5);
  });
  it("should attempt to logout when logout button clicked", () => {
    cy.stub(authApi, "logout").as("logout").resolves();
    factory();
    cy.get(".pi").last().click();
    cy.get("@logout").should("have.been.calledOnce");
  });
});
