import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import CommentModal from "@/components/Modals/CommentModal.vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { AlertComment } from "@/services/api/alertComment";
import { EventComment } from "@/services/api/eventComment";
import { userReadFactory } from "@mocks/user";

function factory(
  args: {
    objectType: "alerts" | "events";
    selectedAlertStore?: { selected: string[] };
    selectedEventStore?: { selected: string[] };
  } = {
    objectType: "alerts",
    selectedAlertStore: { selected: [] },
    selectedEventStore: { selected: [] },
  },
) {
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
            selectedAlertStore: args.selectedAlertStore,
            selectedEventStore: args.selectedEventStore,
            recentCommentsStore: {
              recentComments: ["test"],
            },
          },
        }),
      ],
      provide: {
        objectType: args.objectType,
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
  it("allows submit if both at least one object and comment text is added", () => {
    factory({
      objectType: "alerts",
      selectedAlertStore: { selected: ["uuid"] },
    });
    cy.findAllByPlaceholderText("Add a comment...").click().type("Testing");
    cy.findAllByText("Add").parent().should("not.be.disabled");
  });
  it("does not allow submit if no object is selected", () => {
    factory({ objectType: "alerts", selectedAlertStore: { selected: [] } });
    cy.findAllByPlaceholderText("Add a comment...").click().type("Testing");

    cy.findAllByText("Add").parent().should("be.disabled");
  });
  it("does not allow submit if no comment text is added", () => {
    factory({
      objectType: "alerts",
      selectedAlertStore: { selected: ["uuid"] },
    });
    cy.findAllByText("Add").parent().should("be.disabled");
  });
  it("correctly makes request to create alert comment upon adding comment text via CommentAutocomplete and submit", () => {
    cy.stub(AlertComment, "create")
      .withArgs([
        {
          username: "analyst",
          submissionUuid: "uuid",
          value: "test extra content",
        },
      ])
      .as("addComment")
      .resolves();
    factory({
      objectType: "alerts",
      selectedAlertStore: { selected: ["uuid"] },
    });
    cy.get(".p-autocomplete > .p-button").click();
    cy.contains("test").click();
    cy.get(".p-inputtextarea").click().type(" extra content");
    cy.findByText("Add").click();
    cy.get("@addComment").should("have.been.calledOnce");
    cy.get("@spy-10").should("have.been.calledOnceWith", "test extra content"); // Add comment to recentCommentsStore
    cy.get("[data-cy=CommentModal]").should("not.exist");
  });
  it("correctly makes request to create event comment upon adding comment text via CommentAutocomplete and submit", () => {
    cy.stub(EventComment, "create")
      .withArgs([
        {
          username: "analyst",
          eventUuid: "uuid",
          value: "test extra content",
        },
      ])
      .as("addComment")
      .resolves();
    factory({
      objectType: "events",
      selectedEventStore: { selected: ["uuid"] },
    });
    cy.get(".p-autocomplete > .p-button").click();
    cy.contains("test").click();
    cy.get(".p-inputtextarea").click().type(" extra content");
    cy.findByText("Add").click();
    cy.get("@addComment").should("have.been.calledOnce");
    cy.get("@spy-10").should("have.been.calledOnceWith", "test extra content"); // Add comment to recentCommentsStore
    cy.get("[data-cy=CommentModal]").should("not.exist");
  });
  it("correctly makes request to create alert comment upon adding comment text and submit", () => {
    cy.stub(AlertComment, "create")
      .withArgs([
        {
          username: "analyst",
          submissionUuid: "uuid",
          value: "Testing",
        },
      ])
      .as("addComment")
      .resolves();
    factory({
      objectType: "alerts",
      selectedAlertStore: { selected: ["uuid"] },
    });
    cy.findAllByPlaceholderText("Add a comment...").click().type("Testing");
    cy.findByText("Add").click();
    cy.get("@addComment").should("have.been.calledOnce");
    cy.get("@spy-10").should("have.been.calledOnceWith", "Testing"); // Add comment to recentCommentsStore
    cy.get("[data-cy=CommentModal]").should("not.exist");
  });
  it("correctly makes request to create event comment upon adding comment text and submit", () => {
    cy.stub(EventComment, "create")
      .withArgs([
        {
          username: "analyst",
          eventUuid: "uuid",
          value: "Testing",
        },
      ])
      .as("addComment")
      .resolves();
    factory({
      objectType: "events",
      selectedEventStore: { selected: ["uuid"] },
    });
    cy.findAllByPlaceholderText("Add a comment...").click().type("Testing");
    cy.findByText("Add").click();
    cy.get("@addComment").should("have.been.calledOnce");
    cy.get("@spy-10").should("have.been.calledOnceWith", "Testing"); // Add comment to recentCommentsStore
    cy.get("[data-cy=CommentModal]").should("not.exist");
  });
  it("correctly shows error if request to assign owner fails", () => {
    cy.stub(AlertComment, "create")
      .withArgs([
        {
          username: "analyst",
          submissionUuid: "uuid",
          value: "Testing",
        },
      ])
      .as("addComment")
      .rejects(new Error("404 request failed"));
    factory({
      objectType: "alerts",
      selectedAlertStore: { selected: ["uuid"] },
    });
    cy.findAllByPlaceholderText("Add a comment...").click().type("Testing");
    cy.findByText("Add").click();
    cy.get("@addComment").should("have.been.calledOnce");
    cy.get("[data-cy=CommentModal]").should("be.visible");
    cy.contains("404 request failed").should("be.visible");
  });
});
