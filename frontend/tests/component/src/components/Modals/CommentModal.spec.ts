import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import CommentModal from "@/components/Modals/CommentModal.vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { Comment } from "@/services/api/comment";
import { userReadFactory } from "@mocks/user";

function factory(args: { selected: string[] } = { selected: [] }) {
  return mount(CommentModal, {
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
            recentCommentsStore: {
              recentComments: ["test"],
            },
          },
        }),
      ],
      provide: {
        objectType: "alerts",
      },
    },
    propsData: {
      name: "CommentModal",
    },
  }).then((wrapper) => {
    wrapper.vm.modalStore.open("CommentModal");
    cy.get("[data-cy=CommentModal]").should("be.visible");
    cy.findAllByText("Add Comment").should("be.visible");
    cy.findAllByPlaceholderText("Add a comment...").should("be.visible");
    cy.findAllByText("Nevermind").should("be.visible");
    cy.findAllByText("Add").should("be.visible");
  });
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
  it("correctly makes request to create comment upon adding comment text via CommentAutocomplete and submit", () => {
    cy.stub(Comment, "create")
      .withArgs([
        {
          username: "analyst",
          nodeUuid: "uuid",
          value: "test extra content",
        },
      ])
      .as("addComment")
      .resolves();
    factory({ selected: ["uuid"] });
    cy.get(".p-autocomplete > .p-button").click();
    cy.contains("test").click();
    cy.get(".p-inputtextarea").click().type(" extra content");
    cy.findByText("Add").click();
    cy.get("@addComment").should("have.been.calledOnce");
    cy.get("@spy-10").should("have.been.calledOnceWith", "test extra content"); // Add comment to recentCommentsStore
    cy.get("[data-cy=CommentModal]").should("not.exist");
  });
  it("correctly makes request to create comment upon adding comment text and submit", () => {
    cy.stub(Comment, "create")
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
    cy.get("@spy-10").should("have.been.calledOnceWith", "Testing"); // Add comment to recentCommentsStore
    cy.get("[data-cy=CommentModal]").should("not.exist");
  });
  it("correctly shows error if request to assign owner fails", () => {
    cy.stub(Comment, "create")
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
    cy.contains("404 request failed").should("be.visible");
  });
});
