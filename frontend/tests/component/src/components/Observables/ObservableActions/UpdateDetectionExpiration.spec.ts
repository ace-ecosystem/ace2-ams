import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import UpdateDetectionExpiration from "@/components/Observables/ObservableActions/UpdateDetectionExpiration.vue";
import { observableTreeRead } from "@/models/observable";
import { observableTreeReadFactory } from "@mocks/observable";
import { userReadFactory } from "@mocks/user";
import { ObservableInstance } from "@/services/api/observable";
import { createCustomCypressPinia } from "@tests/cypressHelpers";

function factory(args: { observable: observableTreeRead }) {
  return mount(UpdateDetectionExpiration, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          stubActions: false,
          initialState: {
            authStore: {
              user: userReadFactory(),
            },
          },
        }),
      ],
      provide: {
        nodeType: "alerts",
      },
    },
    propsData: {
      name: "UpdateDetectionExpiration",
      observable: args.observable,
    },
  }).then((wrapper) => {
    wrapper.vm.modalStore.open("UpdateDetectionExpiration");
    cy.get("[data-cy=UpdateDetectionExpiration]").should("be.visible");
    cy.contains("Update Detection Expiration Time").should("be.visible");
    cy.contains("Current Expiration Time (UTC)").should("be.visible");
    cy.contains("This observable should never expire.").should("be.visible");
    cy.contains("Nevermind").should("be.visible");
    cy.contains("Do it!").should("be.visible");
  });
}

describe("UpdateDetectionExpiration", () => {
  const expirationDate = new Date(2022, 4, 20, 12, 0, 0);
  const expirationDateString = expirationDate.toUTCString();

  const neverExpires = observableTreeReadFactory({
    forDetection: true,
  });
  const doesExpire = observableTreeReadFactory({
    forDetection: true,
    expiresOn: expirationDate.toISOString(),
  });

  it("renders correctly if observable does have an expiration datetime", () => {
    factory({ observable: doesExpire });
    cy.findByRole("switch").should("not.be.checked");
    cy.contains(expirationDateString).should("be.visible");
    cy.contains("New Expiration Time (UTC)").should("be.visible");
    cy.findByPlaceholderText("Enter a valid date")
      .should("be.visible")
      .should("have.value", "");
  });
  it("renders correctly if observable does not have an expiration datetime", () => {
    factory({ observable: neverExpires });
    cy.findByRole("switch").should("be.checked");
    cy.contains("New Expiration Time (UTC)").should("not.exist");
    cy.findByPlaceholderText("Enter a valid date").should("not.exist");
  });
  it("does not allow submission if no new expiration datetime is given", () => {
    factory({ observable: neverExpires });
    cy.contains("Do it!").should("not.be.disabled");
    cy.findByRole("switch").parent().parent().click();
    cy.contains("Do it!").should("be.disabled");
    cy.findByPlaceholderText("Enter a valid date")
      .click()
      .type("04/22/2022 12:00:00");
    cy.contains("Do it!").should("not.be.disabled");
  });
  it("correctly attempts to set observable expiration to null on submit", () => {
    cy.stub(ObservableInstance, "update")
      .withArgs("observableUuid1", {
        expiresOn: null,
        historyUsername: "analyst",
      })
      .as("updateObservable")
      .resolves();
    factory({ observable: doesExpire });
    cy.findByRole("switch").parent().parent().click();
    cy.contains("Do it!").click();
    cy.get("@updateObservable").should("have.been.calledOnce");
    cy.get("Update Detection Expiration Time").should("not.exist");
  });
  it("correctly attempts to set observable expiration to a new datetime on submit", () => {
    cy.stub(ObservableInstance, "update")
      .withArgs("observableUuid1", {
        expiresOn: new Date("04/22/2022 12:00:00"),
        historyUsername: "analyst",
      })
      .as("updateObservable")
      .resolves();
    factory({ observable: doesExpire });
    cy.findByPlaceholderText("Enter a valid date")
      .click()
      .type("04/22/2022 12:00:00");
    cy.contains("Do it!").click();
    cy.get("@updateObservable").should("have.been.calledOnce");
    cy.get("Update Detection Expiration Time").should("not.exist");
  });
  it("correctly shows error if request to update expiration fails", () => {
    cy.stub(ObservableInstance, "update")
      .withArgs("observableUuid1", {
        expiresOn: null,
        historyUsername: "analyst",
      })
      .as("updateObservable")
      .rejects(new Error("404 request failed"));
    factory({ observable: doesExpire });
    cy.findByRole("switch").parent().parent().click();
    cy.contains("Do it!").click();
    cy.get("@updateObservable").should("have.been.calledOnce");
    cy.get("[data-cy='error-banner']")
      .contains("404 request failed")
      .should("be.visible");
  });
});
