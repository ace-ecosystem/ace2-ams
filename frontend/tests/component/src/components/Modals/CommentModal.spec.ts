// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import CommentModal from "@/components/Modals/CommentModal.vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { NodeComment } from "@/services/api/nodeComment";
import { userReadFactory } from "@mocks/user";
import Message from "primevue/message";

function factory(args: { selected: string[] } = { selected: [] }) {
  mount(CommentModal, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          stubActions: false,
          initialState: {
            authStore: {
              user: userReadFactory(),
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
      name: "CommentModal",
    },
  });
  cy.vue().then((wrapper) => {
    wrapper.vm.modalStore.open("CommentModal");
  });
  cy.get("[data-cy=CommentModal]").should("be.visible");
  cy.findAllByText("Add Comment").should("be.visible");
  cy.findAllByPlaceholderText("Add a comment...").should("be.visible");
  cy.findAllByText("Nevermind").should("be.visible");
  cy.findAllByText("Add").should("be.visible");
}

describe("CommentModal", () => {
  it("allows submit if both at least one node and comment text is added", () => {
    factory({ selected: ["uuid"] });
    cy.findAllByPlaceholderText("Add a comment...").click().type("Testing");
    cy.findAllByText("Add").parent().should("not.be.disabled");
  });
  it("does not allow submit if no node is selected", () => {
    factory({ selected: [] });
    cy.findAllByPlaceholderText("Add a comment...").click().type("Testing");

    cy.findAllByText("Add").parent().should("be.disabled");
  });
  it("does not allow submit if no comment text is added", () => {
    factory({ selected: ["uuid"] });
    cy.findAllByText("Add").parent().should("be.disabled");
  });
  it("correctly makes request to create comment upon adding comment text and submit", () => {
    cy.stub(NodeComment, "create")
      .withArgs([
        {
          username: "analyst",
          nodeUuid: "uuid",
          value: "Testing",
        },
      ])
      .as("addComment")
      .resolves();
    factory({ selected: ["uuid"] });
    cy.findAllByPlaceholderText("Add a comment...").click().type("Testing");
    cy.findByText("Add").click();
    cy.get("@addComment").should("have.been.calledOnce");
    cy.get("[data-cy=CommentModal]").should("not.exist");
  });
  it("correctly shows error if request to assign owner fails", () => {
    cy.stub(NodeComment, "create")
      .withArgs([
        {
          username: "analyst",
          nodeUuid: "uuid",
          value: "Testing",
        },
      ])
      .as("addComment")
      .rejects(new Error("404 request failed"));
    factory({ selected: ["uuid"] });
    cy.findAllByPlaceholderText("Add a comment...").click().type("Testing");
    cy.findByText("Add").click();
    cy.get("@addComment").should("have.been.calledOnce");
    cy.get("[data-cy=CommentModal]").should("be.visible");
    cy.vue().then((wrapper) => {
      expect(wrapper.findComponent(Message)).to.exist;
      cy.contains("404 request failed").should("be.visible");
    });
  });
});
