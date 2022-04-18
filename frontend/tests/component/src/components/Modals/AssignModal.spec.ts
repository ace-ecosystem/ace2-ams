// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import AssignModal from "@/components/Modals/AssignModal.vue";
import { userRead } from "@/models/user";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { userReadFactory } from "@mocks/user";
import { Alert } from "@/services/api/alert";
import Message from "primevue/message";

function factory(
  args: { users: userRead[]; selected: string[] } = { users: [], selected: [] },
) {
  mount(AssignModal, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          stubActions: false,
          initialState: {
            userStore: {
              items: args.users,
            },
            selectedAlertStore: {
              selected: args.selected,
            },
          },
        }),
      ],
      provide: {
        nodeType: "alerts",
      },
    },
    propsData: {
      name: "AssignModal",
    },
  });
  cy.vue().then((wrapper) => {
    wrapper.vm.modalStore.open("AssignModal");
  });
  cy.get("[data-cy=AssignModal]").should("be.visible");
  cy.findAllByText("Assign Ownership").should("be.visible");
  cy.findAllByText("Select a user").should("be.visible");
  cy.findAllByText("Nevermind").should("be.visible");
  cy.findAllByText("Assign").should("be.visible");
}

describe("AssignModal", () => {
  const users = [
    userReadFactory({ displayName: "Analyst A" }),
    userReadFactory({ displayName: "Analyst B" }),
  ];

  it("renders options correctly if no users available", () => {
    factory();
    cy.contains("Select a user").click();
    cy.contains("No available options").should("be.visible");
  });
  it("renders options correctly if users are available", () => {
    factory({ users: users, selected: [] });
    cy.contains("Select a user").click();
    cy.contains("Analyst A").should("be.visible");
    cy.contains("Analyst B").should("be.visible");
  });
  it("allows submit if both at least one node and a user are selected", () => {
    factory({ users: users, selected: ["uuid"] });
    cy.contains("Select a user").click();
    cy.contains("Analyst B").click();
    cy.findAllByText("Assign").parent().should("not.be.disabled");
  });
  it("does not allow submit if no node is selected", () => {
    factory({ users: users, selected: [] });
    cy.contains("Select a user").click();
    cy.contains("Analyst B").click();
    cy.findAllByText("Assign").parent().should("be.disabled");
  });
  it("does not allow submit if no user is selected", () => {
    factory({ users: [], selected: ["uuid"] });
    cy.findAllByText("Assign").parent().should("be.disabled");
  });
  it("correctly makes request to assign owner upon user selection and submit", () => {
    cy.stub(Alert, "update")
      .withArgs([{ uuid: "uuid", owner: "analyst" }])
      .as("updateAlert")
      .resolves();
    factory({ users: users, selected: ["uuid"] });
    cy.contains("Select a user").click();
    cy.contains("Analyst B").click();
    cy.findByText("Assign").click();
    cy.get("@updateAlert").should("have.been.calledOnce");
    cy.get("[data-cy=AssignModal]").should("not.exist");
  });
  it("correctly shows error if request to assign owner fails", () => {
    cy.stub(Alert, "update")
      .withArgs([{ uuid: "uuid", owner: "analyst" }])
      .as("updateAlert")
      .rejects(new Error("404 request failed"));
    factory({ users: users, selected: ["uuid"] });
    cy.contains("Select a user").click();
    cy.contains("Analyst B").click();
    cy.findByText("Assign").click();
    cy.get("@updateAlert").should("have.been.calledOnce");
    cy.get("[data-cy=AssignModal]").should("be.visible");
    cy.vue().then((wrapper) => {
      expect(wrapper.findComponent(Message)).to.exist;
      cy.contains("404 request failed").should("be.visible");
    });
  });
});
