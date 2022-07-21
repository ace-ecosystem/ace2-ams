import { mount } from "@cypress/vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { userReadFactory } from "@mocks/user";

import PrimeVue from "primevue/config";
import router from "@/router/index";
import authApi from "@/services/api/auth";

import TheHeader from "@/components/UserInterface/TheHeader.vue";

function factory(user: any) {
  mount(TheHeader, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          initialState: {
            authStore: {
              user: user,
            },
          },
        }),
        router,
      ],
    },
  });
}

describe("TheHeader", () => {
  it("renders with expected elements when not auth'd", () => {
    factory(null);
    cy.get("img").should("be.visible");
    cy.contains("Analyze").should("not.exist");
    cy.contains("Alerts").should("not.exist");
    cy.contains("Events").should("not.exist");
    cy.get(".pi").should("have.length", 1);
  });
  it("renders with expected elements when auth'd", () => {
    factory(userReadFactory());
    cy.get("img").should("be.visible");
    cy.contains("Analyze").should("be.visible");
    cy.contains("Alerts").should("be.visible");
    cy.contains("Events").should("be.visible");
    cy.get(".pi").should("have.length", 5);
  });
  it("should attempt to logout when logout button clicked", () => {
    cy.stub(authApi, "logout").as("logout").resolves();
    factory(userReadFactory());
    cy.get(".pi").last().click();
    cy.get("@logout").should("have.been.calledOnce");
  });
});
